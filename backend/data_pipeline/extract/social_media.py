from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class ArticleScraper:
    def __init__(self, symbol):
        """
        Khởi tạo scraper với tên công ty (symbol).
        """
        self.symbol = symbol
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--allow-insecure-localhost")


        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.chrome_options.add_argument(f"user-agent={user_agent}")

        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_comments(self, driver):
        """
        Lấy danh sách bình luận từ trang bài viết.
        """
        comments = []
        try:
            time.sleep(3)
            comment_blocks = driver.find_elements(By.CSS_SELECTOR, "div.thread-comment__box")

            for block in comment_blocks:
                try:
                    author = block.find_element(By.CSS_SELECTOR, "a.author-name").text
                    content = block.find_element(By.CSS_SELECTOR, "div.xfBody").text
                    date = block.find_element(By.CSS_SELECTOR, "a.thread-comment__date span").get_attribute("title")
                    comments.append({
                        'author': author,
                        'date': date if date else "Không rõ",
                        'content': content
                    })
                except Exception as e:
                    print(f"Error extracting comment: {e}")
                    continue
        except Exception as e:
            print(f"Error getting comments: {e}")

        return comments


    def scrape_articles(self):
        """
        Thu thập thông tin từ tất cả các bài viết liên quan đến symbol.
        :return: List of articles with their content and metadata.
        """
        articles = []
        try:
            self.driver.get("https://tinhte.vn")
            time.sleep(3)
            search_box = self.driver.find_element(By.ID, "gsc-i-id1")
            search_box.clear()
            search_box.send_keys(self.symbol)
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)

            article_links = []
            results = self.driver.find_elements(By.CSS_SELECTOR, ".gs-title a.gs-title")
            for item in results:
                url = item.get_attribute('href')
                if url and "thread" in url:
                    article_links.append(url)

            article_links = article_links[:5]  

            for article_url in article_links:
                article_data = self._scrape_single_article(article_url)
                if article_data:
                    articles.append(article_data)

        except Exception as e:
            print(f"Error scraping articles: {e}")

        finally:
            self.driver.quit()

        return articles


    def _scrape_single_article(self, article_url):
        """
        Thu thập thông tin từ một bài viết cụ thể.
        :param article_url: URL của bài viết cần thu thập.
        :return: Một dictionary chứa thông tin bài viết (tiêu đề, nội dung, bình luận).
        """
        try:
            self.driver.get(article_url)
            time.sleep(3)

            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            try:
                title = self.driver.find_element(By.CSS_SELECTOR, ".p-title-value").text
            except:
                title = "Không thể lấy tiêu đề"

            try:
                main_content = self.driver.find_element(By.CSS_SELECTOR, ".message-body").text
            except:
                main_content = "Không thể lấy nội dung bài viết"

            comments = self.get_comments(self.driver)

            return {
                "title": title,
                "content": main_content,
                "comments": comments
            }

        except Exception as e:
            print(f"Error scraping article {article_url}: {e}")
            return None  

if __name__ == "__main__":
    symbol = "Grab" 
    scraper = ArticleScraper(symbol)
    print(scraper.scrape_articles())