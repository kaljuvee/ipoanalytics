"""
Enhanced Regional Mapping Utility for IPO Analytics
Maps countries and exchanges to global regions (APAC, EMEA, Americas)
Includes comprehensive coverage for all major global markets
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
    "Uruguay": "Americas",
    "Venezuela": "Americas",
    "Ecuador": "Americas",
    "Bolivia": "Americas",
    "Paraguay": "Americas",
    "Costa Rica": "Americas",
    "Panama": "Americas",
    "Guatemala": "Americas",
    "Honduras": "Americas",
    "Nicaragua": "Americas",
    "El Salvador": "Americas",
    "Jamaica": "Americas",
    "Trinidad and Tobago": "Americas",
    "Barbados": "Americas",
    "Bahamas": "Americas",
    
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
    "Ghana": "EMEA",
    "Tunisia": "EMEA",
    "Algeria": "EMEA",
    "Jordan": "EMEA",
    "Lebanon": "EMEA",
    "Oman": "EMEA",
    "Bahrain": "EMEA",
    "Cyprus": "EMEA",
    "Malta": "EMEA",
    "Iceland": "EMEA",
    "Croatia": "EMEA",
    "Slovenia": "EMEA",
    "Slovakia": "EMEA",
    "Romania": "EMEA",
    "Bulgaria": "EMEA",
    "Serbia": "EMEA",
    "Ukraine": "EMEA",
    "Belarus": "EMEA",
    
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
    "Kyrgyzstan": "APAC",
    "Tajikistan": "APAC",
    "Turkmenistan": "APAC",
    "Nepal": "APAC",
    "Bhutan": "APAC",
    "Maldives": "APAC",
    "Brunei": "APAC",
    "Papua New Guinea": "APAC",
    "Fiji": "APAC",
    "Solomon Islands": "APAC",
    "Vanuatu": "APAC",
    "Samoa": "APAC",
    "Tonga": "APAC",
    "Palau": "APAC",
    "Marshall Islands": "APAC",
    "Micronesia": "APAC",
    "Nauru": "APAC",
    "Kiribati": "APAC",
    "Tuvalu": "APAC",
}

# Enhanced Exchange to country mapping
EXCHANGE_TO_COUNTRY = {
    # Americas - US Exchanges
    "NASDAQ": "United States",
    "NYSE": "United States", 
    "AMEX": "United States",
    "NYSEARCA": "United States",
    "BATS": "United States",
    "CBOE": "United States",
    "IEX": "United States",
    "ARCA": "United States",
    
    # Americas - Canadian Exchanges
    "TSX": "Canada",
    "TSXV": "Canada",
    "CSE": "Canada",
    "NEO": "Canada",
    
    # Americas - Latin American Exchanges
    "B3": "Brazil",
    "BOVESPA": "Brazil",
    "BMV": "Mexico",
    "BIVA": "Mexico",
    "BCBA": "Argentina",
    "BYMA": "Argentina",
    "BCS": "Chile",
    "BVC": "Colombia",
    "BVL": "Peru",
    "MVDX": "Uruguay",
    "BVQ": "Ecuador",
    "BVPASA": "Panama",
    "BVN": "Nicaragua",
    "BVCR": "Costa Rica",
    "JSE_JM": "Jamaica",
    "TTSE": "Trinidad and Tobago",
    
    # EMEA - UK Exchanges
    "LSE": "United Kingdom",
    "AIM": "United Kingdom",
    "LON": "United Kingdom",
    "AQSE": "United Kingdom",
    "L": "United Kingdom",  # London Stock Exchange suffix
    
    # EMEA - German Exchanges
    "XETRA": "Germany",
    "FSE": "Germany",
    "FRA": "Germany",
    "BER": "Germany",
    "MUN": "Germany",
    "STU": "Germany",
    "HAM": "Germany",
    "DUS": "Germany",
    "TRADEGATE": "Germany",
    "DE": "Germany",  # German exchange suffix
    
    # EMEA - French Exchanges
    "EPA": "France",
    "EURONEXT": "France",
    "PAR": "France",
    "ALTERNEXT": "France",
    "PA": "France",  # Paris exchange suffix
    
    # EMEA - Other European Exchanges
    "AMS": "Netherlands",
    "AS": "Netherlands",  # Amsterdam exchange suffix
    "BIT": "Italy",
    "MIL": "Italy",
    "MI": "Italy",  # Milan exchange suffix
    "BME": "Spain",
    "MCE": "Spain",
    "MAD": "Spain",
    "MC": "Spain",  # Madrid exchange suffix
    "SIX": "Switzerland",
    "SW": "Switzerland",  # Swiss exchange suffix
    "VTX": "Switzerland",
    "STO": "Sweden",
    "ST": "Sweden",  # Stockholm exchange suffix
    "HEL": "Finland",
    "HE": "Finland",  # Helsinki exchange suffix
    "CPH": "Denmark",
    "CO": "Denmark",  # Copenhagen exchange suffix
    "OSL": "Norway",
    "OL": "Norway",  # Oslo exchange suffix
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
    "ISE": "Ireland",
    "LUX": "Luxembourg",
    "MOEX": "Russia",
    "BIST": "Turkey",
    "TASE": "Israel",
    "JSE": "South Africa",
    "DFM": "UAE",
    "ADX": "UAE",
    "TADAWUL": "Saudi Arabia",
    "QE": "Qatar",
    "KSE": "Kuwait",
    "EGX": "Egypt",
    "CSE": "Cyprus",
    "MSE": "Malta",
    "ICEX": "Iceland",
    "ZSE": "Croatia",
    "LJSE": "Slovenia",
    "BSSE": "Slovakia",
    "BVB": "Romania",
    "BSE_BG": "Bulgaria",
    "BELEX": "Serbia",
    
    # APAC - Chinese Exchanges
    "SSE": "China",
    "SZSE": "China",
    "BSE_CN": "China",
    "NEEQ": "China",
    
    # APAC - Hong Kong Exchanges
    "HKEX": "Hong Kong",
    "HKG": "Hong Kong",
    "GEM": "Hong Kong",
    
    # APAC - Japanese Exchanges
    "TSE": "Japan",
    "JPX": "Japan",
    "OSA": "Japan",
    "NSE_JP": "Japan",
    "FSE_JP": "Japan",
    "SSE_JP": "Japan",
    "MOTHERS": "Japan",
    "JASDAQ": "Japan",
    
    # APAC - Korean Exchanges
    "KRX": "South Korea",
    "KOSPI": "South Korea",
    "KOSDAQ": "South Korea",
    "KONEX": "South Korea",
    
    # APAC - Indian Exchanges
    "BSE": "India",
    "NSE": "India",
    "MSE": "India",
    "CSE_IN": "India",
    "USE": "India",
    "ASE": "India",
    "BSE_IN": "India",
    
    # APAC - Singapore Exchange
    "SGX": "Singapore",
    "CATALIST": "Singapore",
    
    # APAC - Taiwan Exchanges
    "TWSE": "Taiwan",
    "TPEx": "Taiwan",
    "GTSM": "Taiwan",
    
    # APAC - Australian Exchanges
    "ASX": "Australia",
    "NSX": "Australia",
    "SSX": "Australia",
    
    # APAC - New Zealand Exchange
    "NZX": "New Zealand",
    "NZAX": "New Zealand",
    
    # APAC - Southeast Asian Exchanges
    "SET": "Thailand",
    "MAI": "Thailand",
    "KLSE": "Malaysia",
    "ACE": "Malaysia",
    "LEAP": "Malaysia",
    "IDX": "Indonesia",
    "PSE": "Philippines",
    "HOSE": "Vietnam",
    "HNX": "Vietnam",
    "UPCOM": "Vietnam",
    "DSE": "Bangladesh",
    "CSE": "Bangladesh",
    "PSX": "Pakistan",
    "CSE_LK": "Sri Lanka",
    "YSX": "Myanmar",
    "CSX": "Cambodia",
    "LSX": "Laos",
    "MSE_MN": "Mongolia",
    "KASE": "Kazakhstan",
    "UzSE": "Uzbekistan",
    "KSE_KG": "Kyrgyzstan",
    "TSE_TJ": "Tajikistan",
    "BCSE": "Brunei",
    "PNGX": "Papua New Guinea",
    "SPX": "Fiji",
}

def get_region_from_country(country: str) -> str:
    """Get the region for a given country"""
    return REGIONAL_MAPPING.get(country, "Other")

def get_country_from_exchange(exchange: str) -> str:
    """Get the country for a given exchange"""
    return EXCHANGE_TO_COUNTRY.get(exchange, "Unknown")

def get_region_from_exchange(exchange: str) -> str:
    """Get the region for a given exchange"""
    country = get_country_from_exchange(exchange)
    return get_region_from_country(country)

def get_countries_by_region(region: str) -> list:
    """Get all countries in a specific region"""
    return [country for country, reg in REGIONAL_MAPPING.items() if reg == region]

def get_exchanges_by_region(region: str) -> list:
    """Get all exchanges in a specific region"""
    region_countries = get_countries_by_region(region)
    exchanges = []
    
    for exchange, country in EXCHANGE_TO_COUNTRY.items():
        if country in region_countries:
            exchanges.append(exchange)
    
    return exchanges

def add_regional_data(df):
    """Add region and country columns to a DataFrame with exchange data"""
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
    """Get a summary of all regions and their countries/exchanges"""
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
    # Test the enhanced regional mapping
    print("Enhanced Regional Mapping Test")
    print("=" * 50)
    
    # Test exchanges from all regions
    test_exchanges = ["NASDAQ", "TSX", "B3", "LSE", "XETRA", "TSE", "SSE", "HKEX", "ASX", "SGX"]
    for exchange in test_exchanges:
        country = get_country_from_exchange(exchange)
        region = get_region_from_exchange(exchange)
        print(f"{exchange} -> {country} -> {region}")
    
    print("\nEnhanced Regional Summary:")
    summary = get_regional_summary()
    for region, data in summary.items():
        print(f"\n{get_region_display_name(region)}:")
        print(f"  Countries: {data['country_count']}")
        print(f"  Exchanges: {data['exchange_count']}")
        print(f"  Sample countries: {', '.join(data['countries'][:8])}")
        print(f"  Sample exchanges: {', '.join(data['exchanges'][:8])}")
