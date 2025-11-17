"""Application configuration and environment settings"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DBHOST: str = "localhost"
    DBPORT: int = 3306
    DBUSER: str = "root"
    DBPWD: str = ""
    DBMKTDATA: str = "GlobalMarketData"
    
    # SSH Tunnel (Optional)
    SSHHOST: Optional[str] = None
    SSHUSR: Optional[str] = None
    SSHPWD: Optional[str] = None
    
    # Database Tables
    TBLOPTCHAIN: str = "OptionChains"
    TBLDLYPRICE: str = "histdailyprice7"
    TBLDLYPRED: str = "GMDailyOutputs"
    TBLDAILYPERF: str = "DailyPerformance_p1"
    TBLWEBPREDICT: str = "predicts_db"
    TBLUSRATES: str = "USRates"
    TBLOPTFEATURE: str = "option_features"
    
    # Server Configuration
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Chat History
    CHAT_HISTORY_PATH: str = "./chat_history"
    
    # Other Configuration
    VENDOR: str = "yfinance"
    FIRSTTRAINDTE: str = "2010/01/01"
    LASTTRAINDATE: str = "2021/10/19"
    PROD_LIST_DIR: str = "../Product_List"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()