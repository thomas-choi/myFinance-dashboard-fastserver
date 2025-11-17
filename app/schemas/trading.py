"""Schemas for trading data (options monitor)"""
from pydantic import BaseModel
from typing import Optional, Any


class OptionTrade(BaseModel):
    """Schema for option trade data matching DataFrame structure"""
    Date: Optional[str] = None
    Type: Optional[str] = None
    Trend: Optional[str] = None
    Symbol: str
    Expiration: str
    PnC: str  # Put or Call
    L_Strike: Optional[float] = None
    H_Strike: float
    Entry: Optional[float] = None
    Target: Optional[float] = None
    Stop: Optional[float] = None
    Last: float
    O_last: float
    O_bid: float
    O_ask: float
    O_pclose: float
    
    class Config:
        from_attributes = True


class OptionListResponse(BaseModel):
    """Response schema for list of options"""
    data: list[dict[str, Any]]
    count: int
    type: str  # "ETF" or "STK"

