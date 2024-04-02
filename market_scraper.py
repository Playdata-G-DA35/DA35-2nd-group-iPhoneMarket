import os
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class MarketInfoScraper:
    def __init__(self):
        self.browser = None

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

    def stop_browser(self):
        if self.browser:
            self.browser.quit()

    def scrape_market_info(self, phone_type, storage_size):
        url_layout = "https://m.bunjang.co.kr/search/products?order=score&page={}&q={} {}"
        urls = [url_layout.format(page_no, phone_type, storage_size) for page_no in range(1, 11)]
        df = pd.DataFrame(columns=['Title', 'Price', 'Link'])

        for url in urls:
            self.browser.get(url)
            time.sleep(random.uniform(1, 2))
            title_list = self.browser.find_elements(By.CLASS_NAME, "sc-iBEsjs.fqRSdX")
            price_list = self.browser.find_elements(By.CLASS_NAME, "sc-hzNEM.bmEaky")
            link_list = self.browser.find_elements(By.CLASS_NAME, "sc-jKVCRD.bqiLXa")

            data = {
                'Title': [title.text for title in title_list],
                'Price': [int(price.text.replace('$', '').replace(',', '')) for price in price_list],
                'Link': [link.get_attribute("href").split("?q")[0] for link in link_list]
            }
            df_add = pd.DataFrame(data)

            df_add.drop(df_add[df_add['Price'] < 200000].index, inplace=True)
            df_add.drop(df_add[df_add['Price'] > 2000000].index, inplace=True)

            df = pd.concat([df, df_add], ignore_index=True)

        return df

    def save_market_info_csv(self, df, phone_type, storage_size):
        if not os.path.exists('market_info'):
            os.makedirs('market_info')

        file_path = f'market_info/{phone_type}_{storage_size}_정보.csv'
        df.to_csv(file_path, index=True)
        return file_path

    def plot_price_distribution(self, df, phone_type, storage_size):
        val = df['Price'].value_counts().sort_index()
        X = val.index.tolist()
        Y = val.values.tolist()

        cnt_list = [0 for _ in range(0, 19)]
        for i in range(len(X)):
            idx = X[i] // 100000 - 2
            cnt_list[idx] += Y[i]

        plt.title(f'<iPhone{phone_type} / {storage_size}gb>')
        plt.xlabel('price')
        plt.ylabel('amount')

        ax = plt.subplot(111)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.patch.set_facecolor('lightgrey')
        ax.patch.set_alpha(0.2)
        ax.grid(True)

        plt.plot(cnt_list, 'k', c='green', label='price')
        plt.legend()
        plt.xticks(range(0, len(cnt_list), 2), ['20', '40', '60', '80', '100', '120', '140', '160', '180', '200'], size=10)
        plt.yticks(size=10)

        plt.savefig(f'{phone_type}_{storage_size}_그래프.png')


def main():
    phone_type = input("기종을 입력해 주세요: ")

    while True:
        storage_size = input("원하시는 용량을 입력해 주세요 (128, 256, 512입력 가능): ")
        if storage_size in ("128", "256", "512"):
            break
        else:
            print("다시 시도해 주세요.")

    scraper = MarketInfoScraper()
    scraper.start_browser()
    try:
        df = scraper.scrape_market_info(phone_type, storage_size)
        csv_file = scraper.save_market_info_csv(df, phone_type, storage_size)
        scraper.plot_price_distribution(df, phone_type, storage_size)
        print(f"Market info saved to: {csv_file}")
    finally:
        scraper.stop_browser()


if __name__ == "__main__":
    main()
