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

@app.get("/phat")
def phat():
    bien_so = '59T101811'
    url = "https://phatnguoixe.com/102699"
    data = {"BienSo": bien_so, "LoaiXe": 2}
    try:
        import requests
        with requests.Session() as se:
            dl = se.post(url, data=data)
            dl.raise_for_status()
            dl = dl.text; print(dl)
            if bien_so in dl:
                if dl.count('Không tìm thấy vi phạm phạt nguội!') == 1:
                    txt = 'Không tìm thấy vi phạm phạt nguội!'
                else:
                    txt = 'Có vi phạm phạt nguội!'
            else:
                txt = 'Lỗi không xác định!'
        return JSONResponse(content={'data': txt}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'data': str(e)}, status_code=200)
