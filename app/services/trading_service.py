"""Service for trading data operations"""
import logging
import pandas as pd
import numpy as np
from datetime import date, datetime
from sqlalchemy import text
from app.db.database import get_db_engine
from app.core.config import settings

logger = logging.getLogger(__name__)


# Helper functions for options calculations
def is_otm(stock_price: float, strike_price: float, option_type: str) -> bool:
    """
    Determine if option is Out of The Money (OTM)
    
    Args:
        stock_price: Current stock price
        strike_price: Option strike price
        option_type: 'C' for call, 'P' for put
    
    Returns:
        True if OTM, False otherwise
    """
    if option_type == 'C':
        return stock_price < strike_price
    elif option_type == 'P':
        return stock_price > strike_price
    return False


def adj_value(stock_price: float, strike_price: float, option_type: str, option_price: float) -> float:
    """
    Calculate adjusted option price based on intrinsic value
    
    Args:
        stock_price: Current stock price
        strike_price: Option strike price
        option_type: 'C' for call, 'P' for put
        option_price: Current option price
    
    Returns:
        Adjusted option price
    """
    if option_type == 'C':
        intrinsic = max(stock_price - strike_price, 0)
    elif option_type == 'P':
        intrinsic = max(strike_price - stock_price, 0)
    else:
        return option_price
    
    # Return max of intrinsic value and option price
    return max(intrinsic, option_price)


def get_stop_percent(symbol: str, stop_price: float, last_price: float, option_type: str) -> float:
    """
    Calculate stop loss percentage
    
    Args:
        symbol: Stock/ETF symbol
        stop_price: Stop loss price
        last_price: Last traded price
        option_type: 'C' for call, 'P' for put
    
    Returns:
        Stop loss percentage
    """
    if last_price is None or last_price == 0:
        return np.nan
    
    if stop_price is None or stop_price == 0:
        return np.nan
    
    stop_pct = round((stop_price / last_price - 1) * 100, 2)
    return stop_pct


def convert_dataframe_for_json(df: pd.DataFrame) -> list[dict]:
    """
    Convert DataFrame to JSON-serializable list of dictionaries
    Handles datetime.date, numpy.nan, numpy.inf, and other non-JSON-serializable types
    
    Args:
        df: DataFrame to convert
    
    Returns:
        List of dictionaries with JSON-serializable values
    """
    records = df.to_dict(orient='records')
    
    for record in records:
        for key, value in record.items():
            # Skip if value is None
            if value is None:
                continue
            
            # Convert datetime.date to ISO string
            if isinstance(value, date) and not isinstance(value, datetime):
                record[key] = value.isoformat()
            # Convert datetime to ISO string
            elif isinstance(value, datetime):
                record[key] = value.isoformat()
            # Convert NaN to None (which becomes null in JSON)
            elif isinstance(value, float):
                if np.isnan(value):
                    record[key] = None
                elif np.isinf(value):
                    record[key] = None
            # Convert numpy types to Python native types
            elif isinstance(value, np.generic):
                if isinstance(value, np.floating):
                    if np.isnan(value) or np.isinf(value):
                        record[key] = None
                    else:
                        record[key] = float(value)
                else:
                    record[key] = value.item()
    
    return records



