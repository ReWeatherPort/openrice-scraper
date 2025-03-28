# OpenRice 餐廳探索

呢個項目包含：
- **資料抓取**：用 Python 抓取 OpenRice 嘅餐廳資料（`scrape_openrice.py`）。
- **前端網站**：顯示餐廳資料，具備搜尋、排序、篩選同隨機推薦功能（`index.html`、`assets/css/style.css` 同 `assets/js/main.js`）。
- **部署**：可以將項目推送至 GitHub 並利用 GitHub Pages 部署網站。

## 使用方法

1. **資料抓取**  
   運行以下命令以抓取資料並儲存到 `openrice_data.json`：
   ```bash
   python scrape_openrice.py