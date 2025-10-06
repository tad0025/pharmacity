from threading import Thread
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from time import sleep

def run():
    from os import system
    system('pip install requests')
Thread(target=run).start()

app = FastAPI()

@app.get("/")
def home():
    try:
        import requests
        return JSONResponse(content={'status': 'ok'}, status_code=200)
    except:
        return JSONResponse(content={'status': 'error', 'message': 'Module requests not installed yet, please try again in a few seconds.'}, status_code=500)

@app.get("/pha")
def pha():
    import requests, json
    from datetime import datetime

    BEARER_TOKEN = "Bearer eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJjcmF0IjoxNzU5NzYwOTc3LCJpYXQiOjE3NTk3NjA5NzcsImlzcyI6ImN1c3RvbWVyIiwianRpIjoiM2RiMDc5MmUtMjQxYi00YzQ4LTg5MDAtNGMxOWE1MDViZWY4IiwidXNlciI6eyJpZCI6NDcwNTExLCJraW5kIjoyLCJpc19hZG1pbiI6ZmFsc2UsInJvbGVzIjp7IjEiOiIwMDAwMDExIiwiMTM3IjoiMDEwMCIsIjE4IjoiMDAxMTExMTExMTEwMDAwMCIsIjIwIjoiMDAxMTEwMTAwIiwiMjAzIjoiMSIsIjIwOSI6IjEiLCIyMSI6IjAwMDAwMDEiLCIyMTYiOiIwMTExMTExMTEwMTExMTExMTExMTExMTExMTExMTExMTEwMCIsIjIxOSI6IjEiLCIyMzUiOiIxIiwiMjM2IjoiMSIsIjIzNyI6IjAxMDAwMDAwMCIsIjIzOSI6IjAxMTEwIiwiMjQwIjoiMDEwMCIsIjI0MyI6IjEiLCIyNDkiOiIxIiwiMjUwIjoiMSIsIjI2OSI6IjEiLCIyNzgiOiIxIiwiMjgyIjoiMSIsIjMyNyI6IjAxMTAwIiwiNTAiOiIwMDAwMDAwMDEwMCIsIjczIjoiMDAwMDAxMTAiLCI4MCI6IjAxMTExMCIsIjgxIjoiMSIsIjk2IjoiMDAwMDAwMTExMTExMDAifSwibmFtZSI6IktoYWNoIGhhbmciLCJleHRlcm5hbF9pZCI6IkswMTQ2ODU0NTQiLCJleHRlcm5hbF9kYXRhIjp7ImVtYWlsIjoiZGF0dDMyMjg1QGdtYWlsLmNvbSIsInBob25lIjoiMDM1OTUzNzk4MSIsInVzZXJfYWdlbnQiOiJva2h0dHAiLCJ1c2VyX2lkIjoiNTQ5OTE2OTYiLCJ1c2VybmFtZSI6IktoYWNoIGhhbmcifX19.piaBBy1be1kskxyHzGJ3FA1WDwcBCqgFVmN4adBYbAKjRliB_OQKEtN27RgFNXI_8YU8J--pGMcR0kiBamp5CA"
    BASE_URL = "https://api-gateway.pharmacity.vn/pmc-ecm-minigame-api-golang/api"
    COMMON_HEADERS = {
        'host': 'api-gateway.pharmacity.vn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'appversion': '3.3.6',
        'x-device-id': '26292a4881e43647',
        'x-device-platform': 'ANDROID',
        'x-device-platform-version': '9',
        'authorization': f'Bearer {BEARER_TOKEN}',
        'x-device-timezone': 'Asia/Ho_Chi_Minh',
        'user-agent': 'okhttp/4.9.2',
    }

    def get_checkin_info():
        url = f"{BASE_URL}/checkin_sequence"
        params = {'sequence': '7'}
        try:
            response = requests.get(url, headers=COMMON_HEADERS, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi lấy thông tin check-in: {e}")
            if e.response:
                print(f"Chi tiết lỗi: {e.response.text}")
            return None

    def perform_checkin():
        url = f"{BASE_URL}/checkin"
        headers = {**COMMON_HEADERS, 'content-type': 'application/json'}
        data = {}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi thực hiện check-in: {e}")
            if e.response:
                print(f"Chi tiết lỗi: {e.response.text}")
            return None

    # Begin
    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"--- Bắt đầu quy trình check-in cho ngày {today_str} ---")

    checkin_data = get_checkin_info()

    if not checkin_data:
        print("Không thể lấy dữ liệu check-in. Dừng chương trình.")
        return JSONResponse(content={'data': "Không thể lấy dữ liệu check-in. Dừng chương trình."}, status_code=200)

    # Tìm trạng thái check-in của ngày hôm nay
    today_status = None
    for day_info in checkin_data:
        if day_info.get('check_date') == today_str:
            today_status = day_info
            break

    # Nếu không tìm thấy ngày hôm nay trong chuỗi, giả định là chưa check-in
    if today_status is None:
            print(f"Không tìm thấy ngày {today_str} trong chuỗi, tiến hành check-in.")
            checkin_result = perform_checkin()
            if checkin_result:
                print("\n--- Kết quả check-in ---")
                print(json.dumps(checkin_result, indent=2, ensure_ascii=False))
                return JSONResponse(content={'data': checkin_result}, status_code=200)

    # Nếu đã tìm thấy và chưa check-in
    elif not today_status.get('checked'):
        print(f"Hôm nay ({today_str}) chưa check-in. Tiến hành check-in.")
        checkin_result = perform_checkin()
        if checkin_result:
            print("\n--- Kết quả check-in ---")
            print(json.dumps(checkin_result, indent=2, ensure_ascii=False))
            return JSONResponse(content={'data': checkin_result}, status_code=200)
            
    # Nếu đã check-in rồi
    else:
        print(f"Hôm nay ({today_str}) đã check-in rồi. Không cần làm gì thêm.")
        return JSONResponse(content={'data': f"Hôm nay ({today_str}) đã check-in rồi. Không cần làm gì thêm."}, status_code=200)
