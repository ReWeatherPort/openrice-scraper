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
    # 設定 Chrome 無頭模式
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
    
    # 等待 5 秒以確保大部分動態內容載入
    time.sleep(5)
    
    # 模擬頁面滾動，促使 lazy load 資料出現
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    
    html = driver.page_source
    driver.quit()
    return html

def parse_dataset(html):
    """
    使用 BeautifulSoup 解析 HTML，並提取餐廳名稱與菜系/種類/價位信息  
    依據你提供的範例，假設提取邏輯如下：  
      - 餐廳名稱位於 div.poi-name 中。  
      - 其他信息位於包含 class "poi-list-cell-line-info" 的元素裏，其內部
        <span class="poi-list-cell-line-info-link"> 依序包含：  
          [0] 地區 (例如：西環) → 忽略  
          [1] 菜系 (例如：日本菜 或 港式)  
          [2] 種類 (例如：拉麵 或 粉麵/米線)  
          [3] 價位 (例如：$51-100 或 $50以下)
    """
    soup = BeautifulSoup(html, "html.parser")
    records = []
    
    # 根據實際情況，此處以 'div.poi-list-cell-desktop-right-top-wrapper-main'
    # 作為每筆資料的父容器（觀察提供的部分 HTML 可知，餐廳名稱與資訊都在此區域）
    containers = soup.select("div.poi-list-cell-desktop-right-top-wrapper-main")
    if not containers:
        print("未能依據選擇器找到任何餐廳容器, 請檢查 HTML 結構!")
    
    for container in containers:
        # 嘗試從 container 中取得餐廳名稱
        name_elem = container.select_one("div.poi-name")
        if not name_elem:
            continue
        name = name_elem.get_text(strip=True)
        
        # 嘗試抓取包含「菜系/種類/價位」信息的容器（此處包含在 div.poi-list-cell-line-info）
        info_container = container.select_one("div.poi-list-cell-line-info")
        if info_container:
            spans = info_container.select("span.poi-list-cell-line-info-link")
            # 預期至少 4 個 span: [0] 地區、[1] 菜系、[2] 種類、[3] 價位
            if len(spans) >= 4:
                cuisine = spans[1].get_text(strip=True)
                dish_type = spans[2].get_text(strip=True)
                price = spans[3].get_text(strip=True)
            else:
                cuisine = dish_type = price = ""
        else:
            cuisine = dish_type = price = ""
        
        # 僅保留符合預期的資料
        if name and cuisine and dish_type and price:
            records.append({
                "name": name,
                "cuisine": cuisine,
                "type": dish_type,
                "price": price
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
            # 根據你的需求，只展示部分（例如：彩aya  日本菜  拉麵  $51-100）
            print(rec["name"], rec["cuisine"], rec["type"], rec["price"])
    else:
        print("未提取到任何餐廳資料。")

if __name__ == "__main__":
    main()