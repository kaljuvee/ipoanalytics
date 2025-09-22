"""
Regional Mapping Utility for IPO Analytics
Maps countries and exchanges to global regions (APAC, EMEA, Americas)
"""

# Regional mapping for countries
REGIONAL_MAPPING = {
    # Americas
    "United States": "Americas",
    "Canada": "Americas", 
    "Brazil": "Americas",
    "Mexico": "Americas",
    "Argentina": "Americas",
    "Chile": "Americas",
    "Colombia": "Americas",
    "Peru": "Americas",
    
    # EMEA (Europe, Middle East, Africa)
    "United Kingdom": "EMEA",
    "Germany": "EMEA",
    "France": "EMEA",
    "Netherlands": "EMEA",
    "Italy": "EMEA",
    "Spain": "EMEA",
    "Switzerland": "EMEA",
    "Sweden": "EMEA",
    "Norway": "EMEA",
    "Denmark": "EMEA",
    "Finland": "EMEA",
    "Poland": "EMEA",
    "Hungary": "EMEA",
    "Czech Republic": "EMEA",
    "Greece": "EMEA",
    "Portugal": "EMEA",
    "Belgium": "EMEA",
    "Austria": "EMEA",
    "Estonia": "EMEA",
    "Latvia": "EMEA",
    "Lithuania": "EMEA",
    "Ireland": "EMEA",
    "Luxembourg": "EMEA",
    "Russia": "EMEA",
    "Turkey": "EMEA",
    "Israel": "EMEA",
    "South Africa": "EMEA",
    "UAE": "EMEA",
    "Saudi Arabia": "EMEA",
    "Qatar": "EMEA",
    "Kuwait": "EMEA",
    "Egypt": "EMEA",
    "Morocco": "EMEA",
    "Nigeria": "EMEA",
    "Kenya": "EMEA",
    
    # APAC (Asia-Pacific)
    "China": "APAC",
    "Japan": "APAC",
    "South Korea": "APAC",
    "India": "APAC",
    "Singapore": "APAC",
    "Hong Kong": "APAC",
    "Taiwan": "APAC",
    "Australia": "APAC",
    "New Zealand": "APAC",
    "Thailand": "APAC",
    "Malaysia": "APAC",
    "Indonesia": "APAC",
    "Philippines": "APAC",
    "Vietnam": "APAC",
    "Bangladesh": "APAC",
    "Pakistan": "APAC",
    "Sri Lanka": "APAC",
    "Myanmar": "APAC",
    "Cambodia": "APAC",
    "Laos": "APAC",
    "Mongolia": "APAC",
    "Kazakhstan": "APAC",
    "Uzbekistan": "APAC",
}

# Exchange to country mapping (for cases where we have exchange but need country)
EXCHANGE_TO_COUNTRY = {
    # US Exchanges
    "NASDAQ": "United States",
    "NYSE": "United States", 
    "AMEX": "United States",
    "NYSEARCA": "United States",
    "BATS": "United States",
    
    # UK Exchanges
    "LSE": "United Kingdom",
    "AIM": "United Kingdom",
    "LON": "United Kingdom",
    
    # German Exchanges
    "XETRA": "Germany",
    "FSE": "Germany",
    "FRA": "Germany",
    "BER": "Germany",
    "MUN": "Germany",
    "STU": "Germany",
    "HAM": "Germany",
    "DUS": "Germany",
    
    # French Exchanges
    "EPA": "France",
    "EURONEXT": "France",
    "PAR": "France",
    
    # Other European Exchanges
    "AMS": "Netherlands",  # Amsterdam
    "BIT": "Italy",       # Borsa Italiana
    "MIL": "Italy",       # Milan
    "BME": "Spain",       # Bolsas y Mercados Españoles
    "MCE": "Spain",       # Madrid
    "MAD": "Spain",       # Madrid
    "SIX": "Switzerland", # SIX Swiss Exchange
    "VTX": "Switzerland", # SIX Swiss Exchange
    "STO": "Sweden",      # Stockholm
    "HEL": "Finland",     # Helsinki
    "CPH": "Denmark",     # Copenhagen
    "OSL": "Norway",      # Oslo
    "WSE": "Poland",      # Warsaw
    "BUD": "Hungary",     # Budapest
    "PRA": "Czech Republic", # Prague
    "ATH": "Greece",      # Athens
    "LIS": "Portugal",    # Lisbon
    "BRU": "Belgium",     # Brussels
    "VIE": "Austria",     # Vienna
    "TAL": "Estonia",     # Tallinn
    "RIG": "Latvia",      # Riga
    "VSE": "Lithuania",   # Vilnius
    
    # APAC Exchanges
    "SSE": "China",       # Shanghai
    "SZSE": "China",      # Shenzhen
    "HKEX": "Hong Kong",  # Hong Kong
    "HKG": "Hong Kong",   # Hong Kong
    "TSE": "Japan",       # Tokyo
    "JPX": "Japan",       # Japan Exchange Group
    "KRX": "South Korea", # Korea Exchange
    "KOSPI": "South Korea", # KOSPI
    "KOSDAQ": "South Korea", # KOSDAQ
    "BSE": "India",       # Bombay Stock Exchange
    "NSE": "India",       # National Stock Exchange of India
    "SGX": "Singapore",   # Singapore Exchange
    "TWSE": "Taiwan",     # Taiwan Stock Exchange
    "ASX": "Australia",   # Australian Securities Exchange
    "NZX": "New Zealand", # New Zealand Exchange
    "SET": "Thailand",    # Stock Exchange of Thailand
    "KLSE": "Malaysia",   # Kuala Lumpur Stock Exchange
    "IDX": "Indonesia",   # Indonesia Stock Exchange
    "PSE": "Philippines", # Philippine Stock Exchange
    "HOSE": "Vietnam",    # Ho Chi Minh Stock Exchange
    "HNX": "Vietnam",     # Hanoi Stock Exchange
    
    # Americas (non-US)
    "TSX": "Canada",      # Toronto Stock Exchange
    "TSXV": "Canada",     # TSX Venture Exchange
    "B3": "Brazil",       # B3 (Brasil, Bolsa, Balcão)
    "BOVESPA": "Brazil",  # Bovespa
    "BMV": "Mexico",      # Mexican Stock Exchange
    "BCBA": "Argentina",  # Buenos Aires Stock Exchange
    "BCS": "Chile",       # Santiago Stock Exchange
    "BVC": "Colombia",    # Colombian Stock Exchange
    "BVL": "Peru",        # Lima Stock Exchange
}

