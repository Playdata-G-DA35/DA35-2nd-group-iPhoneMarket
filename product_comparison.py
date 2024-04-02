import pandas as pd
import matplotlib.pyplot as plt
from market_scraper import MarketInfoScraper

size1 = input("1 사이즈")
type1 = input("1 타입")
size2 = input("2 사이즈")
type2 = input("2 타입")
size3 = input("3 사이즈")
type3 = input("3 타입")

info = [('blue', size1, type1), ('green', size2, type2), ('red', size3, type3)]

scraper = MarketInfoScraper()  # Create an instance of MarketInfoScraper
scraper.start_browser()  # Start the browser


for color, storage_size, phone_type in info:
    df = scraper.scrape_market_info(phone_type, storage_size)
    tmp = df['Price'].value_counts().sort_index()

    X = tmp.index.tolist()
    Y = tmp.values.tolist()

    cnt_list = [0 for i in range(0,19)]
    for j in range(len(X)):
        idx = X[j] // 100000 - 2
        cnt_list[idx] += Y[j]



    plt.plot(cnt_list, 'k', c=color, label=phone_type +" "+storage_size+'GB')
    plt.legend()
    plt.xticks(range(0, len(cnt_list), 2), ['20', '40', '60', '80', '100', '120', '140', '160', '180', '200'], size=10)


phone_type_new = phone_type.split("폰")[1]
plt.title('Product Comparison')
plt.xlabel('price')
plt.ylabel('amount')
plt.show()


