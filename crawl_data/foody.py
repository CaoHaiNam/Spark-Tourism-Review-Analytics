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

class AutoGenerator(object):
    def __init__(self):
        self.data = dict()
        self.resp_list = list()
        self.driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)

    def get_comment_detail(self, data=None, location=None):
        try:
            PAUSE_TIME = 3
            category = data.get("category")
            link = data.get("link")
            count_comment = data.get("count_comment")
            address = data.get("address")
            list_comment = []
            if link and count_comment:
                url = link + "/binh-luan"
                self.driver.get(url)
                WebDriverWait(self.driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.list-reviews')))
                # time.sleep(PAUSE_TIME)

                last_height = self.driver.execute_script("return document.body.scrollHeight")
                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(PAUSE_TIME)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                while True:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, '.pn-loadmore')
                        if element.is_displayed():
                            element.click()
                            time.sleep(PAUSE_TIME)

                    except NoSuchElementException:
                        break

                comments = self.driver.find_elements(By.CSS_SELECTOR, 'div.list-reviews > div > ul > li')
                if comments:
                    for comment in comments:
                        comment_score = comment.find_element(By.CSS_SELECTOR, "div.review-user.fd-clearbox.ng-scope > div:nth-child(2) > div.review-points.ng-scope > span").text
                        comment_text = comment.find_element(By.CSS_SELECTOR,
                                                 "div.review-des.fd-clearbox.ng-scope > div > span").text

                        list_comment.append({
                            "text": comment_text,
                            "score": comment_score
                        })

            if list_comment:
                ls = {
                    "category": category,
                    "link": link,
                    "count_comment": count_comment,
                    "address": address,
                    "comments": list_comment,
                }

                filename = './data/comment_foody/comment_{location}_{cate}.json'.format(location=location, cate=category)
                if not (os.path.exists(filename)):
                    with open(filename, "w") as jsf:
                        jsf.write(json.dumps([]))

                with open(filename) as fp:
                    listObj = json.load(fp)

                listObj.append(ls)

                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump(listObj, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)

                print(f'{link}')

        except Exception as e:
            pass

    def _insert_links_json(self, items=None, cate=None, platforms=None):
        try:
            if items:
                for i in items:
                    try:
                        link = i.find_element(By.CSS_SELECTOR, "div.ng-scope > a:nth-child(2)").get_attribute('href')
                        address = i.find_element(By.CSS_SELECTOR,
                                                 "div.ng-scope > a:nth-child(2) > div.address.limit-text.ng-binding").text

                        filename = './data/comment_foody/comment_{}.json'.format(cate)
                        if not (os.path.exists(filename)):
                            with open(filename, "w") as jsf:
                                jsf.write(json.dumps([]))

                        with open(filename) as fp:
                            listObj = json.load(fp)

                        listObj.append({
                            "category": cate,
                            "link": link,
                            "address": address
                        })

                        with open(filename, 'w', encoding='utf-8') as json_file:
                            json.dump(listObj, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)
                        print(f'{link} - {address}')

                    except Exception as e:
                        print(f'get element detail error: {e}')
                        pass

        except Exception as e:
            print(f'get element detail error: {e}')
            pass

    def get_foody_urls(self, category=None, location=None):
        try:
            print(category)
            platforms = "https://www.foody.vn"
            location = location
            cate = category["category"]
            url = category["url"]
            SCROLL_PAUSE_TIME = 3
            # driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)
            self.driver.get(url)
            WebDriverWait(self.driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#box-delivery')))

            # driver.find_element(By.CSS_SELECTOR, '.nav-box > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1) > span:nth-child(1)').click()
            # time.sleep(4)
            # home1 = driver.find_elements(By.CSS_SELECTOR, '#box-delivery > div.n-listitems > ul > li')
            # self._insert_links_json(items=home1, cate=cate)

            # while True:
            #     try:
            #         WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.li-page'))).click()
            #         time.sleep(4)
            #         home1 = driver.find_elements(By.CSS_SELECTOR, '#box-delivery > div.n-listitems > ul > li')
            #         print(f'len item home1: {len(home1)}')
            #         self._insert_links_json(items=home1, cate=cate)
            #
            #     except NoSuchElementException:
            #         break

            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            WebDriverWait(self.driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ajaxRequestDiv > div > div.content-container.fd-clearbox.ng-scope > div')))
            home2 = self.driver.find_elements(By.CSS_SELECTOR, '#ajaxRequestDiv > div > div.content-container.fd-clearbox.ng-scope > div')
            print(f'len item home2: {len(home2)}')

            for i in home2:
                try:
                    try:
                        count_comment = i.find_element(By.CSS_SELECTOR, "div > div.items-count > a > span").text
                    except:
                        count_comment = 0

                    try:
                        link = i.find_element(By.CSS_SELECTOR, "div.items-content.hide-points > div.title.fd-text-ellip > a").get_attribute('href')
                    except:
                        link = ""

                    try:
                        address = i.find_element(By.CSS_SELECTOR, "div.items-content.hide-points > div.desc.fd-text-ellip.ng-binding").text
                    except:
                        address = ""

                    filename = './data/comment_foody/comment_{location}_{cate}.json'.format(location=location, cate=cate)
                    if not (os.path.exists(filename)):
                        with open(filename, "w") as jsf:
                            jsf.write(json.dumps([]))

                    with open(filename) as fp:
                        listObj = json.load(fp)

                    listObj.append({
                        "category": cate,
                        "link": link,
                        "address": address,
                        "count_comment": count_comment
                    })

                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(listObj, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)
                    print(f'{link} - {address} - {count_comment}')

                except Exception as e:
                    print(f'get element detail error: {e}')
                    pass

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"

        except NoSuchElementException:
            print(f'No element were found matching your selection')

        except ElementClickInterceptedException:
            print(f"Can't click to element your selection")

    def get_comment_foody(self, brand_name=None, description=None):
        try:
            count_text = 0
            brand_name = brand_name
            description = description

            if brand_name and description:
                description_en = translate(f'{description.replace(".", ",").replace("?", ",").replace("!", ",")}', 'en')
                description_en = description_en.replace(']', '').replace('[', '').replace("'vi'", '').replace(';', '').replace("',",
                                                                                                                               "'").replace(
                    ",'", ".'").replace("'", '')

                login_url = "https://app.peppertype.ai/signin"
                description_url = "https://app.peppertype.ai/create/brand-product-descriptions"

                config = [{
                        'EMAIL': 'seamen728@gmail.com',
                        'PASSWORD': '123456c@'
                    },
                    {
                        'EMAIL': 'mensea700@gmail.com',
                        'PASSWORD': '123456c@'
                    },
                ]

                account = random.choice(config)

                driver = webdriver.Chrome(path_chrome_driver, options=chrome_options, desired_capabilities=capabilities)
                # driver = webdriver.Chrome(path_chrome_driver, options=chrome_options)
                driver.get(login_url)
                elem = WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.NAME, 'username')))
                elem.clear()
                elem.send_keys(account['EMAIL'])
                elem = WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.NAME, 'password')))
                elem.clear()
                elem.send_keys(account['PASSWORD'])
                elem.send_keys(Keys.RETURN)
                WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section/main/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/button')))
                # time.sleep(7)

                driver.get(description_url)
                element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rc_select_4"]')))
                ActionChains(driver).send_keys(brand_name).perform()
                element.clear()
                element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="description"]')))
                element.send_keys(description_en)
                element.clear()
                WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/section/main/div/div/div[1]/div/div[1]/div/form/div[4]/button'))).click()
                WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CLASS_NAME, 'styles_activateEdit__46YPk')))
                texts = driver.find_elements(By.CLASS_NAME, 'styles_activateEdit__46YPk')

                for i in texts:
                    text = i.text
                    text_vi = translate(f'{text.replace(".", ",").replace("!", "").replace("?", "").replace("`", "").replace("|", "")}', 'vi')
                    text_vi = text_vi.replace(']', '').replace('[', '').replace("'en'", '').replace(';', '').replace(
                        "',", "'").replace(",'", ".'").replace("'", '')
                    self.resp_list.append(str(text_vi).strip())
                    count_text += 1

                    if count_text == 10:
                        break

                #print(self.resp_list)
                driver.close()
                self.data["results"] = self.resp_list
                self.data["message"] = 200
            else:
                self.data["results"] = "Brand name or description is null"
                self.data["message"] = 401

        except TimeoutException:
            print(f'error timeout or over 10000 characters')
            self.data["message"] = 401
            self.data["results"] = "Error timeout or over 10000 characters"

        except NoSuchElementException:
            print(f'No element were found matching your selection')

        except ElementClickInterceptedException:
            print(f"Can't click to element your selection")

        return self.data


