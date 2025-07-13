import requests

with open("test.mov", "rb") as f:
    files = {"video": ("test.mov", f, "video/mp4")}
    print("▶ 上傳影片到 /detect/")
    res = requests.post("http://localhost:8001/detect/", files=files)

if res.status_code != 200:
    print("❌ detect 失敗:", res.text)
else:
    session_id = res.json().get("session_id")
    print("✅ detect 成功, session_id =", session_id)

    # 執行 lama
    print("▶ 呼叫 /inpaint/")
    r = requests.post("http://localhost:8001/inpaint/", data={"session_id": session_id})
    if r.status_code == 200:
        print("✅ inpaint 成功")
    else:
        print("❌ inpaint 失敗:", r.text)

    # 執行 lama
    print("▶ 呼叫 /get_model/")
    r = requests.post("http://localhost:8001/get_model/", data={"session_id": session_id})
    if r.status_code == 200:
        print("✅ get_model 成功")
    else:
        print("❌ get_model 失敗:", r.text)
