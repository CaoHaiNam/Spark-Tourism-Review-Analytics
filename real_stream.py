import os
import re
import time
import random
import json
from glob import glob
from pathlib import Path
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver import DesiredCapabilities
import sys

chrome_options = ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--incognito')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options.add_argument(f'--user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option('w3c', False)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--allow-running-insecure-content')

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['browserName'] = 'chrome'
capabilities['chromeOptions'] = {'args': ['no-sandbox']}
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
path_chrome_driver = os.path.abspath("chromedriver_linux64/chromedriver")

link_us = [
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/saigon-waterbus-tickets-2000038451947",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/hanoi-shuttle-bus-round-trip-transfer-to-sapa-2001792892682",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/hanoi-shuttle-bus-transfer-to-sapa-2001791129188",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/han-river-by-night-on-my-xuan-cruise-2001540807078",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/saigon-hop-on-hop-off-bus-pass-2001438308062",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/sapa-shuttle-bus-transfer-to-hanoi-2001791129180",
           "https://www.traveloka.com/vi-vn/activities/vietnam/product/ho-chi-minh-city-speedboat-transfer-to-vung-tau-city-2001591261755",
           "https://www.traveloka.com/vi-vn/activities/singapore/product/singapore-tourist-pass-plus-1000282396981",
           "https://www.traveloka.com/vi-vn/activities/singapore/product/changi-airport-private-car-transfers-2001180496514",
           "https://www.traveloka.com/vi-vn/activities/indonesia/product/sewa-motor-rental-di-kuta-bali-untuk-2-hari-2000485976393",
           ""
           ]


class AutoGenerator(object):
    def __init__(self):
        self.data = dict()
        self.resp_list = list()
        self.driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)

    def get_traveloka_comment(self, link_url=None, location=None, page=None):
        try:
            platforms = "https://www.traveloka.com"
            location = location
            ls_comment = []
            list_cmm = []
            cate = "van-tai"
            url = link_url
            SCROLL_PAUSE_TIME = 2
            self.driver.get(url)
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script("window.scrollTo(177, document.body.scrollHeight);")

            WebDriverWait(self.driver, 200).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-1dbjc4n.r-14lw9ot.r-tskmnb')))

            comment1 = self.driver.find_elements(By.CSS_SELECTOR, 'div.r-1xlxj57 > div')
            # print(comment1)
            # return

            try:
                count_comment = self.driver.find_element(By.CSS_SELECTOR, ".css-901oao.r-cwxd7f.r-1sixt3s.r-ubezar.r-majxgm.r-135wba7.r-1wzrnnt.r-fdjqy7").text
                count_comment = int(re.findall(r'\d+', count_comment)[0])
            except:
                count_comment = 0

            # ls_comment.extend(comment1)

            for i in comment1:
                text = i.find_element(By.CSS_SELECTOR,
                                      "div.css-901oao.r-cwxd7f.r-1sixt3s.r-ubezar.r-majxgm.r-135wba7.r-fdjqy7").text
                if text != '':
                    print(f'1:  {text}')
                # sys.exit()

            count = 0
            while True:
                try:
                    nextButton = self.driver.find_element(By.CSS_SELECTOR, "#__next > div.css-1dbjc4n.r-391gc0.r-bnwqim.r-13qz1uu.r-1e2svnr > div.css-1dbjc4n.r-6koalj.r-18u37iz.r-1777fci.r-13qz1uu.r-184en5c > div > div.css-1dbjc4n.r-eqz5dr.r-dj2ral > div:nth-child(4) > div.css-1dbjc4n.r-1kihuf0.r-11c0sde > div > div.css-18t94o4.css-1dbjc4n.r-1ihkh82.r-kdyh1x.r-1loqt21.r-61z16t.r-ero68b.r-vkv6oe.r-10paoce.r-1e081e0.r-5njf8e.r-1otgn73.r-lrvibr")
                    self.driver.execute_script('arguments[0].click();', nextButton)
                    time.sleep(4)
                    comment = self.driver.find_elements(By.CSS_SELECTOR, 'div.r-1xlxj57 > div')
                    count += 1
                    if comment:
                        for i in comment:
                            text = i.find_element(By.CSS_SELECTOR,
                                                     "div.css-901oao.r-cwxd7f.r-1sixt3s.r-ubezar.r-majxgm.r-135wba7.r-fdjqy7").text
                            star = i.find_element(By.CSS_SELECTOR, "div > h1").text
                            if text != '':
                                print(f'2:  {text}')
                
                    if count == 30:
                        break

                except NoSuchElementException:
                    break

                except TimeoutException:
                    print('timeout')
                    break

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"

        except NoSuchElementException:
            print(f'No element were found matching your selection')

        except ElementClickInterceptedException:
            print(f"Can't click to element your selection")


def comment_travolaka():
    page = 0
    crawler = AutoGenerator()
    for i in link_us:
        page += 1
        crawler.get_traveloka_comment(link_url=i, page=page)

if __name__ == '__main__':
    comment_travolaka()