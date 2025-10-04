-- Postgres DDL for IPO Analytics schema (mirrors utils/database.py)

CREATE TABLE IF NOT EXISTS ipo_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR NOT NULL UNIQUE,
    company_name VARCHAR,
    sector VARCHAR,
    industry VARCHAR,
    exchange VARCHAR,
    country VARCHAR,
    region VARCHAR,
    ipo_date DATE,
    ipo_price DOUBLE PRECISION,
    current_price DOUBLE PRECISION,
    market_cap BIGINT,
    price_change_since_ipo DOUBLE PRECISION,
    volume BIGINT,
    last_updated VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ipo_ticker ON ipo_data (ticker);
CREATE INDEX IF NOT EXISTS idx_ipo_sector ON ipo_data (sector);
CREATE INDEX IF NOT EXISTS idx_ipo_exchange ON ipo_data (exchange);
CREATE INDEX IF NOT EXISTS idx_ipo_date ON ipo_data (ipo_date);
CREATE INDEX IF NOT EXISTS idx_ipo_market_cap ON ipo_data (market_cap);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR NOT NULL,
    total_return DOUBLE PRECISION,
    annualized_volatility DOUBLE PRECISION,
    max_drawdown DOUBLE PRECISION,
    days_since_ipo INTEGER,
    high_52w DOUBLE PRECISION,
    low_52w DOUBLE PRECISION,
    avg_volume DOUBLE PRECISION,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS refresh_log (
    id SERIAL PRIMARY KEY,
    refresh_type VARCHAR,
    status VARCHAR,
    records_processed INTEGER,
    error_message TEXT,
    started_at VARCHAR,
    completed_at VARCHAR
);

CREATE TABLE IF NOT EXISTS sign_up (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