def get_region_from_country(country: str) -> str:
    """
    Get the region for a given country
    
    Args:
        country (str): Country name
        
    Returns:
        str: Region name (APAC, EMEA, Americas) or 'Other' if not found
    """
    return REGIONAL_MAPPING.get(country, "Other")

def get_country_from_exchange(exchange: str) -> str:
    """
    Get the country for a given exchange
    
    Args:
        exchange (str): Exchange code/name
        
    Returns:
        str: Country name or 'Unknown' if not found
    """
    return EXCHANGE_TO_COUNTRY.get(exchange, "Unknown")

def get_region_from_exchange(exchange: str) -> str:
    """
    Get the region for a given exchange
    
    Args:
        exchange (str): Exchange code/name
        
    Returns:
        str: Region name (APAC, EMEA, Americas) or 'Other' if not found
    """
    country = get_country_from_exchange(exchange)
    return get_region_from_country(country)

def get_countries_by_region(region: str) -> list:
    """
    Get all countries in a specific region
    
    Args:
        region (str): Region name (APAC, EMEA, Americas)
        
    Returns:
        list: List of country names in the region
    """
    return [country for country, reg in REGIONAL_MAPPING.items() if reg == region]

def get_exchanges_by_region(region: str) -> list:
    """
    Get all exchanges in a specific region
    
    Args:
        region (str): Region name (APAC, EMEA, Americas)
        
    Returns:
        list: List of exchange codes in the region
    """
    region_countries = get_countries_by_region(region)
    exchanges = []
    
    for exchange, country in EXCHANGE_TO_COUNTRY.items():
        if country in region_countries:
            exchanges.append(exchange)
    
    return exchanges

def add_regional_data(df):
    """
    Add region and country columns to a DataFrame with exchange data
    
    Args:
        df: DataFrame with 'exchange' column
        
    Returns:
        DataFrame with added 'country' and 'region' columns
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Add country if not present
    if 'country' not in df.columns:
        df['country'] = df['exchange'].apply(get_country_from_exchange)
    
    # Add region
    df['region'] = df['country'].apply(get_region_from_country)
    
    return df

def get_regional_summary():
    """
    Get a summary of all regions and their countries/exchanges
    
    Returns:
        dict: Summary of regions with countries and exchanges
    """
    summary = {}
    
    for region in ["Americas", "EMEA", "APAC"]:
        countries = get_countries_by_region(region)
        exchanges = get_exchanges_by_region(region)
        
        summary[region] = {
            "countries": sorted(countries),
            "exchanges": sorted(exchanges),
            "country_count": len(countries),
            "exchange_count": len(exchanges)
        }
    
    return summary

# Regional display names and emojis for UI
REGION_DISPLAY = {
    "Americas": "🌎 Americas",
    "EMEA": "🌍 EMEA", 
    "APAC": "🌏 APAC",
    "Other": "🌐 Other"
}

def get_region_display_name(region: str) -> str:
    """Get display name with emoji for a region"""
    return REGION_DISPLAY.get(region, f"🌐 {region}")

if __name__ == "__main__":
    # Test the regional mapping
    print("Regional Mapping Test")
    print("=" * 50)
    
    # Test some exchanges
    test_exchanges = ["NASDAQ", "LSE", "TSE", "SSE", "B3"]
    for exchange in test_exchanges:
        country = get_country_from_exchange(exchange)
        region = get_region_from_exchange(exchange)
        print(f"{exchange} -> {country} -> {region}")
    
    print("\nRegional Summary:")
    summary = get_regional_summary()
    for region, data in summary.items():
        print(f"\n{get_region_display_name(region)}:")
        print(f"  Countries: {data['country_count']}")
        print(f"  Exchanges: {data['exchange_count']}")
        print(f"  Sample countries: {', '.join(data['countries'][:5])}")
        print(f"  Sample exchanges: {', '.join(data['exchanges'][:5])}")
