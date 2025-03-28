import os
import json
from flask import Flask, render_template, jsonify
import scrape_openrice

app = Flask(__name__, template_folder=".", static_folder=".")

# 全域變數儲存抓取到嘅資料
data = []

def load_data():
    global data
    # 如果 JSON 檔存在，就由檔案讀取
    if os.path.exists("openrice_data.json"):
        with open("openrice_data.json", "r", encoding="utf8") as f:
            data = json.load(f)
        print("由 openrice_data.json 載入資料。")
    else:
        # 否則進行抓取，並存入 JSON 檔
        data = scrape_openrice.get_dataset()
        with open("openrice_data.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("抓取完成，數據已存入 openrice_data.json。")

@app.route("/")
def index():
    global data
    # 初次訪問先嘗試由 JSON 檔載入或進行抓取
    if not data:
        load_data()
    return render_template("index.html", records=data)

@app.route("/api/data")
def api_data():
    global data
    return jsonify(data)

if __name__ == "__main__":
    # 部署開發階段：host 為 0.0.0.0，埠使用 5000，同 debug 模式開啟
    app.run(host="0.0.0.0", port=5000, debug=True)