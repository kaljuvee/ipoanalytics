"""
Global Markets Utility for IPO Map
Comprehensive exchange and country mappings for worldwide IPO coverage
"""

import logging

logger = logging.getLogger(__name__)

# Comprehensive global exchange to country mapping
GLOBAL_EXCHANGE_MAPPING = {
    # North America
    "NASDAQ": "United States",
    "NYSE": "United States", 
    "AMEX": "United States",
    "TSX": "Canada",
    "TSXV": "Canada",
    
    # Europe
    "LSE": "United Kingdom",
    "AIM": "United Kingdom", 
    "LON": "United Kingdom",
    "XETRA": "Germany",
    "FSE": "Germany",
    "FRA": "Germany",
    "BER": "Germany",
    "EPA": "France",
    "EURONEXT": "France",
    "PAR": "France",
    "AMS": "Netherlands",
    "BIT": "Italy",
    "MIL": "Italy",
    "BME": "Spain",
    "MCE": "Spain",
    "MAD": "Spain",
    "SIX": "Switzerland",
    "VTX": "Switzerland",
    "STO": "Sweden",
    "HEL": "Finland",
    "CPH": "Denmark",
    "OSL": "Norway",
    "WSE": "Poland",
    "BUD": "Hungary",
    "PRA": "Czech Republic",
    "ATH": "Greece",
    "LIS": "Portugal",
    "BRU": "Belgium",
    "VIE": "Austria",
    "TAL": "Estonia",
    "RIG": "Latvia",
    "VSE": "Lithuania",
    
    # Asia Pacific
    "TSE": "Japan",
    "TYO": "Japan",
    "JPX": "Japan",
    "NIKKEI": "Japan",
    "SSE": "China",
    "SZSE": "China",
    "HKEX": "Hong Kong",
    "HKG": "Hong Kong",
    "KRX": "South Korea",
    "KOSPI": "South Korea",
    "KOSDAQ": "South Korea",
    "SGX": "Singapore",
    "ASX": "Australia",
    "NZX": "New Zealand",
    "SET": "Thailand",
    "KLSE": "Malaysia",
    "IDX": "Indonesia",
    "PSE": "Philippines",
    "VNX": "Vietnam",
    "TWSE": "Taiwan",
    "TPE": "Taiwan",
    
    # India
    "NSE": "India",
    "BSE": "India",
    "NSEI": "India",
    "BSESN": "India",
    
    # Middle East & Africa
    "TADAWUL": "Saudi Arabia",
    "DFM": "UAE",
    "ADX": "UAE",
    "EGX": "Egypt",
    "JSE": "South Africa",
    "TASE": "Israel",
    "QSE": "Qatar",
    "MSM": "Oman",
    "BHB": "Bahrain",
    "KSE": "Kuwait",
    
    # Latin America
    "BOVESPA": "Brazil",
    "B3": "Brazil",
    "BMV": "Mexico",
    "BCS": "Chile",
    "BVC": "Colombia",
    "BVL": "Peru",
    "BYMA": "Argentina",
}

# Regional groupings for analysis
REGIONAL_GROUPS = {
    "North America": ["United States", "Canada"],
    "Europe": [
        "United Kingdom", "Germany", "France", "Netherlands", "Italy", "Spain", 
        "Switzerland", "Sweden", "Finland", "Denmark", "Norway", "Poland", 
        "Hungary", "Czech Republic", "Greece", "Portugal", "Belgium", "Austria",
        "Estonia", "Latvia", "Lithuania"
    ],
    "Asia Pacific": [
        "Japan", "China", "Hong Kong", "South Korea", "Singapore", "Australia", 
        "New Zealand", "Thailand", "Malaysia", "Indonesia", "Philippines", 
        "Vietnam", "Taiwan"
    ],
    "India": ["India"],
    "Middle East & Africa": [
        "Saudi Arabia", "UAE", "Egypt", "South Africa", "Israel", "Qatar", 
        "Oman", "Bahrain", "Kuwait"
    ],
    "Latin America": ["Brazil", "Mexico", "Chile", "Colombia", "Peru", "Argentina"]
}

