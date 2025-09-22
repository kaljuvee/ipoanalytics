#!/usr/bin/env python3
"""
Performance calculation utilities for IPO Analytics
"""

from datetime import datetime, date
import pandas as pd
import numpy as np

def calculate_annualized_return(total_return, ipo_date_str, current_date=None):
    """
    Calculate annualized return based on total return and time since IPO
    
    Args:
        total_return (float): Total return since IPO (e.g., 0.15 for 15%)
        ipo_date_str (str): IPO date in ISO format (YYYY-MM-DD)
        current_date (datetime, optional): Current date for calculation. Defaults to today.
    
    Returns:
        float: Annualized return
    """
    if current_date is None:
        current_date = datetime.now()
    
    try:
        # Parse IPO date
        if isinstance(ipo_date_str, str):
            ipo_date = datetime.fromisoformat(ipo_date_str.replace('Z', '+00:00'))
        else:
            ipo_date = ipo_date_str
        
        # Calculate years since IPO
        days_since_ipo = (current_date - ipo_date).days
        years_since_ipo = days_since_ipo / 365.25
        
        # Avoid division by zero or negative time
        if years_since_ipo <= 0:
            return 0.0
        
        # Calculate annualized return: (1 + total_return)^(1/years) - 1
        annualized_return = (1 + total_return) ** (1 / years_since_ipo) - 1
        
        return annualized_return
        
    except (ValueError, TypeError, AttributeError):
        return 0.0

def format_annualized_return(annualized_return):
    """
    Format annualized return as percentage string
    
    Args:
        annualized_return (float): Annualized return as decimal
    
    Returns:
        str: Formatted percentage string
    """
    if pd.isna(annualized_return) or annualized_return == 0:
        return "0.00%"
    
    return f"{annualized_return:.2%}"

def add_performance_metrics(df):
    """
    Add performance metrics to dataframe including annualized returns
    
    Args:
        df (pd.DataFrame): DataFrame with IPO data
    
    Returns:
        pd.DataFrame: DataFrame with added performance metrics
    """
    df = df.copy()
    
    # Calculate annualized returns
    df['annualized_return'] = df.apply(
        lambda row: calculate_annualized_return(
            row['price_change_since_ipo'], 
            row['ipo_date']
        ), 
        axis=1
    )
    
    return df

def format_ipo_date(ipo_date_str):
    """
    Format IPO date for display
    
    Args:
        ipo_date_str (str): IPO date in ISO format
    
    Returns:
        str: Formatted date string
    """
    try:
        if isinstance(ipo_date_str, str):
            ipo_date = datetime.fromisoformat(ipo_date_str.replace('Z', '+00:00'))
        else:
            ipo_date = ipo_date_str
        
        return ipo_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError, AttributeError):
        return "Unknown"
