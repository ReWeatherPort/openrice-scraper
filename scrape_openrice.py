#!/usr/bin/env python3
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_page_source(url):
    """
    使用 Selenium 抓取指定 URL 嘅頁面 HTML
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/115.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("打開 URL：", url)
    driver.get(url)
    
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    
    html = driver.page_source
    driver.quit()
    return html

def parse_dataset(html):
    """
    使用 BeautifulSoup 解析 HTML，提取更多餐廳資訊
    """
    soup = BeautifulSoup(html, "html.parser")
    records = []
    
    containers = soup.select("div.poi-list-cell-desktop-right-top-wrapper-main")
    if not containers:
        print("未能依據選擇器找到任何餐廳容器，請檢查 HTML 結構!")
    
    for container in containers:
        # 餐廳名稱
        name_elem = container.select_one("div.poi-name")
        if not name_elem:
            continue
        name = name_elem.get_text(strip=True)
        
        # 菜系、種類、價位
        info_container = container.select_one("div.poi-list-cell-line-info")
        if info_container:
            spans = info_container.select("span.poi-list-cell-line-info-link")
            if len(spans) >= 4:
                cuisine = spans[1].get_text(strip=True)
                dish_type = spans[2].get_text(strip=True)
                price = spans[3].get_text(strip=True)
            else:
                cuisine = dish_type = price = ""
        else:
            cuisine = dish_type = price = ""
        
        # 評分
        rating_elem = container.select_one("span.score")
        rating = float(rating_elem.get_text(strip=True)) if rating_elem else 0.0
        
        # 評論數量
        review_elem = container.select_one("span.review-count")
        review_count = int(review_elem.get_text(strip=True).replace("則", "")) if review_elem else 0
        
        # 電話（假設喺某個元素中，可能需要點擊進入餐廳詳情頁）
        phone_elem = container.select_one("span.phone-number")
        phone = phone_elem.get_text(strip=True) if phone_elem else ""
        
        # 營業時間
        hours_elem = container.select_one("span.opening-hours")
        opening_hours = hours_elem.get_text(strip=True) if hours_elem else ""
        
        # 特色菜式（假設喺某個標籤中）
        special_dish_elem = container.select_one("span.special-dish")
        special_dish = special_dish_elem.get_text(strip=True) if special_dish_elem else ""
        
        # 圖片 URL
        image_elem = container.select_one("img.restaurant-image")
        image_url = image_elem['src'] if image_elem and 'src' in image_elem.attrs else ""
        
        # 僅保留完整資料
        if name and cuisine and dish_type and price:
            records.append({
                "name": name,
                "cuisine": cuisine,
                "type": dish_type,
                "price": price,
                "phone": phone,
                "opening_hours": opening_hours,
                "rating": rating,
                "review_count": review_count,
                "special_dish": special_dish,
                "image_url": image_url
            })
        else:
            print("資料不完整，跳過：", name)
            
    return records

def main():
    url = "https://www.openrice.com/zh/hongkong/restaurants/district/%E7%9F%B3%E5%A1%98%E5%92%80?sortBy=ORScoreDesc"
    html = fetch_page_source(url)
    
    dataset = parse_dataset(html)
    if dataset:
        with open("openrice_data.json", "w", encoding="utf8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
        print("抓取完成，數據已存入 openrice_data.json")
        print("數據內容：")
        for rec in dataset:
            print(rec["name"], rec["cuisine"], rec["type"], rec["price"], rec["rating"], rec["review_count"])
    else:
        print("未提取到任何餐廳資料。")

if __name__ == "__main__":
    main()