# Sample global IPO companies for testing
GLOBAL_IPO_COMPANIES = {
    # Asia Pacific
    "Japan": [
        {"ticker": "7974.T", "name": "Nintendo Co Ltd", "sector": "Communication Services"},
        {"ticker": "6758.T", "name": "Sony Group Corp", "sector": "Consumer Cyclical"},
        {"ticker": "9984.T", "name": "SoftBank Group Corp", "sector": "Technology"},
        {"ticker": "7203.T", "name": "Toyota Motor Corp", "sector": "Consumer Cyclical"},
        {"ticker": "6861.T", "name": "Keyence Corp", "sector": "Technology"}
    ],
    "China": [
        {"ticker": "BABA", "name": "Alibaba Group Holding Ltd", "sector": "Consumer Cyclical"},
        {"ticker": "JD", "name": "JD.com Inc", "sector": "Consumer Cyclical"},
        {"ticker": "BIDU", "name": "Baidu Inc", "sector": "Communication Services"},
        {"ticker": "NIO", "name": "NIO Inc", "sector": "Consumer Cyclical"},
        {"ticker": "XPEV", "name": "XPeng Inc", "sector": "Consumer Cyclical"}
    ],
    "Hong Kong": [
        {"ticker": "0700.HK", "name": "Tencent Holdings Ltd", "sector": "Communication Services"},
        {"ticker": "0941.HK", "name": "China Mobile Ltd", "sector": "Communication Services"},
        {"ticker": "0005.HK", "name": "HSBC Holdings PLC", "sector": "Financial Services"},
        {"ticker": "1299.HK", "name": "AIA Group Ltd", "sector": "Financial Services"},
        {"ticker": "3690.HK", "name": "Meituan", "sector": "Consumer Cyclical"}
    ],
    "South Korea": [
        {"ticker": "005930.KS", "name": "Samsung Electronics Co Ltd", "sector": "Technology"},
        {"ticker": "000660.KS", "name": "SK Hynix Inc", "sector": "Technology"},
        {"ticker": "035420.KS", "name": "NAVER Corp", "sector": "Communication Services"},
        {"ticker": "207940.KS", "name": "Samsung Biologics Co Ltd", "sector": "Healthcare"},
        {"ticker": "373220.KS", "name": "LG Energy Solution Ltd", "sector": "Industrials"}
    ],
    "Singapore": [
        {"ticker": "D05.SI", "name": "DBS Group Holdings Ltd", "sector": "Financial Services"},
        {"ticker": "O39.SI", "name": "Oversea-Chinese Banking Corp", "sector": "Financial Services"},
        {"ticker": "U11.SI", "name": "United Overseas Bank Ltd", "sector": "Financial Services"},
        {"ticker": "C6L.SI", "name": "Singapore Airlines Ltd", "sector": "Industrials"},
        {"ticker": "S68.SI", "name": "Singapore Exchange Ltd", "sector": "Financial Services"}
    ],
    "Australia": [
        {"ticker": "CBA.AX", "name": "Commonwealth Bank of Australia", "sector": "Financial Services"},
        {"ticker": "BHP.AX", "name": "BHP Group Ltd", "sector": "Basic Materials"},
        {"ticker": "CSL.AX", "name": "CSL Ltd", "sector": "Healthcare"},
        {"ticker": "WBC.AX", "name": "Westpac Banking Corp", "sector": "Financial Services"},
        {"ticker": "ANZ.AX", "name": "Australia and New Zealand Banking Group", "sector": "Financial Services"}
    ],
    "India": [
        {"ticker": "RELIANCE.NS", "name": "Reliance Industries Ltd", "sector": "Energy"},
        {"ticker": "TCS.NS", "name": "Tata Consultancy Services Ltd", "sector": "Technology"},
        {"ticker": "INFY.NS", "name": "Infosys Ltd", "sector": "Technology"},
        {"ticker": "HDFCBANK.NS", "name": "HDFC Bank Ltd", "sector": "Financial Services"},
        {"ticker": "ICICIBANK.NS", "name": "ICICI Bank Ltd", "sector": "Financial Services"}
    ],
    # Middle East & Africa
    "Saudi Arabia": [
        {"ticker": "2222.SR", "name": "Saudi Aramco", "sector": "Energy"},
        {"ticker": "1120.SR", "name": "Al Rajhi Bank", "sector": "Financial Services"},
        {"ticker": "2030.SR", "name": "Saudi Basic Industries Corp", "sector": "Basic Materials"},
        {"ticker": "1180.SR", "name": "Al Ahli Bank", "sector": "Financial Services"},
        {"ticker": "4030.SR", "name": "Riyad Bank", "sector": "Financial Services"}
    ],
    "UAE": [
        {"ticker": "ADCB.AD", "name": "Abu Dhabi Commercial Bank", "sector": "Financial Services"},
        {"ticker": "ENBD.DU", "name": "Emirates NBD Bank", "sector": "Financial Services"},
        {"ticker": "ADNOC.AD", "name": "ADNOC Drilling Co", "sector": "Energy"},
        {"ticker": "DFM.DU", "name": "Dubai Financial Market", "sector": "Financial Services"},
        {"ticker": "EMAAR.DU", "name": "Emaar Properties", "sector": "Real Estate"}
    ],
    "South Africa": [
        {"ticker": "NPN.JO", "name": "Naspers Ltd", "sector": "Communication Services"},
        {"ticker": "PRX.JO", "name": "Prosus NV", "sector": "Technology"},
        {"ticker": "SBK.JO", "name": "Standard Bank Group Ltd", "sector": "Financial Services"},
        {"ticker": "FSR.JO", "name": "FirstRand Ltd", "sector": "Financial Services"},
        {"ticker": "AGL.JO", "name": "Anglo American PLC", "sector": "Basic Materials"}
    ],
    # Latin America
    "Brazil": [
        {"ticker": "VALE3.SA", "name": "Vale SA", "sector": "Basic Materials"},
        {"ticker": "PETR4.SA", "name": "Petrobras", "sector": "Energy"},
        {"ticker": "ITUB4.SA", "name": "Itau Unibanco Holding SA", "sector": "Financial Services"},
        {"ticker": "BBDC4.SA", "name": "Banco Bradesco SA", "sector": "Financial Services"},
        {"ticker": "ABEV3.SA", "name": "Ambev SA", "sector": "Consumer Defensive"}
    ],
    "Mexico": [
        {"ticker": "AMXL.MX", "name": "America Movil SAB de CV", "sector": "Communication Services"},
        {"ticker": "WALMEX.MX", "name": "Wal-Mart de Mexico SAB de CV", "sector": "Consumer Defensive"},
        {"ticker": "FEMSA.MX", "name": "Fomento Economico Mexicano SAB de CV", "sector": "Consumer Defensive"},
        {"ticker": "GFNORTEO.MX", "name": "Grupo Financiero Banorte SAB de CV", "sector": "Financial Services"},
        {"ticker": "CEMEXCPO.MX", "name": "Cemex SAB de CV", "sector": "Basic Materials"}
    ]
}

