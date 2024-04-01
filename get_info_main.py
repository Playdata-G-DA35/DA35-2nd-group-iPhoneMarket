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

phone_type = input("기종을 입력해주세요")
url_layout = "https://m.bunjang.co.kr/search/products?order=score&page={}&q={}"
urls = [url_layout.format(page_no, phone_type) for page_no in range(1,11)]


#셀리움 사용해서 번개장터 들어가기
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service = service)


#데이터프레임 만들기
df = pd.DataFrame(columns = ['Title', 'Price','Link'])

for url in urls:
    browser.get(url)
    time.sleep(random.uniform(1,2))
    #타이틀 정보 가져오기, dataframe에 저장
    title_list = browser.find_elements(By.CLASS_NAME,"sc-iBEsjs.fqRSdX")
    #print(len(title_list))
    #for title in title_list:
        #print(title.text)

    #가격 가져오기
    #string값 -> 정수로 값 반환 필요
    price_list = browser.find_elements(By.CLASS_NAME,"sc-hzNEM.bmEaky")
    #print(len(price_list))
    #for price in price_list:
    #    print(price.text)

    #링크 가져오기
    link_list = browser.find_elements(By.CLASS_NAME,"sc-jKVCRD.bqiLXa")
    #print(len(link_list))
    #for link in link_list:
    #    print(link.get_attribute("href").split("?q")[0])


    #타이틀, 가격, 링크 dataframe에 추가해서 넣기
    data = {
        'Title': [title.text for title in title_list],
        'Price': [int(price.text.replace('$', '').replace(',', '')) for price in price_list],
        'Link': [link.get_attribute("href").split("?q")[0] for link in link_list]
    }

    df_add= pd.DataFrame(data)

    df_add.drop(df_add[df_add['Price'] < 200000].index, inplace=True)
    df_add.reset_index(drop=True, inplace=True)

    #페이지 dataframe을 전체dataframe에 추가 (append사용 대신 concat사용)
    df = pd.concat([df, df_add], ignore_index=True)


file_path = 'test1.csv'
df.to_csv(file_path, index = True)