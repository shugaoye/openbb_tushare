import logging
import pandas as pd
import tushare as ts
from typing import Optional, Literal
from mysharelib.tools import setup_logger
from openbb_tushare.utils.helpers import get_api_key
from mysharelib.tools import normalize_symbol
from openbb_tushare import project_name

setup_logger(project_name)
logger = logging.getLogger(__name__)

def get_income_statement(
        symbol: str, 
        period: Literal["annual", "quarter"] = "annual",
        limit: Optional[int] = 5,
        use_cache: bool = True,
        api_key : Optional[str] = ""
    ) -> pd.DataFrame:
    from mysharelib.blob_cache import BlobCache

    cache = BlobCache(table_name="income_statement", project=project_name)
    data = cache.load_cached_data(symbol, "quarter", use_cache, get_tushare_data, api_key=api_key)
    if data is None:
        return pd.DataFrame()
    else:
        if period == "annual":
            # Filter rows where end_date ends with "1231"
            data = data[data['end_date'].astype(str).str.endswith('1231')]

        # Apply limit if specified
        if limit is not None:
            data = data.head(limit)
        
        return processing_data(data)
def get_tushare_data(
        symbol: str,
        period: str = "annual",
        api_key : Optional[str] = ""
    ) -> pd.DataFrame:
    tushare_api_key = get_api_key(api_key)
    pro = ts.pro_api(tushare_api_key)
    _, _, market = normalize_symbol(symbol)
    if market == 'HK':
        income_statement_df = pro.hk_income(ts_code=symbol)
    else:
        income_statement_df = pro.income(ts_code=symbol)
        income_statement_df = income_statement_df.drop_duplicates(subset='end_date', keep='first')
    
    return income_statement_df

def processing_data(income_statement_df: pd.DataFrame) -> pd.DataFrame:
    from openbb_tushare.utils.helpers import get_fiscal_period
    # logger.info("Processing income statement data")
    selected_columns = income_statement_df[['total_revenue', 'n_income']]
    selected_columns = selected_columns.rename(columns={'n_income':'net_income'})

    # Extract year from end_date and create fiscal_year column
    selected_columns.loc[:, 'fiscal_year'] = pd.to_datetime(income_statement_df['end_date']).dt.year
    selected_columns.loc[:, 'period_ending'] = pd.to_datetime(income_statement_df['end_date'])
    selected_columns.loc[:, 'fiscal_period'] = income_statement_df['end_type'].apply(get_fiscal_period)
    return selected_columns