def get_country_from_exchange(exchange):
    """Get country from exchange code"""
    return GLOBAL_EXCHANGE_MAPPING.get(exchange, "Unknown")

def get_region_from_country(country):
    """Get region from country name"""
    for region, countries in REGIONAL_GROUPS.items():
        if country in countries:
            return region
    return "Other"

def get_all_countries():
    """Get list of all supported countries"""
    return sorted(list(set(GLOBAL_EXCHANGE_MAPPING.values())))

def get_exchanges_by_country(country):
    """Get list of exchanges for a specific country"""
    return [exchange for exchange, ctry in GLOBAL_EXCHANGE_MAPPING.items() if ctry == country]

def get_sample_companies_by_country(country, limit=5):
    """Get sample companies for a specific country"""
    return GLOBAL_IPO_COMPANIES.get(country, [])[:limit]

def get_all_sample_companies():
    """Get all sample companies across all countries"""
    all_companies = []
    for country, companies in GLOBAL_IPO_COMPANIES.items():
        for company in companies:
            company_data = company.copy()
            company_data['country'] = country
            company_data['region'] = get_region_from_country(country)
            all_companies.append(company_data)
    return all_companies

logger.info(f"Global markets utility loaded with {len(GLOBAL_EXCHANGE_MAPPING)} exchanges across {len(get_all_countries())} countries")
