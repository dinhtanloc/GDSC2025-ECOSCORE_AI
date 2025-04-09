import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaoChinhPhuScraper:
    def __init__(self, id_company):
        self.id_company = id_company
        self.data = []
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        return webdriver.Chrome(options=options)

    def search_articles(self):
        try:
            self.driver.get("https://baochinhphu.vn/")

            search_button = self.driver.find_element(By.CLASS_NAME, "header__search")
            search_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".header__search-layout.open-search"))
            )

            search_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.btn-search"))
            )
            search_input.send_keys(self.id_company)

            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "a.submit-search")
            submit_btn.click()
            time.sleep(3)

            self._extract_articles()

        finally:
            self.driver.quit()
        print(self.data)
        return self.data

    def _extract_articles(self):
        articles = self.driver.find_elements(By.CSS_SELECTOR, "div.box-stream-item")

        for index, article in enumerate(articles):
            try:
                title = article.find_element(By.CSS_SELECTOR, "a.box-stream-link-title").text
                link = article.find_element(By.CSS_SELECTOR, "a.box-stream-link-title").get_attribute("href")
                sapo = article.find_element(By.CSS_SELECTOR, "p.box-stream-sapo").text
                time_posted = article.find_element(By.CSS_SELECTOR, "span.box-stream-time").get_attribute("title")

                print(f"\n📌 Bài viết {index + 1}")
                print(f"📰 {title}")
                print(f"🔗 {link}")
                print(f"🕒 {time_posted}")
                print(f"📄 {sapo}")

                self.driver.get(link)
                time.sleep(2)

                full_title = self.driver.find_element(By.CSS_SELECTOR, "h1.detail-title").text

                paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "div.detail-content p")
                full_content = "\n".join([p.text for p in paragraphs if p.text.strip() != ""])

                self.data.append({
                    "id_company": self.id_company,
                    "title": title,
                    "link": link,
                    "time_posted": time_posted,
                    "sapo": sapo,
                    "full_title": full_title,
                    "content": full_content
                })

                self.driver.back()
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Lỗi đọc bài viết: {e}")

    def save_to_excel(self):
        df = pd.DataFrame(self.data)
        file_name = f"{self.id_company}_baiviet.xlsx"
        df.to_excel(file_name, index=False)
        print(f"\n✅ Đã lưu {len(self.data)} bài viết vào file: {file_name}")

if __name__ == "__main__":
    scraper = BaoChinhPhuScraper("VNG")
    scraper.search_articles()
    scraper.save_to_excel()