def crawl_urls_comments():
    crawler = AutoGenerator()

    locations = ["ho-chi-minh", "ha-noi", "da-nang", "can-tho", "khanh-hoa", "vung-tau", "hai-phong", "binh-thuan",
                 "lam-dong", "dong-nai", "quang-ninh", "hue", "binh-duong", "hai-duong", "ninh-thuan", "nam-dinh",
                 "tien-giang", "phu-quoc", "kon-tum", "lao-cai", "quang-nam", "nghe-an", "long-an", "dien-bien",
                 "binh-dinh", "thanh-hoa", "phu-yen", "dak-lak", "an-giang", "thai-nguyen", "bac-ninh", "kien-giang",
                 "quang-ngai", "tay-ninh", "gia-lai", "binh-phuoc", "vinh-long", "ca-mau", "dong-thap", "quang-tri",
                 "quang-binh", "hoa-binh", "vinh-phuc", "ben-tre", "thai-binh", "soc-trang", "ninh-binh", "tra-vinh",
                 "bac-giang", "hung-yen", "bac-lieu", "ha-tinh", "phu-tho", "hau-giang", "son-la", "lang-son",
                 "dak-nong", "ha-nam", "ha-giang", "tuyen-quang", "yen-bai", "cao-bang", "bac-kan", "lai-chau"]

    for location in locations:
        categories = [
            {"category": "foods", "url": f"https://www.foody.vn/{location}"},
            {"category": "travel", "url": f"https://www.foody.vn/{location}/travel"},
            {"category": "wedding", "url": f"https://www.foody.vn/{location}/wedding"},
            {"category": "beauty", "url": f"https://www.foody.vn/{location}/beauty"},
            {"category": "entertain", "url": f"https://www.foody.vn/{location}/entertain"},
            {"category": "shop", "url": f"https://www.foody.vn/{location}/shop"},
            {"category": "edu", "url": f"https://www.foody.vn/{location}/edu"},
            {"category": "service", "url": f"https://www.foody.vn/{location}/service"},
        ]

        for i in categories:
            crawler.get_foody_urls(category=i, location=location)


def crawl_comment_detail():
    crawler = AutoGenerator()
    location_blacklist = list(set([str(file.name).split("_")[1] for file in list(Path("./data/comments_detail/").glob("*.json"))]))
    file_list = list(Path("./data/comment_foody/").glob("*.json"))
    for index, file in enumerate(file_list):
        location = str(file.name).split("_")[1]
        if location not in location_blacklist:
            with open(file, 'r', encoding='utf-8') as json_file:
                data = json.loads(json_file.read())
                for line in data:
                    crawler.get_comment_detail(data=line, location=location)


if __name__ == '__main__':
    crawl_comment_detail()