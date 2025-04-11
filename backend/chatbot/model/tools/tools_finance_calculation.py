#-----DATA-PREPROCESSING-------
import pandas as pd
from vnstock import Vnstock
from bs4 import BeautifulSoup
from typing import Literal, List
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime, timedelta
from langchain_core.tools import tool




###EUT
@tool
def calculate_utility(outcome: float, risk_aversion: float) -> float:
    """
    Tính toán độ hữu ích dựa trên kết quả và hệ số ngại rủi ro.

    Args:
        outcome: Kết quả tài chính cần đánh giá.
        risk_aversion: Hệ số ngại rủi ro.
    """
    if risk_aversion != 1:
        return (outcome ** (1 - risk_aversion)) / (1 - risk_aversion)
    else:
        return np.log(outcome)
@tool
def calculate_expected_utility(probabilities: List[float], utilities: List[float]) -> float:
    """
    Tính toán độ hữu ích kỳ vọng.

    Args:
        probabilities:Danh sách xác suất liên quan đến các kết quả khác nhau.
        utilities: Danh sách độ hữu ích tương ứng với các kết quả.

    Raises:
        ValueError:Nếu độ dài của probabilities và utilities không khớp nhau.
    """
    if len(probabilities) != len(utilities):
        raise ValueError("Probabilities and utilities must have the same length.")
    
    expected_utility = np.dot(probabilities, utilities)
    return expected_utility


# @tool
# def porfolio_optimize_EUT():
#     pass

###MVP
@tool
def calculate_portfolio_return(returns: List[float], weights: List[float]) -> float:
    """
    Tính toán lợi nhuận hàng năm của danh mục đầu tư.

    Args:
        returns: Danh sách lợi nhuận lịch sử của các tài sản trong danh mục đầu tư.
        weights: Danh sách tỷ trọng đại diện cho phần trăm của từng tài sản trong danh mục.
    """
    returns_array = np.array(returns)
    return np.dot(returns_array.mean(), weights) * 252

@tool
def calculate_portfolio_volatility(returns: List[float], weights: List[float]) -> float:
    """
    Tính toán biến động hàng năm của danh mục đầu tư.

    Args:
        returns:  Danh sách lợi nhuận lịch sử của các tài sản trong danh mục đầu tư.
        weights:  Danh sách tỷ trọng đại diện cho phần trăm của từng tài sản trong danh mục.
    """
    return np.dot(weights, np.dot(returns.cov() * 252, weights)) ** 0.5  # Annualized volatility

@tool
def calculate_sharpe_ratio(returns: List[float], weights: List[float], risk_free_rate: float) -> float:
    """
    Tính toán tỷ lệ Sharpe của danh mục đầu tư.

    Args:
        returns: Danh sách lợi nhuận lịch sử của các tài sản trong danh mục đầu tư.
        weights: Danh sách tỷ trọng đại diện cho phần trăm của từng tài sản trong danh mục.
        risk_free_rate: Tỷ lệ lợi nhuận không rủi ro.
    """
    port_return = calculate_portfolio_return(returns, weights)
    port_volatility = calculate_portfolio_volatility(returns, weights)
    sharpe_ratio = (port_return - risk_free_rate) / port_volatility
    return sharpe_ratio

