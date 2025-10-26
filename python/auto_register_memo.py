import requests

# 自動登録するメモのリスト
memos = [
    {"title": "自動メモ1", "body": "これは自動登録されたメモです。"},
    {"title": "自動メモ2", "body": "Pythonスクリプトから登録。"},
    {"title": "自動メモ3", "body": "Flaskアプリのテスト用。"}
]

# FlaskアプリのエンドポイントURL
url = "http://localhost:5000/regist"

for memo in memos:
    response = requests.post(url, data=memo)
    if response.status_code == 200 or response.status_code == 302:
        print(f"登録成功: {memo['title']}")
    else:
        print(f"登録失敗: {memo['title']} (status: {response.status_code})")
