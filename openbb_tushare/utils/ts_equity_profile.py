import logging
import pandas as pd
import tushare as ts
from datetime import (
    date as dateType,
    datetime,
)
from typing import Optional, Union
from openbb_tushare.utils.tools import setup_logger
from openbb_tushare.utils.helpers import get_api_key
from openbb_tushare.utils.tools import normalize_symbol

setup_logger()
logger = logging.getLogger(__name__)

EQUITY_INFO_SCHEMA = {
    "ts_code": "TEXT PRIMARY KEY",        # 证券代码 (Security ID)
    "com_name": "TEXT",          # 公司常用名称 (Common Name)
    "isin": "TEXT",                # 国际证券识别号码 (ISIN Code)
    "exchange": "TEXT",          # 证券交易所 (Exchange)
    "introduction": "TEXT",               # 公司描述 (Description)
    "chairman": "TEXT",                   # 董事长 (Chairman)
    "website": "TEXT",                    # 公司网站 (Website URL)
    "office": "TEXT",                     # 总部地址 (Headquarters)
    "city": "TEXT",                       # 城市 (City)
    "province": "TEXT",                   # 省份/州 (Province/State)
    "employees": "INTEGER",               # 员工数量 (Employee Count)
    "list_status": "TEXT",                # 上市状态 (List Status)
    "market": "TEXT",                     # 行业分类 (Industry/Market)
    "com_id": "TEXT",              # 统一社会信用代码 (Business ID)
    "manager": "TEXT",                    # 总经理 (General Manager)
    "secretary": "TEXT",                  # 董事会秘书 (Board Secretary)
    "reg_capital": "REAL",                # 注册资本 (Registered Capital)
    "setup_date": "TEXT",                 # 注册日期 (Registration Date)
    "email": "TEXT",                      # 邮箱 (Email)
    "ann_date": "TEXT",                   # 公告日期 (Announcement Date)
    "business_scope": "TEXT",             # 经营范围 (Business Scope)
    "main_business": "TEXT",              # 主营业务 (Main Business)
    "fullname": "TEXT",          # 公司全称 (Full Legal Name)
    "enname": "TEXT",                     # 英文名称 (English Name)
    "cn_spell": "TEXT",                   # 拼音 (Chinese Spelling)
    "list_date": "TEXT",         # 上市日期 (Listing Date)
    "delist_date": "TEXT",                # 退市日期 (Delisting Date)
    "trade_unit": "REAL",                 # 交易单位 (Trading Unit)
    "curr_type": "TEXT"          # 货币代码 (Currency)
}

def get_one(ts_code : str, use_cache: bool = True, api_key : str = "") -> pd.DataFrame:
    """
    Retrieves equity profile data from a cache or downloads it from the data source.
    
    Parameters:
        ts_code (str): Tushare stock symbol to fetch data for.
        use_cache (bool): Whether to use cached data or download fresh data.
        api_key (str): Tushare API key for authentication.

    Returns:
        DataFrame: DataFrame containing equity profile data.
    """
    from openbb_tushare.utils.table_cache import TableCache

    