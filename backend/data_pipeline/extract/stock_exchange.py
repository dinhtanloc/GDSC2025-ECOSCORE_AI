import pandas as pd
from vnstock import Vnstock
from bs4 import BeautifulSoup
from vnstock.explorer.vci import Company
import os


class StockCompanyDataCollector:
    def __init__(self, ticket_collection, period='year', clean_html=False, filter_by=None):
        self.ticket_collection = ticket_collection
        self.vnstock = Vnstock()
        self.period = period
        self.clean_html = clean_html
        self.filter_by = filter_by

    @staticmethod
    def extract_text_from_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=" ", strip=True)

    @staticmethod
    def process_html_columns(df):
        html_columns = [col for col in df.columns if df[col].astype(str).str.contains('<').any()]
        for col in html_columns:
            df[col] = df[col].apply(StockCompanyDataCollector.extract_text_from_html)
        return df

    def get_profile(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                company = self.vnstock.stock(symbol=symbol, source='TCBS').company
                df = company.profile()
                if self.clean_html:
                    df = self.process_html_columns(df)
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Profile] {symbol}: {e}")
        return df_all

    def get_financial_ratio(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                stock = self.vnstock.stock(symbol=symbol, source='VCI')
                df = stock.finance.ratio(period=self.period, lang='en')
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Ratio] {symbol}: {e}")
        return df_all

    def get_cashflow(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                stock = self.vnstock.stock(symbol=symbol, source='VCI')
                df = stock.finance.cash_flow(period=self.period, dropna=True)
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Cash Flow] {symbol}: {e}")
        return df_all

    def get_balance_sheet(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                stock = self.vnstock.stock(symbol=symbol, source='VCI')
                df = stock.finance.balance_sheet(period=self.period, dropna=True)
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Balance Sheet] {symbol}: {e}")
        return df_all

    def get_income_statement(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                stock = self.vnstock.stock(symbol=symbol, source='VCI')
                df = stock.finance.income_statement(period=self.period, dropna=True)
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Income] {symbol}: {e}")
        return df_all

    def get_events(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                company = self.vnstock.stock(symbol=symbol, source='TCBS').company
                df = company.events()
                df.drop(columns=['notify_date', 'exer_date', 'reg_final_date', 'exer_right_date'], inplace=True, errors='ignore')
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Events] {symbol}: {e}")
        return df_all

    def get_news(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                company = self.vnstock.stock(symbol=symbol, source='TCBS').company
                df = company.news()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[News] {symbol}: {e}")
        return df_all

    def get_company_reports(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).reports()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Reports] {symbol}: {e}")
        return df_all

    def get_officers(self, filter_by='working'):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).officers(filter_by=filter_by)
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Officers] {symbol}: {e}")
        return df_all

    def get_affiliates(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).affiliate()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Affiliates] {symbol}: {e}")
        return df_all

    def get_shareholders(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).shareholders()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Shareholders] {symbol}: {e}")
        return df_all

    def get_ratio_summary(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).ratio_summary()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Ratio Summary] {symbol}: {e}")
        return df_all

    def get_overview(self):
        df_all = pd.DataFrame()
        for symbol in self.ticket_collection:
            try:
                df = Company(symbol).overview()
                df['ticker'] = symbol
                df_all = pd.concat([df_all, df], ignore_index=True)
            except Exception as e:
                print(f"[Overview] {symbol}: {e}")
        return df_all

    def export_all_to_csv(self, output_dir='company_data'):
        print("Exporting data to CSV files...")
        os.makedirs(output_dir, exist_ok=True)
        data_sources = {
            'Profile': self.get_profile,
            'FinancialRatio': self.get_financial_ratio,
            'CashFlow': self.get_cashflow,
            'BalanceSheet': self.get_balance_sheet,
            'IncomeStatement': self.get_income_statement,
            'Events': self.get_events,
            'News': self.get_news,
            'Reports': self.get_company_reports,
            'Officers': self.get_officers,
            'Affiliates': self.get_affiliates,
            'Shareholders': self.get_shareholders,
            'RatioSummary': self.get_ratio_summary,
            'Overview': self.get_overview
        }

        for name, func in data_sources.items():
            try:
                df = func()
                df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)
                print(f"{name}.csv exported.")
            except Exception as e:
                print(f"Failed to export {name}: {e}")

        print(f"All available data exported to folder '{output_dir}'.")
if __name__ == "__main__":
    ticket_collection = ['VNM', 'FPT', 'VCB']
    collector = StockCompanyDataCollector(ticket_collection)
    collector.export_all_to_csv()


