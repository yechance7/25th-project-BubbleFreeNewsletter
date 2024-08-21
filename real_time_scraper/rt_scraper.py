from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import json

# 로그인용
user_name = "filterbubble2024@gmail.com"
password = "Ybigta2024!"

class RTScraper:
    def __init__(self) -> None:
        self.url: str = 'https://www.bigkinds.or.kr/'
        self.url2: str = 'https://www.bigkinds.or.kr/v2/news/index.do'
        self.options = Options()
        self.save_dir = ""
        # self.options.add_argument("--headless")   # 활성시키면 background에서 실행
        self.driver = webdriver.Chrome(options=self.options)
        # self.driver.set_window_size(1920, 1080)
        self.wait = WebDriverWait(self.driver, 60)  # Explicit wait with a timeout of 10 seconds

    def scrap(self) -> None:
        try:
            #open URL
            self.driver.get(self.url)
            
            #로그인 먼저 해야됨.
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/button[1]'))).click()
            username_field = self.driver.find_element(By.XPATH, '//*[@id="login-user-id"]')
            username_field.send_keys(user_name)
            pw_filed = self.driver.find_element(By.XPATH, '//*[@id="login-user-password"]')
            pw_filed.send_keys(password)
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-btn"]/i'))).click()
            time.sleep(5)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-modal"]/div/div/div/div[4]/button[3]/i'))).click()
            
            # 크롤링 페이지로 리다이렏트
            self.driver.get(self.url2)
            
            # 날짜 선택 
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[1]/a'))).click()
            # 1일 
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="srch-tab1"]/div/div[1]/span[1]/label'))).click()
            time.sleep(1)
            
            #언론사 선택, 5개
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[3]/a'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_provider_list"]/li[1]/span/label'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_provider_list"]/li[4]/span/label'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_provider_list"]/li[9]/span/label'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_provider_list"]/li[10]/span/label'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_provider_list"]/li[11]/span/label'))).click()
            time.sleep(3)
            
            #삼세 검색 선택
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[3]/div[1]/a')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'start'});", element)
            element.click()
            #사설 선택
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-index-type-editorial"]')))
            element.click()
            time.sleep(3)
            
            #검색
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="detailSrch1"]/div[7]/div/button[2]')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'start'});", element)
            element.click()
            time.sleep(3)

            #다운로드
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-step-3"]')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest', inline: 'start'});", element)
            element.click()
            time.sleep(3)
            
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="analytics-data-download"]/div[3]/button')))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
            element.click()
            time.sleep(3)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Save the articles to a JSON file
            pass
            self.driver.quit()
