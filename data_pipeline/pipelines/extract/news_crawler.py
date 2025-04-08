import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class ChinhPhuNewsCrawler:
    def __init__(self, keyword="VNG", max_pages=5, delay=1.5):
        self.base_url = "https://chinhphu.vn/"
        self.keyword = keyword
        self.max_pages = max_pages
        self.delay = delay
        self.articles = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_page(self, page_number):
        params = {
            "pageid": "473",
            "q": self.keyword,
            "p": page_number
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Lỗi khi tải trang {page_number}: {e}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, "html.parser")
        articles_html = soup.select(".list-news .item")

        if not articles_html:
            return False

        for item in articles_html:
            try:
                title_tag = item.find("a")
                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                if not link.startswith("http"):
                    link = self.base_url.rstrip("/") + "/" + link.lstrip("/")
                summary = item.find("div", class_="sapo").get_text(strip=True) if item.find("div", class_="sapo") else ""
                self.articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary
                })
            except Exception as e:
                print(f"⚠️ Lỗi khi xử lý bài viết: {e}")
                continue

        return True

    def crawl(self):
        for page in range(1, self.max_pages + 1):
            print(f"🔍 Đang crawl trang {page}...")
            html = self.fetch_page(page)
            if not html:
                continue
            has_data = self.parse_page(html)
            if not has_data:
                print("Không tìm thấy thêm bài viết, dừng lại.")
                break
            time.sleep(self.delay)

        return pd.DataFrame(self.articles)

    def save_to_csv(self, df, filename=None):
        if filename is None:
            filename = f"chinhphu_news_{self.keyword}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"Đã lưu {len(df)} bài viết vào '{filename}'")


if __name__ == "__main__":
    crawler = ChinhPhuNewsCrawler(keyword="VNG", max_pages=5)
    df_news = crawler.crawl()
    crawler.save_to_csv(df_news)
    print(df_news.head())
