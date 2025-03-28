import json

# 讀取 JSON 數據
with open("openrice_data.json", "r", encoding="utf-8") as f:
    restaurants = json.load(f)

# 開始組合 HTML 內容
html_content = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenRice 餐廳資料</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }
        h1 { text-align: center; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background-color: #eee; }
        tr:nth-child(even) { background-color: #fafafa; }
    </style>
</head>
<body>
    <h1>OpenRice 餐廳資料</h1>
    <table>
        <tr>
            <th>餐廳名稱</th>
            <th>地址</th>
            <th>評分</th>
        </tr>
"""

# 將數據逐行寫入表格
for restaurant in restaurants:
    html_content += f"""
        <tr>
            <td>{restaurant['name']}</td>
            <td>{restaurant['address']}</td>
            <td>{restaurant['rating']}</td>
        </tr>
    """

html_content += """
    </table>
</body>
</html>
"""

# 儲存生成的 HTML 文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML 網站已生成: index.html")