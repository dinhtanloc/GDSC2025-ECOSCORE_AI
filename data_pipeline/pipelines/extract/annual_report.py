from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

class CafefPDFScraper:
    def __init__(self, stock_symbol: str, headless: bool = True, download_folder: str = "pdfs"):
        self.stock_symbol = stock_symbol
        self.download_folder = download_folder
        self.pdf_links = set()
        self.page = 1

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def search_disclosures(self):
        self.driver.get("https://cafef.vn/du-lieu/cong-bo-thong-tin.chn")
        stock_input = self.wait.until(EC.presence_of_element_located((By.ID, "acp-inp-disclosure")))
        stock_input.clear()
        stock_input.send_keys(self.stock_symbol)
        time.sleep(1)
        search_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-disclosure")))
        search_button.click()
        time.sleep(2)

    def scrape_pdf_links(self):
        while True:
            print(f"⏳ Đang xử lý trang {self.page}...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            try:
                anchors = self.wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(translate(@href, 'PDF', 'pdf'), '.pdf')]")
                ))
                for a in anchors:
                    href = a.get_attribute("href").strip()
                    if href.lower().endswith(".pdf"):
                        self.pdf_links.add(href)

            except Exception as e:
                print(f"❌ Không thể lấy PDF ở trang {self.page}: {e}")

            try:
                next_icon = self.wait.until(EC.presence_of_element_located((By.ID, "paging-right")))
                next_button_class = next_icon.get_attribute("class")

                if "enable" in next_button_class:
                    print("✅ Không còn trang tiếp theo.")
                    break

                next_icon.click()
                self.page += 1
                time.sleep(2)

            except Exception as e:
                print(f"❗Lỗi khi chuyển trang: {e}")
                break

    def save_links_to_file(self, file_path="pdf_links.txt"):
        with open(file_path, "w", encoding="utf-8") as f:
            for link in sorted(self.pdf_links):
                f.write(link + "\n")
        print(f"✅ Đã lưu {len(self.pdf_links)} link PDF vào '{file_path}'.")

    def download_all_pdfs(self):
        os.makedirs(self.download_folder, exist_ok=True)
        print(f"⬇️ Bắt đầu tải {len(self.pdf_links)} file PDF...")

        for idx, link in enumerate(sorted(self.pdf_links), 1):
            try:
                response = requests.get(link, timeout=20)
                file_name = os.path.basename(link.split('?')[0])
                file_path = os.path.join(self.download_folder, f"{idx:03d}_{file_name}")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Đã tải: {file_name}")
            except Exception as e:
                print(f"❌ Lỗi khi tải {link}: {e}")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = CafefPDFScraper(stock_symbol="ACB", headless=True)
    
    scraper.search_disclosures()
    scraper.scrape_pdf_links()
    scraper.save_links_to_file()
    scraper.download_all_pdfs()
    
    scraper.close()