import pytest
from datetime import date, datetime
from openbb_tushare.utils.tools import get_valid_date

def test_get_valid_date_with_string():
    test_date = "2023-01-01"
    result = get_valid_date(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 1)

def test_get_valid_date_with_date():
    test_date = date(2023, 1, 1)
    result = get_valid_date(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 1)

def test_get_valid_date_invalid_type():
    test_date = 20230101
    with pytest.raises(ValueError) as excinfo:
        get_valid_date(test_date)
    assert "must be a string or datetime object" in str(excinfo.value)

def test_get_valid_date_invalid_format():
    test_date = "2023/01/01"
    with pytest.raises(ValueError):
        get_valid_date(test_date)