from typing import Annotated
from dotenv import load_dotenv

from components.login_component.LoginComponent import LoginComponent
from components.index_component.IndexComponent import IndexComponent
from components.coloring_gallery_component.coloring_gallery_component import ColoringGalleryComponent
from components.generative_ai_component.generative_ai_component import GenerativeAiComponent
from authorization.user import get_user_tokens, get_user_printer, check_user_scanner

import uvicorn
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse, Response

load_dotenv()

app = FastAPI()

login_component = LoginComponent()
index_component = IndexComponent()
generative_ai_component = GenerativeAiComponent()
coloring_gallery_component = ColoringGalleryComponent()

login_component.mount(app, url="/login")
index_component.mount(app, url="/index")
coloring_gallery_component.mount(app, url="/coloring_gallery")
generative_ai_component.mount(app, url="/generative_ai")


# @app.middleware("login_checker")
# async def add_process_time_header(request: Request, call_next):
#     white_list = ['/login', '/callback', '/robots.txt']
#     access_token = request.cookies.get('access_token')
#     if access_token is None and not any(request.url.path.startswith(_) for _ in white_list):
#         return RedirectResponse(url='/login/')
#     response = await call_next(request)
#     return response


@app.get('/')
def root():
    return RedirectResponse(url='/index/')


@app.get('/callback')
def callback(request: Request):
    try:
        token = get_user_tokens(request)
        productName, serialNumber, connected = get_user_printer(token['access_token'])
        check_user_scanner(token['access_token'])
        response = HTMLResponse("""<script>alert("登入成功！此頁面將關閉");window.close();</script>""")
        response.set_cookie('access_token', token['access_token'], expires=token['expires_in'])
        response.set_cookie('product_name', productName, expires=token['expires_in'])
        response.set_cookie('serial_number', serialNumber, expires=token['expires_in'])
        response.set_cookie('connected', connected, expires=token['expires_in'])
        return response
    except Exception as e:
        response = HTMLResponse("""<script>alert("登入失敗！請稍等或再次聯絡技術人員");window.close();</script>""")
        return response


@app.post('/scanning_destinations')
async def receive_scanning(request: Request):
    form_data = await request.form()

    for file_key, file in form_data.items():
        if not file.filename.endswith('.jpg'):
            return Response(status_code=200)

        with open(f'static/upload/{file.filename}', "wb") as buffer:
            buffer.write(file.file.read())

    return Response(status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
