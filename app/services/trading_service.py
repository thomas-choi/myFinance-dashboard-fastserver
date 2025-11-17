"""Service for trading data operations"""
import logging
import pandas as pd
import numpy as np
from datetime import date, datetime
from sqlalchemy import text
from app.db.database import get_db_engine
from app.core.config import settings

logger = logging.getLogger(__name__)


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
        Fetch ETF options trading data
        Executes stored procedure: Trading.sp_etf_trades_v2
        
        Returns:
            DataFrame with ETF options data
        """
        try:
            engine = get_db_engine()
            query = "CALL Trading.sp_etf_trades_v2;"
            
            logger.info("Fetching ETF options data...")
            df = pd.read_sql_query(query, con=engine)
            logger.info(f"Fetched {len(df)} ETF options records")
            
            return df
        except Exception as e:
            logger.error(f"Error fetching ETF options: {str(e)}")
            raise
    
    @staticmethod
    def get_stock_options() -> pd.DataFrame:
        """
        Fetch stock options trading data
        Executes stored procedure: Trading.sp_stock_trades_V3
        
        Returns:
            DataFrame with stock options data
        """
        try:
            engine = get_db_engine()
            query = "CALL Trading.sp_stock_trades_V3;"
            
            logger.info("Fetching stock options data...")
            df = pd.read_sql_query(query, con=engine)
            logger.info(f"Fetched {len(df)} stock options records")
            
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
