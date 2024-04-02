import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


phone_type = input("기종을 입력해 주세요: ")
storage_size = input("원하시는 용량을 입력해 주세요 (128, 256, 512입력 가능): ")


while True:
    storage_size = input("원하시는 용량을 입력해 주세요 (128, 256, 512입력 가능): ")
    if storage_size in ("128", "256", "512"):
        break
    else: 
        print("다시 시도해 주세요.")



#최대/최소 가격 입력값 코드 (적용 여부?)
'''
while True:
    min_price_str = input("최소 가격을 입력해 주세요: ")
    try:
        min_price = int(min_price_str)
        break  # Exit the loop if conversion is successful
    except ValueError:
        print("숫자를 입력하세요. 다시 시도해 주세요.")

while True:
    max_price_str = input("최대 가격을 입력해 주세요: ")
    try:
        max_price = int(min_price_str)
        break  # Exit the loop if conversion is successful
    except ValueError:
        print("숫자를 입력하세요. 다시 시도해 주세요.")
'''

url_layout = "https://m.bunjang.co.kr/search/products?order=score&page={}&q={} {}"
urls = [url_layout.format(page_no,phone_type,storage_size) for page_no in range(1,11)]


#셀리움 사용해서 번개장터 들어가기
option = webdriver.ChromeOptions()
option.add_argument("--headless")
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service = service, options = option)


#데이터프레임 만들기
df = pd.DataFrame(columns = ['Title', 'Price','Link'])

#각각 url에서 제목, 가격, 링크 크콜링
for url in urls:
    browser.get(url)
    time.sleep(random.uniform(1,2))
    title_list = browser.find_elements(By.CLASS_NAME,"sc-iBEsjs.fqRSdX")
    price_list = browser.find_elements(By.CLASS_NAME,"sc-hzNEM.bmEaky")
    link_list = browser.find_elements(By.CLASS_NAME,"sc-jKVCRD.bqiLXa")

    #타이틀, 가격, 링크 dataframe에 추가해서 넣기
    data = {
        'Title': [title.text for title in title_list],
        'Price': [int(price.text.replace('$', '').replace(',', '')) for price in price_list],
        'Link': [link.get_attribute("href").split("?q")[0] for link in link_list]
    }
    df_add= pd.DataFrame(data)

    #최대/최소값 적용
    df_add.drop(df_add[df_add['Price'] < 200000].index, inplace=True)
    df_add.drop(df_add[df_add['Price'] > 2000000].index, inplace=True)
    #df_add.drop(df_add[df_add['Price'] < min_price].index, inplace=True)
    #df_add.drop(df_add[df_add['Price'] > max_price].index, inplace=True)
    #df_add.reset_index(drop=True, inplace=True)

    #페이지 dataframe을 전체dataframe에 추가 (append함수 사용 대신 concat사용함)
    df = pd.concat([df, df_add], ignore_index=True)

#csv파일로 export하기
file_path = f'{phone_type}_{storage_size}_정보.csv'
df.to_csv(file_path, index = True)