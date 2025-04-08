from vnstock import Vnstock
import pandas as pd
from datetime import datetime
import time
from vnstock.explorer.vci import Company

class StockDataCollector:
    def __init__(self, group: str, period: str, start: str, end: str, interval: str, export_format: str):
        """
        Khởi tạo đối tượng StockDataCollector.
        
        :param group: Nhóm cổ phiếu (ví dụ: 'VN30', 'HNX').
        :param period: Khoảng thời gian báo cáo tài chính ('year' hoặc 'quarter').
        :param start: Ngày bắt đầu thu thập dữ liệu lịch sử (định dạng YYYY-MM-DD).
        :param end: Ngày kết thúc thu thập dữ liệu lịch sử (định dạng YYYY-MM-DD).
        :param interval: Khoảng thời gian giữa các điểm dữ liệu ('1D', '1W', v.v.).
        :param export_format: Định dạng xuất file ('csv', 'xlsx', 'json').
        """
        self.group = group
        self.period = period
        self.start = start
        self.end = end
        self.interval = interval
        self.export_format = export_format
        self.vnstock = Vnstock()
        self.symbols = self.get_symbols_from_group()

    def get_symbols_from_group(self):
        """Lấy danh sách mã cổ phiếu từ nhóm."""
        print(f"📌 Lấy danh sách mã cổ phiếu từ nhóm: {self.group}")
        symbols = self.vnstock.stock().listing.symbols_by_group(self.group)
        if symbols is None or symbols.empty:
            raise ValueError(f"Không tìm thấy mã cổ phiếu nào trong nhóm: {self.group}")
        return symbols.tolist()

    def collect_stock_data(self, symbol: str):
        """Thu thập dữ liệu chứng khoán lịch sử."""
        try:
            print(f"⏳ Thu thập dữ liệu lịch sử cho mã: {symbol}")
            stock = self.vnstock.stock(symbol=symbol, source='VCI')
            quote_df = stock.quote.history(start=self.start, end=self.end, interval=self.interval)
            if quote_df is None or quote_df.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            quote_df['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return quote_df
        except Exception as e:
            print(f"❌ Lỗi khi thu thập dữ liệu lịch sử cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_info(self, symbol: str):
        """Thu thập thông tin công ty."""
        try:
            print(f"🔍 Thu thập thông tin công ty cho mã: {symbol}")
            company = Company(symbol)
            overview = company.overview()
            if overview is None or overview.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            return overview
        except Exception as e:
            print(f"❌ Lỗi khi thu thập thông tin công ty cho {symbol}: {type(e).__name__} - {e}")
            return {'symbol': symbol, 'error': str(e)}

    def collect_company_shareholder(self, symbol: str):
        """Thu thập thông tin cổ đông."""
        try:
            print(f"👥 Thu thập thông tin cổ đông cho mã: {symbol}")
            company = Company(symbol)
            shareholders = company.shareholders()
            if shareholders is None or shareholders.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            shareholders['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return shareholders
        except Exception as e:
            print(f"❌ Lỗi khi thu thập thông tin cổ đông cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_ratio(self, symbol: str):
        """Thu thập tỷ số tài chính."""
        try:
            print(f"📊 Thu thập tỷ số tài chính cho mã: {symbol}")
            company = Company(symbol)
            ratio = company.ratio_summary()
            if ratio is None or ratio.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            ratio['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return ratio
        except Exception as e:
            print(f"❌ Lỗi khi thu thập tỷ số tài chính cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_affiliate(self, symbol: str):
        """Thu thập thông tin công ty liên kết."""
        try:
            print(f"🔗 Thu thập thông tin công ty liên kết cho mã: {symbol}")
            company = Company(symbol)
            affiliates = company.affiliate()
            if affiliates is None or affiliates.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            affiliates['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return affiliates
        except Exception as e:
            print(f"❌ Lỗi khi thu thập thông tin công ty liên kết cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_officers(self, symbol: str, filter_by: str = 'working'):
        """Thu thập thông tin ban lãnh đạo công ty."""
        try:
            print(f"👔 Thu thập thông tin ban lãnh đạo cho mã: {symbol}")
            company = Company(symbol)
            officers = company.officers(filter_by=filter_by)
            if officers is None or officers.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            officers['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return officers
        except Exception as e:
            print(f"❌ Lỗi khi thu thập thông tin ban lãnh đạo cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_news(self, symbol: str):
        """Thu thập tin tức công ty."""
        try:
            print(f"📰 Thu thập tin tức cho mã: {symbol}")
            company = Company(symbol)
            news = company.news()
            if news is None or news.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            news['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return news
        except Exception as e:
            print(f"❌ Lỗi khi thu thập tin tức cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_event(self, symbol: str):
        """Thu thập sự kiện công ty."""
        try:
            print(f"📅 Thu thập sự kiện cho mã: {symbol}")
            company = Company(symbol)
            events = company.events()
            if events is None or events.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            events['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return events
        except Exception as e:
            print(f"❌ Lỗi khi thu thập sự kiện cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_company_report(self, symbol: str):
        """Thu thập báo cáo công ty."""
        try:
            print(f"📋 Thu thập báo cáo cho mã: {symbol}")
            company = Company(symbol)
            reports = company.reports()
            if reports is None or reports.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            reports['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return reports
        except Exception as e:
            print(f"❌ Lỗi khi thu thập báo cáo cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_income_statement(self, symbol: str):
        """Thu thập báo cáo thu nhập."""
        try:
            print(f"💰 Thu thập báo cáo thu nhập cho mã: {symbol}")
            stock = self.vnstock.stock(symbol=symbol, source='VCI')
            income = stock.finance.income_statement(period=self.period, dropna=True)
            if income is None or income.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            income['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return income
        except Exception as e:
            print(f"❌ Lỗi khi thu thập báo cáo thu nhập cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_balance_sheet(self, symbol: str):
        """Thu thập bảng cân đối kế toán."""
        try:
            print(f"⚖️ Thu thập bảng cân đối kế toán cho mã: {symbol}")
            stock = self.vnstock.stock(symbol=symbol, source='VCI')
            balance = stock.finance.balance_sheet(period=self.period, dropna=True)
            if balance is None or balance.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            balance['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return balance
        except Exception as e:
            print(f"❌ Lỗi khi thu thập bảng cân đối kế toán cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_cash_flow(self, symbol: str):
        """Thu thập báo cáo lưu chuyển tiền tệ."""
        try:
            print(f"💸 Thu thập báo cáo lưu chuyển tiền tệ cho mã: {symbol}")
            stock = self.vnstock.stock(symbol=symbol, source='VCI')
            cashflow = stock.finance.cash_flow(period=self.period, dropna=True)
            if cashflow is None or cashflow.empty:
                raise ValueError("DataFrame rỗng hoặc không có dữ liệu.")
            cashflow['symbol'] = symbol  # Thêm cột mã cổ phiếu
            return cashflow
        except Exception as e:
            print(f"❌ Lỗi khi thu thập báo cáo lưu chuyển tiền tệ cho {symbol}: {type(e).__name__} - {e}")
            return None

    def collect_all(self):
        """Thu thập tất cả dữ liệu cho tất cả các mã."""
        stock_data = []
        company_info = []
        company_shareholders = []
        company_ratios = []
        company_affiliates = []
        company_officers = []
        company_news = []
        company_events = []
        company_reports = []
        income_statements = []
        balance_sheets = []
        cash_flows = []

        for symbol in self.symbols:
            print(f"⏳ Đang thu thập dữ liệu cho: {symbol}")
            stock_data.append(self.collect_stock_data(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_info.append(self.collect_company_info(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_shareholders.append(self.collect_company_shareholder(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_ratios.append(self.collect_company_ratio(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_affiliates.append(self.collect_company_affiliate(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_officers.append(self.collect_company_officers(symbol, filter_by='working'))
            time.sleep(1)  # Tránh quá tải API
            company_news.append(self.collect_company_news(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_events.append(self.collect_company_event(symbol))
            time.sleep(1)  # Tránh quá tải API
            company_reports.append(self.collect_company_report(symbol))
            time.sleep(1)  # Tránh quá tải API
            income_statements.append(self.collect_income_statement(symbol))
            time.sleep(1)  # Tránh quá tải API
            balance_sheets.append(self.collect_balance_sheet(symbol))
            time.sleep(1)  # Tránh quá tải API
            cash_flows.append(self.collect_cash_flow(symbol))
            time.sleep(5)  # Tránh quá tải API

        # Kết hợp các DataFrame thành một
        stock_data = pd.concat([df for df in stock_data if df is not None], ignore_index=True)
        company_info = pd.DataFrame(company_info)
        company_shareholders = pd.concat([df for df in company_shareholders if df is not None], ignore_index=True)
        company_ratios = pd.concat([df for df in company_ratios if df is not None], ignore_index=True)
        company_affiliates = pd.concat([df for df in company_affiliates if df is not None], ignore_index=True)
        company_officers = pd.concat([df for df in company_officers if df is not None], ignore_index=True)
        company_news = pd.concat([df for df in company_news if df is not None], ignore_index=True)
        company_events = pd.concat([df for df in company_events if df is not None], ignore_index=True)
        company_reports = pd.concat([df for df in company_reports if df is not None], ignore_index=True)
        income_statements = pd.concat([df for df in income_statements if df is not None], ignore_index=True)
        balance_sheets = pd.concat([df for df in balance_sheets if df is not None], ignore_index=True)
        cash_flows = pd.concat([df for df in cash_flows if df is not None], ignore_index=True)

        return (
            stock_data, company_info, company_shareholders, company_ratios, company_affiliates,
            company_officers, company_news, company_events, company_reports,
            income_statements, balance_sheets, cash_flows
        )

    def export(self, dataframes, filenames=None):
        """Xuất dữ liệu ra file."""
        if filenames is None:
            filenames = [
                f'stock_data_{self.group}.{self.export_format}',
                f'company_info_{self.group}.{self.export_format}',
                f'company_shareholders_{self.group}.{self.export_format}',
                f'company_ratios_{self.group}.{self.export_format}',
                f'company_affiliates_{self.group}.{self.export_format}',
                f'company_officers_{self.group}.{self.export_format}',
                f'company_news_{self.group}.{self.export_format}',
                f'company_events_{self.group}.{self.export_format}',
                f'company_reports_{self.group}.{self.export_format}',
                f'income_statements_{self.group}.{self.export_format}',
                f'balance_sheets_{self.group}.{self.export_format}',
                f'cash_flows_{self.group}.{self.export_format}'
            ]

        for df, filename in zip(dataframes, filenames):
            if df is None or df.empty:
                print(f"⚠️ Không có dữ liệu để xuất cho file: {filename}")
                continue

            print(f"💾 Xuất dữ liệu ra file: {filename}")
            if self.export_format == 'csv':
                df.to_csv(filename, index=False, encoding='utf-8-sig')
            elif self.export_format == 'xlsx':
                df.to_excel(filename, index=False)
            elif self.export_format == 'json':
                df.to_json(filename, orient='records', force_ascii=False)
            else:
                raise ValueError(f"Định dạng xuất không hỗ trợ: {self.export_format}")

if __name__ == "__main__":
    # Khởi tạo đối tượng StockDataCollector với các tham số cần thiết
    collector = StockDataCollector(
        group='VN30',               # Nhóm cổ phiếu (ví dụ: VN30)
        period='year',             # Khoảng thời gian báo cáo tài chính ('year' hoặc 'quarter')
        start='2024-01-01',        # Ngày bắt đầu thu thập dữ liệu lịch sử
        end='2025-03-31',          # Ngày kết thúc thu thập dữ liệu lịch sử
        interval='1D',             # Khoảng thời gian giữa các điểm dữ liệu (1 ngày)
        export_format='xlsx'       # Định dạng xuất file ('csv', 'xlsx', hoặc 'json')
    )

    # Thu thập tất cả dữ liệu cho nhóm cổ phiếu đã chọn
    (
        stock_data, company_info, company_shareholders, company_ratios, company_affiliates,
        company_officers, company_news, company_events, company_reports,
        income_statements, balance_sheets, cash_flows
    ) = collector.collect_all()

    # Xuất dữ liệu ra file
    collector.export([
        stock_data, company_info, company_shareholders, company_ratios, company_affiliates,
        company_officers, company_news, company_events, company_reports,
        income_statements, balance_sheets, cash_flows
    ])

    # Thông báo hoàn thành
    print("✅ Đã lưu tất cả dữ liệu.")