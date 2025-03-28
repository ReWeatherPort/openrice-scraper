import requests
from bs4 import BeautifulSoup
import json

# 目標網頁（示例網址，請根據需要修改）
url = "https://www.openrice.com/zh/hongkong/restaurants" 

# 設定 headers 以模擬瀏覽器訪問
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/90.0.4430.93 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("無法訪問網頁，狀態碼：", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# 假設餐廳資訊位於 class="restaurant-item" ，根據實際頁面修改 selector
restaurants = soup.select(".restaurant-item")

data_list = []

for item in restaurants:
    # 根據實際結構選取資料
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

# 將數據儲存到 JSON 檔案
with open("openrice_data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=2)

print("數據已成功儲存到 openrice_data.json")