# File: scrape_openrice.py
import requests
from bs4 import BeautifulSoup
import json
import time

# 目標 OpenRice 網頁（請根據需要修改 URL）
url = "https://www.openrice.com/zh/hongkong/restaurants"  

# 設定 headers 模擬瀏覽器訪問
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/90.0.4430.93 Safari/537.36"
}

# 發送 HTTP 請求
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("無法訪問網頁，狀態碼：", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# 根據實際網頁結構選取元素 (以下假設每個餐廳資料位於 class="restaurant-item")
restaurants = soup.select(".restaurant-item")

data_list = []
for item in restaurants:
    # 根據網頁結構抽取資料，請根據實際情況修改 CSS Selector
    name_element = item.select_one(".restaurant-name")
    address_element = item.select_one(".restaurant-address")
    rating_element = item.select_one(".restaurant-rating")
    
    name = name_element.get_text(strip=True) if name_element else "N/A"
    address = address_element.get_text(strip=True) if address_element else "N/A"
    rating = rating_element.get_text(strip=True) if rating_element else "N/A"

    data_list.append({
        "name": name,
        "address": address,
        "rating": rating
    })
    # 加入延時，避免請求太快 (可根據需求調整)
    time.sleep(0.5)

# 儲存結果到 JSON 檔案
with open("openrice_data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=2)

print("成功將資料儲存到 openrice_data.json")