@tool
def portfolio_optimize(returns, sharpe_ratio_or_variance=True):
    """
    Tối ưu hóa danh mục đầu tư dựa trên tối ưu lợi nhuận hoặc giảm thiểu rủi ro sau khi biết được tình hình doanh mục đầu tư được dự đoán trong tương lai trước đó.

    Args:
        returns: Thông tin tình hình danh mục đầu tư sau khi dùng hàm predict_future_prices .
        sharpe_ratio_or_variance: Một giá trị boolean chỉ định có tối ưu hóa cho tỷ lệ Sharpe (True) hay biến động (False).
    """
    returns = json.loads(returns)
    returns = pd.DataFrame([returns])
    # returns=returns[returns.columns[1:]]
    # print(returns)
    num_assets = len(returns.columns)
    # print('haha',num_assets)
    init_guess = num_assets * [1. / num_assets]
    bounds = tuple((0, 1) for asset in range(num_assets))
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    if sharpe_ratio_or_variance:
        result = minimize(lambda x: -calculate_sharpe_ratio(x, returns), init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    else:
        result = minimize(lambda x: calculate_portfolio_volatility(x, returns), init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    optimal_weights = dict(zip(returns.columns, result.x))
    
    return optimal_weights

### CAPM
@tool
def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
    """
    Tính toán hệ số beta của một tài sản.

    Args:
        asset_returns: Danh sách lợi nhuận của tài sản.
        market_returns: Danh sách lợi nhuận của thị trường.
    """
    covariance_matrix = np.cov(asset_returns, market_returns)
    beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
    return beta

@tool
def calculate_capm(risk_free_rate: float, beta: float, market_return: float) -> float:
    """
    Tính toán lợi nhuận kỳ vọng của một tài sản bằng công thức CAPM.

    Args:
        risk_free_rate: Tỷ lệ lợi nhuận không rủi ro.
        beta: Hệ số beta của tài sản.
        market_return: Lợi nhuận kỳ vọng của thị trường.
    """
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return expected_return


#### Make prediction
@tool
def predict_future_prices(api_portfolio,symbols, n):
    """
    Dự đoán giá danh mục đầu tư trong n tháng tới dựa trên dữ liệu đầu vào. Phù hợp cho việc dự báo tình hình của danh mục 

    Args:
        api_portfolio: dữ liệu về một danh mục đầu tư gồm nhiều mã cổ phiếu khác nhau trong một khoảng thời gian
        symbols: Danh sách các mã cổ phiếu khác nhau thuộc danh mục đầu tư đó
        n: Số tháng từ ngày hiện tại để dự đoán.
    """
    data = api_portfolio

    try:
        df = pd.DataFrame(eval(data))
    except (ValueError, SyntaxError) as e:
        print(f"Error creating DataFrame: {e}")
        return
    
    if df.empty or not {'idx_time', 'AAA', 'A32'}.issubset(df.columns):
        print("Data không hợp lệ. Đảm bảo dữ liệu chứa các cột 'idx_time', 'AAA', và 'A32'.")
        return
    
    df['idx_time'] = pd.to_datetime(df['idx_time'] + '-01', format='%Y-%m-%d')
    
    df['days'] = (df['idx_time'] - df['idx_time'].min()).dt.days
    
    df = df.dropna(subset=symbols)
    
    degree = 2
    coeffs = {}

    for symbol in symbols:
        coeffs[symbol] = np.polyfit(df['days'], df[symbol], degree)
    
    future_dates = pd.date_range(start=pd.to_datetime('today').replace(day=1), periods=n, freq='MS')
    future_days = (future_dates - df['idx_time'].min()).days
    
    predictions = {}
    for symbol in symbols:
        predictions[symbol] = np.polyval(coeffs[symbol], future_days)
    
    future_df = pd.DataFrame({
        'idx_time': future_dates.strftime('%Y-%m'),  
        **predictions
    })
    
    last_prediction = future_df.iloc[-1]
    
    result = {symbol: last_prediction[symbol] for symbol in symbols}
    
    return json.dumps(result, default=str)

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

def calculate_esg_score_by_ratio(amount, revenue, threshold=0.01):
    if revenue == 0 or pd.isna(revenue):
        return 0
    ratio = amount / revenue
    score = min(100, round((ratio / threshold) * 100))
    return score


@tool
def score_training_cost(financial_df: dict) -> str:
    """
    Tính điểm ESG từ chi phí đào tạo dựa trên tỷ lệ chi phí đào tạo / doanh thu
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    revenue = df.get("Doanh thu thuần", 0).values[0]
    training_cost = df.get("Chi phí đào tạo", 0).values[0]
    score = calculate_esg_score_by_ratio(training_cost, revenue)
    return f"Chi phí đào tạo chiếm {training_cost:,} trên {revenue:,} doanh thu. Điểm ESG đào tạo: {score}/100"


@tool
def score_social_cost(financial_df: dict) -> str:
    """
    Tính điểm ESG từ chi phí xã hội, từ thiện
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    revenue = df.get("Doanh thu thuần", 0).values[0]
    social_cost = df.get("Chi phí xã hội", 0).values[0]
    score = calculate_esg_score_by_ratio(social_cost, revenue)
    return f"Chi phí xã hội chiếm {social_cost:,} trên {revenue:,} doanh thu. Điểm ESG xã hội: {score}/100"


@tool
def score_environment_cost(financial_df: dict) -> str:
    """
    Tính điểm ESG từ chi phí môi trường / năng lượng
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    revenue = df.get("Doanh thu thuần", 0).values[0]
    env_cost = df.get("Chi phí môi trường", 0).values[0]
    score = calculate_esg_score_by_ratio(env_cost, revenue)
    return f"Chi phí môi trường chiếm {env_cost:,} trên {revenue:,} doanh thu. Điểm ESG môi trường: {score}/100"


@tool
def score_rnd_cost(financial_df: dict) -> str:
    """
    Tính điểm ESG từ chi phí R&D / nghiên cứu phát triển
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    revenue = df.get("Doanh thu thuần", 0).values[0]
    rnd_cost = df.get("Chi phí R&D", 0).values[0]
    score = calculate_esg_score_by_ratio(rnd_cost, revenue)
    return f"Chi phí R&D chiếm {rnd_cost:,} trên {revenue:,} doanh thu. Điểm ESG R&D: {score}/100"

@tool
def score_short_term_debt(financial_df: dict) -> str:
    """
    Tính điểm quản trị rủi ro tài chính từ tỷ lệ nợ ngắn hạn / tổng tài sản
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    debt = df.get("Nợ ngắn hạn", 0).values[0]
    assets = df.get("Tổng tài sản", 0).values[0]
    if assets == 0:
        return "Không thể tính điểm vì tổng tài sản bằng 0."
    ratio = debt / assets
    score = max(0, 100 - int(ratio * 100)) 
    return f"Tỷ lệ nợ ngắn hạn: {ratio:.2%}. Điểm quản trị rủi ro: {score}/100"

@tool
def score_net_profit_margin(financial_df: dict) -> str:
    """
    Đánh giá hiệu quả sinh lời
    Args:
        financial_df: DataFrame chứa thông tin tài chính của doanh nghiệp.
    """
    df = pd.DataFrame([financial_df])
    net_profit = df.get("Lợi nhuận sau thuế", 0).values[0]
    revenue = df.get("Doanh thu thuần", 0).values[0]
    if revenue == 0:
        return "Không có doanh thu để tính biên lợi nhuận."
    margin = net_profit / revenue
    score = min(100, round((margin / 0.05) * 100)) 
    return f"Tỷ suất lợi nhuận: {margin:.2%}. Điểm hiệu quả tài chính: {score}/100"


@tool
def score_esg_report(symbol: str) -> str:
    """
    Tính toán tổng điểm ESG của doanh nghiệp dựa trên các yếu tố đào tạo, xã hội, môi trường, R&D, rủi ro tài chính, hiệu quả sinh lời và mức độ tập trung cổ đông.

    Args:
        symbol: Mã cổ phiếu doanh nghiệp

    Returns:
        Báo cáo ESG dạng văn bản chi tiết theo từng phần, kèm tổng điểm (trung bình các phần).
    """
    results = []
    total_score = 0
    count = 0

    try:
        # ---- 1. Income Statement: đào tạo, xã hội, môi trường, R&D, biên lợi nhuận
        income_data = json.loads(get_api_income_statement(symbol))
        if isinstance(income_data, list) and income_data:
            latest_income = income_data[0]
            for scoring_tool in [
                score_training_cost, 
                score_social_cost, 
                score_environment_cost, 
                score_rnd_cost, 
                score_net_profit_margin
            ]:
                explanation = scoring_tool(latest_income)
                results.append(explanation)
                score = extract_score(explanation)
                if score is not None:
                    total_score += score
                    count += 1

        # ---- 2. Balance Sheet: nợ ngắn hạn / tài sản
        balance_data = json.loads(get_api_balance_sheet(symbol))
        if isinstance(balance_data, list) and balance_data:
            latest_balance = balance_data[0]
            explanation = score_short_term_debt(latest_balance)
            results.append(explanation)
            score = extract_score(explanation)
            if score is not None:
                total_score += score
                count += 1

        # ---- 3. Company Info: phân tán cổ đông
        results.append(explanation)
        score = extract_score(explanation)
        if score is not None:
            total_score += score
            count += 1

    except Exception as e:
        results.append(f"❌ Lỗi trong quá trình tính toán: {str(e)}")

    avg_score = total_score / count if count > 0 else 0
    summary = f"\n\n📊 Tổng điểm ESG trung bình: {round(avg_score, 2)}/100 dựa trên {count} chỉ số."

    return "\n".join(results) + summary


def extract_score(text):
    """Trích xuất điểm số từ chuỗi văn bản"""
    try:
        parts = text.split("Điểm")
        for p in parts:
            if "/100" in p:
                return int(p.strip().split("/")[0].split()[-1])
    except:
        return None


tools = [
    calculate_utility,
    calculate_expected_utility,
    calculate_portfolio_return,
    calculate_portfolio_volatility,
    calculate_sharpe_ratio,
    calculate_beta,
    calculate_capm,
    generate_prompt_with_date,
    get_company_information,
    get_api_stock,
    get_api_portfolio,
    get_api_income_statement,
    get_api_balance_sheet,
    predict_future_prices,
    portfolio_optimize,
    score_training_cost,
    score_social_cost,
    score_environment_cost,
    score_rnd_cost,
    score_short_term_debt,
    score_net_profit_margin,
    
]



tool_mapping = {
    "calculate_utility": calculate_utility,
    "calculate_expected_utility": calculate_expected_utility,
    "calculate_portfolio_return": calculate_portfolio_return,
    "calculate_portfolio_volatility": calculate_portfolio_volatility,
    "calculate_sharpe_ratio": calculate_sharpe_ratio,
    "calculate_beta": calculate_beta,
    "calculate_capm": calculate_capm,
    "generate_prompt_with_date": generate_prompt_with_date,
    "get_company_information": get_company_information,
    "get_api_stock": get_api_stock,
    "get_api_income_statement": get_api_income_statement,
    "get_api_balance_sheet": get_api_balance_sheet,
    "predict_future_prices": predict_future_prices,
    "get_api_portfolio": get_api_portfolio,
    "portfolio_optimize": portfolio_optimize,
}

      
