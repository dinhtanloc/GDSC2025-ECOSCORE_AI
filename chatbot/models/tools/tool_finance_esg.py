#-----DATA-PREPROCESSING-------
import pandas as pd
from vnstock3 import Vnstock
from bs4 import BeautifulSoup
from typing import Literal, List
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime, timedelta
from langchain_core.tools import tool




####Get API
@tool
def generate_prompt_with_date(prompt):
    """
    Tạo một prompt có kèm theo ngày hiện tại.

    Args:
        prompt: Chuỗi prompt ban đầu.
    """
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    full_prompt = f"{prompt} Today's date is {current_date}."
    return full_prompt

@tool
def get_company_information(symbol):
    """
    Lấy thông tin công ty bao gồm tổng quan, hồ sơ, cổ đông, công ty con, và cán bộ. Phù hợp cho việc điều tra thông tin cụ thể của một doanh nghiệp trước khi đưa ra quyết định

    Args:
        symbol: Mã cổ phiếu của công ty.
    """
    company = Vnstock().stock(symbol=symbol, source='TCBS').company
    
    try:
        overview = company.overview()
        profile = company.profile()  # Assuming profile is another method; adjust if incorrect
        shareholders = company.shareholders()
        subsidiaries = company.subsidiaries()
        officers = company.officers()
        
        result = {
            "overview": overview.to_dict() if isinstance(overview, pd.DataFrame) else overview,
            "profile": profile.to_dict() if isinstance(profile, pd.DataFrame) else profile,
            "shareholders": shareholders.to_dict() if isinstance(shareholders, pd.DataFrame) else shareholders,
            "subsidiaries": subsidiaries.to_dict() if isinstance(subsidiaries, pd.DataFrame) else subsidiaries,
            "officers": officers.to_dict() if isinstance(officers, pd.DataFrame) else officers
        }
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)


@tool
def get_api_stock(symbols, startday, endday):
    """
    Lấy dữ liệu cổ phiếu cho một mã và khoảng thời gian cụ thể.

    Args:
        symbols: Mã cổ phiếu cần lấy dữ liệu.
        startday: Ngày bắt đầu của khoảng thời gian.
        endday: Ngày kết thúc của khoảng thời gian.
    """


    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    
    try:
        startday = pd.to_datetime(startday).strftime('%Y-%m-%d')
        endday = pd.to_datetime(endday).strftime('%Y-%m-%d')
        df = stock.quote.history(start=startday, end=endday, interval='1D')
        
        if not df.empty:
            df = df.map(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, pd.Timestamp)) else x)
            result = df.to_dict(orient='records')
        else:
            result = {"error": "Có lẽ ngày này ngân hàng không làm việc, do đây có thể là thứ bảy chủ nhật hoặc ngày lễ"}
        if startday==endday:
            result = [record for record in result if record['time'].startswith(startday)]
            if result.empty:
                result={"error": "Có lẽ ngày này ngân hàng không làm việc, do đây có thể là thứ bảy chủ nhật hoặc ngày lễ"}

    
    except Exception as e:
        result = {"error": "Có lẽ ngày này ngân hàng không làm việc, do đây có thể là thứ bảy chủ nhật hoặc ngày lễ"}

    
    return json.dumps(result, ensure_ascii=False)


@tool
def get_api_income_statement(symbols):
    """
    Truy xuất bảng báo cáo tài chính theo năm của từng doanh nghiệp cụ thể

    Args:
        symbols: Mã doanh nghiệp được niêm yết trên sàn chuwnsg khoán.
    """
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.income_statement(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)

@tool
def get_api_portfolio(symbols):
    """
    Lấy dữ liệu về một danh mục đầu tư gồm nhiều mã cổ phiếu khác nhau trong một khoảng thời gian.

    Args:
        symbols: Một danh sách các mã cổ phiếu trong danh mục đầu tư.
    """
    endday = datetime.now()
    startday = endday - timedelta(days=365)
    
    data = pd.DataFrame()
    errors = []  # To store error messages for each symbol
    for symbol in symbols:
        stock = Vnstock().stock(symbol=symbol, source='TCBS')
        try:
            df = stock.quote.history(
                start=startday.strftime('%Y-%m-%d'), 
                end=endday.strftime('%Y-%m-%d'), 
                interval='1D'
            )
            if df.empty:
                errors.append(f"No data found for symbol {symbol}")
                continue
            
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values(by='time', ascending=False)
            df['month'] = df['time'].dt.month
            df['year'] = df['time'].dt.year
            df['idx_time'] = df['time'].dt.to_period('M')
            
            df = df.drop_duplicates(subset=['idx_time'])
            df.set_index('idx_time', inplace=True)
            df = df[['close']]
            df.columns = [symbol]
            data = pd.concat([data, df], axis=1)
        except Exception as e:
            errors.append(f"Error for symbol {symbol}: {str(e)}")

    if data.empty:
        return json.dumps({"error": "No data found for the given symbols and range"}, default=str)
    
    data = data[~data.index.duplicated(keep='first')]
    data = data.groupby(data.index).mean()
    rets = np.log(data / data.shift(1)).dropna()
    
    result = rets.reset_index().to_dict(orient='records')

    # Convert the result and errors into a string for ToolMessage compatibility
    output = {"result": result, "errors": errors} if errors else result
    return json.dumps(output, default=str)

@tool
def get_api_balance_sheet(symbols):
    """
    Truy xuất bảng cân đối kế toán của từng doanh nghiệp cụ thể

    Args:
        symbols: Mã doanh nghiệp được định giá trên sàn chứng khoán
    """
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.balance_sheet(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)


tools = [
    generate_prompt_with_date,
    get_company_information,
    get_api_stock,
    get_api_portfolio,
    get_api_income_statement,
    get_api_balance_sheet,

]



tool_mapping = {
    "generate_prompt_with_date": generate_prompt_with_date,
    "get_company_information": get_company_information,
    "get_api_stock": get_api_stock,
    "get_api_income_statement": get_api_income_statement,
    "get_api_balance_sheet": get_api_balance_sheet,
    "get_api_portfolio": get_api_portfolio,
}

      
