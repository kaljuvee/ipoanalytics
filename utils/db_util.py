import os
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Text, Float, DateTime, UniqueConstraint
)
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select, and_, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

DB_URL = os.getenv("DB_URL")
engine: Optional[Engine] = create_engine(DB_URL, pool_pre_ping=True) if DB_URL else None

metadata = MetaData()

# Define tables mirroring utils/database.py schema
ipo_data = Table(
    "ipo_data",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ticker", String, nullable=False),
    Column("company_name", String),
    Column("sector", String),
    Column("industry", String),
    Column("exchange", String),
    Column("country", String),
    Column("region", String),
    Column("ipo_date", DateTime),  # store as date/time in Postgres
    Column("ipo_price", Float),
    Column("current_price", Float),
    Column("market_cap", Integer),
    Column("price_change_since_ipo", Float),
    Column("volume", Integer),
    Column("last_updated", String),
    Column("created_at", DateTime, default=datetime.utcnow),
    UniqueConstraint("ticker", name="uq_ipo_ticker"),
)

performance_metrics = Table(
    "performance_metrics",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ticker", String, nullable=False),
    Column("total_return", Float),
    Column("annualized_volatility", Float),
    Column("max_drawdown", Float),
    Column("days_since_ipo", Integer),
    Column("high_52w", Float),
    Column("low_52w", Float),
    Column("avg_volume", Float),
    Column("calculated_at", DateTime, default=datetime.utcnow),
)

refresh_log = Table(
    "refresh_log",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("refresh_type", String),
    Column("status", String),
    Column("records_processed", Integer),
    Column("error_message", Text),
    Column("started_at", String),
    Column("completed_at", String),
)

sign_up = Table(
    "sign_up",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    UniqueConstraint("email", name="uq_signup_email"),
)


def remote_db_available() -> bool:
    return engine is not None


def init_remote_database() -> None:
    if not remote_db_available():
        return
    metadata.create_all(engine)


def insert_ipo_records_remote(records: List[Dict]) -> int:
    if not remote_db_available() or not records:
        return 0
    init_remote_database()
    upsertable_fields = [
        "company_name", "sector", "industry", "exchange", "country", "region",
        "ipo_date", "ipo_price", "current_price", "market_cap",
        "price_change_since_ipo", "volume", "last_updated"
    ]
    count = 0
    with engine.begin() as conn:
        for rec in records:
            stmt = pg_insert(ipo_data).values(
                ticker=rec["ticker"],
                company_name=rec.get("company_name"),
                sector=rec.get("sector"),
                industry=rec.get("industry"),
                exchange=rec.get("exchange"),
                country=rec.get("country", "Unknown"),
                region=rec.get("region", "Other"),
                ipo_date=rec.get("ipo_date"),
                ipo_price=rec.get("ipo_price"),
                current_price=rec.get("current_price"),
                market_cap=rec.get("market_cap"),
                price_change_since_ipo=rec.get("price_change_since_ipo"),
                volume=rec.get("volume"),
                last_updated=rec.get("last_updated"),
            )
            update_set = {field: getattr(stmt.excluded, field) for field in upsertable_fields}
            stmt = stmt.on_conflict_do_update(index_elements=[ipo_data.c.ticker], set_=update_set)
            conn.execute(stmt)
            count += 1
    return count


def get_ipo_data_remote(year: Optional[int] = None, exchange: Optional[str] = None,
                        sector: Optional[str] = None, limit: Optional[int] = None) -> pd.DataFrame:
    if not remote_db_available():
        return pd.DataFrame()
    init_remote_database()
    clauses = ["1=1"]
    params: Dict[str, object] = {}
    if year is not None:
        # robust year filter for both DATE and VARCHAR columns
        clauses.append("substring(CAST(ipo_date AS TEXT),1,4) = :year_text")
        params["year_text"] = str(year)
    if exchange:
        clauses.append("exchange = :exchange")
        params["exchange"] = exchange
    if sector:
        clauses.append("sector = :sector")
        params["sector"] = sector
    order = " ORDER BY market_cap DESC"
    limit_sql = " LIMIT :limit" if limit else ""
    if limit:
        params["limit"] = limit
    sql = f"SELECT * FROM ipo_data WHERE {' AND '.join(clauses)}{order}{limit_sql}"
    with engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn, params=params)


def log_refresh_remote(refresh_type: str, status: str, records_processed: int = 0,
                       error_message: Optional[str] = None, started_at: Optional[str] = None) -> int:
    if not remote_db_available():
        return 0
    init_remote_database()
    with engine.begin() as conn:
        result = conn.execute(
            refresh_log.insert().values(
                refresh_type=refresh_type,
                status=status,
                records_processed=records_processed,
                error_message=error_message,
                started_at=started_at or datetime.utcnow().isoformat(),
                completed_at=datetime.utcnow().isoformat(),
            )
        )
        return int(result.inserted_primary_key[0]) if result.inserted_primary_key else 0


def get_last_refresh_remote() -> Optional[Dict]:
    if not remote_db_available():
        return None
    init_remote_database()
    with engine.connect() as conn:
        df = pd.read_sql_query(text("SELECT * FROM refresh_log ORDER BY completed_at DESC LIMIT 1"), conn)
        if df.empty:
            return None
        return df.iloc[0].to_dict()


def insert_signup_email_remote(email: str) -> bool:
    if not remote_db_available() or not email or '@' not in email:
        return False
    init_remote_database()
    with engine.begin() as conn:
        stmt = pg_insert(sign_up).values(email=email.strip().lower())
        stmt = stmt.on_conflict_do_nothing(index_elements=[sign_up.c.email])
        conn.execute(stmt)
    return True


