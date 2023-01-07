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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver import DesiredCapabilities

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
path_chrome_driver = os.path.abspath("chromedrive_linux64/chromedriver")

link_us = [
           "https://www.booking.com/hotel/vn/raon-valley-villa.vi.html",
           "https://www.booking.com/hotel/vn/nhat-huy-bungalow.vi.html",
           "https://www.booking.com/hotel/vn/tigon-dalat-hostel-thanh-pho-da-lat12.vi.html",
           "https://www.booking.com/hotel/vn/noel.vi.html",
           "https://www.booking.com/hotel/vn/queen-t-amp-t-dalat.vi.html",
           "https://www.booking.com/hotel/vn/khanh-uyen.vi.html",
           "https://www.booking.com/hotel/vn/nhim-house-thanh-pho-da-lat.vi.html",
           "https://www.booking.com/hotel/vn/thien-ha-thanh-pho-da-lat.vi.html",
           "https://www.booking.com/hotel/vn/bungalow-mai-phuong-binh.vi.html",
           "https://www.booking.com/hotel/vn/tasme.vi.html",
           "https://www.booking.com/hotel/vn/seven-a.vi.html",
           "https://www.booking.com/hotel/vn/coco-palm-resort-phu-quoc.vi.html",
           "https://www.booking.com/hotel/vn/novotel-phu-quoc-resort.vi.html",
           "https://www.booking.com/hotel/vn/best-western-premier-sonasea-phu-quoc.vi.html",
           "https://www.booking.com/hotel/vn/lahana-resort.vi.html",
           "https://www.booking.com/hotel/vn/premier-residences-phu-quoc-emerald-bay.vi.html",
           "https://www.booking.com/hotel/vn/nadine-phu-quoc-resort.vi.html",
           "https://www.booking.com/hotel/vn/movenpick-resort-waverly-phu-quoc.vi.html",
           "https://www.booking.com/hotel/vn/sasco-blue-lagoon-resort-amp-spa.vi.html",
           "https://www.booking.com/hotel/vn/dusit-princess-moonrise-beach-resort.vi.html",
           "https://www.booking.com/hotel/vn/m-phu-quoc.vi.html",
           "https://www.booking.com/hotel/vn/the-vibe-house.vi.html",
           ]


class AutoGenerator(object):
    def __init__(self):
        self.data = dict()
        self.resp_list = list()
        self.driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)

    def get_booking_comment(self, link_url=None, location=None, page=None):
        try:
            
            platforms = "https://www.booking.com"
            cate = "khach-san"
            url = link_url
            SCROLL_PAUSE_TIME = 2
            self.driver.get(url)
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script("window.scrollTo(177, document.body.scrollHeight);")

            review_elemen = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.hp-review-score-cta-remote')))
            print(1111111111111111111)
            review_elemen.click()
            time.sleep(4)
            

            while True:
                try:
                    comment1 = self.driver.find_elements(By.CSS_SELECTOR, '#review_list_page_container > ul > li')
                    if comment1:
                        for i in comment1:
                            try:
                                text = i.find_element(By.CSS_SELECTOR,
                                                       "p > span.c-review__body").text

                                rating = i.find_element(By.CSS_SELECTOR, "div.bui-grid__column-2.bui-u-text-right > div > div").text

                                if text and rating:
                                    filename = './data/comment_booking/comment_{cate}_{page}.json'.format(cate=cate, page=page)
                                    if not (os.path.exists(filename)):
                                        with open(filename, "w") as jsf:
                                            jsf.write(json.dumps([]))

                                    with open(filename) as fp:
                                        listObj = json.load(fp)

                                    listObj.append({
                                        "category": cate,
                                        "link": url,
                                        "comments": text,
                                        "rating": rating
                                    })

                                    with open(filename, 'w', encoding='utf-8') as json_file:
                                        json.dump(listObj, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)

                                    print(f'comment: {text} - {rating}')

                            except:
                                pass

                    print(len(comment1))

                    clk = WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div > div.bui-pagination__item.bui-pagination__next-arrow > a')))
                    clk.click()
                    time.sleep(4)

                except NoSuchElementException:
                    break

                except TimeoutException:
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
        crawler.get_booking_comment(link_url=i, page=page)


if __name__ == '__main__':
    comment_travolaka()