from typing import Annotated
from dotenv import load_dotenv

from components.login_component.LoginComponent import LoginComponent
from authorization.user import get_user_tokens

import uvicorn
from fastapi import FastAPI, Request, Cookie, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, Response

load_dotenv()

app = FastAPI()

login_component = LoginComponent()
login_component.mount(app, url="/login")


@app.middleware("login_checker")
async def add_process_time_header(request: Request, call_next):
    white_list = ['/login', '/callback']
    access_token = request.cookies.get('access_token')
    if access_token is None and not any(request.url.path.startswith(_) for _ in white_list):
        return RedirectResponse(url='/login')
    response = await call_next(request)
    return response


@app.get('/')
def index():
    return "Hello World!"


@app.get('/callback')
def callback(request: Request):
    try:
        token = get_user_tokens(request)
        response = HTMLResponse("""<script>alert("登入成功！此頁面將關閉");window.close();</script>""")
        response.set_cookie('access_token', token['access_token'], expires=token['expires_in'])
        return response
    except Exception as e:
        response = HTMLResponse("""<script>alert("登入失敗！請稍等或再次聯絡技術人員");window.close();</script>""")
        return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
