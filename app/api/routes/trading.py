"""API routes for trading data (options monitor)"""
import logging
from fastapi import APIRouter, HTTPException, Query
from app.services.trading_service import TradingService, convert_dataframe_for_json
from app.schemas.trading import OptionListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trading", tags=["trading"])


@router.get("/etf-options", response_model=OptionListResponse)
async def get_etf_options():
    """
    Get ETF options monitor data
    
    Executes stored procedure: Trading.sp_etf_trades_v2
    Returns latest table of ETF options with status and calculations
    """
    try:
        df = TradingService.get_etf_options()
        
        logger.debug(f"ETF options DataFrame shape: {df.shape}")
        # Convert DataFrame to JSON-serializable list
        options = convert_dataframe_for_json(df)
        logger.debug(f"ETF options converted to {len(options)} records")
        
        return OptionListResponse(
            data=options,
            count=len(options),
            type="ETF"
        )
    except Exception as e:
        logger.error(f"Error fetching ETF options: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching ETF options: {str(e)}"
        )


@router.get("/stock-options", response_model=OptionListResponse)
async def get_stock_options():
    """
    Get US stock options monitor data
    
    Executes stored procedure: Trading.sp_stock_trades_V3
    Returns latest table of stock options with status and calculations
    """
    try:
        df = TradingService.get_stock_options()
        
        # Convert DataFrame to JSON-serializable list
        options = convert_dataframe_for_json(df)
        
        return OptionListResponse(
            data=options,
            count=len(options),
            type="STK"
        )
    except Exception as e:
        logger.error(f"Error fetching stock options: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock options: {str(e)}"
        )


@router.get("/max-date/{table_name}")
async def get_max_date(
    table_name: str,
    symbol: str = Query(None, description="Optional symbol filter")
):
    """
    Get the maximum date from a table
    
    Args:
        table_name: Name of the table to query
        symbol: Optional symbol to filter by
    
    Returns:
        Maximum date found in the table
    """
    try:
        max_date = TradingService.get_max_date(table_name, symbol)
        return {"table": table_name, "symbol": symbol, "max_date": max_date}
    except Exception as e:
        logger.error(f"Error getting max date: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting max date: {str(e)}"
        )


@router.post("/custom-query")
async def execute_custom_query(query: str = Query(..., description="SQL query to execute")):
    """
    Execute a custom SQL query
    
    WARNING: Only use this endpoint with trusted inputs
    
    Args:
        query: SQL query string
    
    Returns:
        Query results
    """
    try:
        df = TradingService.execute_custom_query(query)
        results = convert_dataframe_for_json(df)
        return {
            "count": len(results),
            "data": results
        }
    except Exception as e:
        logger.error(f"Error executing custom query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing query: {str(e)}"
        )