class TradingService:
    """Service for handling trading data queries"""
    
    @staticmethod
    def get_etf_options() -> pd.DataFrame:
        """
        Fetch ETF options trading data with calculated fields
        Executes stored procedure: Trading.sp_etf_trades_v2
        
        Calculates:
        - Stop%: Stop loss percentage (only when L_Strike is null)
        - OPrice: Entry price (prioritizes O_bid if > 0, falls back to O_last)
        - adjOPrice: Adjusted price considering intrinsic value for OTM options (uses H_Strike)
        - Reward%: Reward percentage (OPrice / H_Strike * 100)
        - AdjReward%: Adjusted reward percentage (adjOPrice / H_Strike * 100)
        
        Returns:
            DataFrame with ETF options data and calculated fields
        """
        try:
            engine = get_db_engine()
            query = "CALL Trading.sp_etf_trades_v2;"
            
            logger.info("Fetching ETF options data...")
            df = pd.read_sql_query(query, con=engine)
            logger.info(f"Fetched {len(df)} ETF options records")
            
            # Convert date columns to string
            if 'Date' in df.columns:
                df['Date'] = df['Date'].astype(str)
            if 'Expiration' in df.columns:
                df['Expiration'] = df['Expiration'].astype(str)
            
            # Initialize calculation columns
            df['Stop%'] = np.nan
            df['OPrice'] = np.nan
            df['Target%'] = np.nan
            df['Reward%'] = np.nan
            df['adjOPrice'] = np.nan
            df['AdjReward%'] = np.nan
            
            # Calculate OPrice: Use O_bid if > 0, else use O_last
            if 'O_bid' in df.columns and 'O_last' in df.columns:
                df['OPrice'] = df.apply(
                    lambda row: row['O_bid'] 
                    if (pd.notna(row['O_bid']) and row['O_bid'] > 0.0) 
                    else row['O_last'],
                    axis=1
                )
            elif 'O_last' in df.columns:
                df['OPrice'] = df['O_last']
            
            # Calculate Stop% for each row (only when L_Strike is null)
            for ix, row in df.iterrows():
                # Only calculate Stop% when L_Strike is null
                if pd.isnull(row.get('L_Strike')):
                    if all(col in row.index for col in ['Symbol', 'Stop', 'Last', 'PnC']):
                        # Ensure Last is numeric
                        last_val = row['Last'] if isinstance(row['Last'], (int, float, complex)) else 0.0
                        df.at[ix, 'Stop%'] = get_stop_percent(
                            row['Symbol'],
                            row['Stop'],
                            last_val,
                            row['PnC']
                        )
            
            # Calculate Target%: (Target / Last - 1) * 100
            if 'Target' in df.columns and 'Last' in df.columns:
                df['Target%'] = df.apply(
                    lambda row: round((row['Target'] / row['Last'] - 1) * 100, 2)
                    if (pd.notna(row['Target']) and pd.notna(row['Last']) and row['Last'] != 0)
                    else np.nan,
                    axis=1
                )
            
            # Calculate adjOPrice: Adjusted value for OTM options (uses H_Strike)
            if all(col in df.columns for col in ['Last', 'H_Strike', 'PnC', 'OPrice']):
                df['adjOPrice'] = df.apply(
                    lambda row: adj_value(row['Last'], row['H_Strike'], row['PnC'], row['OPrice'])
                    if is_otm(row['Last'], row['H_Strike'], row['PnC'])
                    else row['OPrice'],
                    axis=1
                )
            
            # Ensure OPrice is float
            if 'OPrice' in df.columns:
                df['OPrice'] = df['OPrice'].astype(float)
            
            # Calculate Reward%: OPrice / H_Strike * 100
            if 'OPrice' in df.columns and 'H_Strike' in df.columns:
                df['Reward%'] = round(df['OPrice'] / df['H_Strike'] * 100.0, 2)
            
            # Calculate AdjReward%: adjOPrice / H_Strike * 100
            if 'adjOPrice' in df.columns and 'H_Strike' in df.columns:
                df['AdjReward%'] = round(df['adjOPrice'] / df['H_Strike'] * 100.0, 2)
            
            logger.info(f"Calculated metrics for {len(df)} records")
            
            return df
        except Exception as e:
            logger.error(f"Error fetching ETF options: {str(e)}")
            raise
    
    @staticmethod
    def get_stock_options() -> pd.DataFrame:
        """
        Fetch stock options trading data with calculated fields
        Executes stored procedure: Trading.sp_stock_trades_V3
        
        Calculates:
        - Stop%: Stop loss percentage
        - OPrice: Entry price (prioritizes O_bid, falls back to O_last)
        - adjOPrice: Adjusted price considering intrinsic value for OTM options
        - Reward%: Reward percentage (OPrice / Strike * 100)
        - AdjReward%: Adjusted reward percentage (adjOPrice / Strike * 100)
        
        Returns:
            DataFrame with stock options data and calculated fields
        """
        try:
            engine = get_db_engine()
            query = "CALL Trading.sp_stock_trades_V3;"
            
            logger.info("Fetching stock options data...")
            df = pd.read_sql_query(query, con=engine)
            logger.info(f"Fetched {len(df)} stock options records")
            
            # Convert date columns to string
            if 'Date' in df.columns:
                df['Date'] = df['Date'].astype(str)
            if 'Expiration' in df.columns:
                df['Expiration'] = df['Expiration'].astype(str)
            
            # Initialize calculation columns
            df['Stop%'] = np.nan
            df['OPrice'] = np.nan
            df['Target%'] = np.nan
            df['Reward%'] = np.nan
            df['adjOPrice'] = np.nan
            df['AdjReward%'] = np.nan
            
            # Calculate OPrice: Use O_bid if available and > 0, else use O_last
            if 'O_bid' in df.columns and 'O_last' in df.columns:
                df['OPrice'] = df.apply(
                    lambda row: row['O_bid'] 
                    if (pd.notna(row['O_bid']) and row['O_bid'] > 0.0) 
                    else row['O_last'],
                    axis=1
                )
            elif 'O_last' in df.columns:
                df['OPrice'] = df['O_last']
            
            # Calculate Stop% for each row
            for ix, row in df.iterrows():
                if all(col in row.index for col in ['Symbol', 'Stop', 'Last', 'PnC']):
                    df.at[ix, 'Stop%'] = get_stop_percent(
                        row['Symbol'],
                        row['Stop'],
                        row['Last'],
                        row['PnC']
                    )
            
            # Calculate Target%: (Target / Last - 1) * 100
            if 'Target' in df.columns and 'Last' in df.columns:
                df['Target%'] = df.apply(
                    lambda row: round((row['Target'] / row['Last'] - 1) * 100, 2)
                    if (pd.notna(row['Target']) and pd.notna(row['Last']) and row['Last'] != 0)
                    else np.nan,
                    axis=1
                )
            
            # Calculate adjOPrice: Adjusted value for OTM options
            if all(col in df.columns for col in ['Last', 'Strike', 'PnC', 'OPrice']):
                df['adjOPrice'] = df.apply(
                    lambda row: adj_value(row['Last'], row['Strike'], row['PnC'], row['OPrice'])
                    if is_otm(row['Last'], row['Strike'], row['PnC'])
                    else row['OPrice'],
                    axis=1
                )
            
            # Calculate Reward%: OPrice / Strike * 100
            if 'OPrice' in df.columns and 'Strike' in df.columns:
                df['Reward%'] = round(df['OPrice'] / df['Strike'] * 100, 2)
            
            # Calculate AdjReward%: adjOPrice / Strike * 100
            if 'adjOPrice' in df.columns and 'Strike' in df.columns:
                df['AdjReward%'] = round(df['adjOPrice'] / df['Strike'] * 100, 2)
            
            logger.info(f"Calculated metrics for {len(df)} records")
            
            return df
        except Exception as e:
            logger.error(f"Error fetching stock options: {str(e)}")
            raise
    
    @staticmethod
    def get_max_date(table_name: str, symbol: str = None) -> str:
        """
        Get the maximum date from a table
        
        Args:
            table_name: Name of the table to query
            symbol: Optional symbol filter
        
        Returns:
            Maximum date as string
        """
        try:
            engine = get_db_engine()
            
            if symbol:
                query = f"SELECT MAX(Date) as max_date FROM {settings.DBMKTDATA}.{table_name} WHERE symbol = '{symbol}'"
            else:
                query = f"SELECT MAX(Date) as max_date FROM {settings.DBMKTDATA}.{table_name}"
            
            result = pd.read_sql_query(query, con=engine)
            max_date = result['max_date'].iloc[0]
            
            logger.info(f"Max date for {table_name}: {max_date}")
            return str(max_date)
        except Exception as e:
            logger.error(f"Error getting max date: {str(e)}")
            raise
    
    @staticmethod
    def execute_custom_query(query: str) -> pd.DataFrame:
        """
        Execute a custom SQL query
        
        Args:
            query: SQL query string
        
        Returns:
            Query results as DataFrame
        """
        try:
            engine = get_db_engine()
            logger.info(f"Executing custom query: {query}")
            
            df = pd.read_sql_query(query, con=engine)
            logger.info(f"Query returned {len(df)} records")
            
            return df
        except Exception as e:
            logger.error(f"Error executing custom query: {str(e)}")
            raise
