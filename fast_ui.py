from functools import partial
from typing import Coroutine, Any

from starlette.middleware.base import BaseHTTPMiddleware
from typing_extensions import Annotated

from fastapi import FastAPI, Request, Form, Response, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import gradio as gr
import requests

from app_admin import create_admin_page
from app_gr import create_main_page
from security_middleware import MyMiddleware
from ui_fast_utils import has_cookie, fetch_data, redirect_to_page_with_cookie, redirect_to_page, get_token_from_cookie, \
    fetch_admin_data, update_authorization, get_cookie_name
from comm_utils import OK, UNAUTHORIZED, REFUSED, BAD_REQUEST
from app_inference import create_demo as create_text_to_video_demo
from app_history_page import create_demo as create_history_demo
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")
my_middleware = MyMiddleware(some_attribute="some_attribute_here_if_needed")
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def compute_fn(req: gr.Request):
    print(req.headers)

# with gr.Blocks() as demo:
#     button = gr.Button()
#     button.click(compute_fn)
demo = create_main_page()
app = gr.mount_gradio_app(app, demo, path='/inference')

demo2 = create_admin_page()
app = gr.mount_gradio_app(app, demo2, path='/admin')
# demo2 = create_history_demo()
# demo2.queue()
# from app_gr import demo
# app = gr.mount_gradio_app(app, demo2, path='/history')
BACKEND_URL = 'http://localhost:5000'  # Replace with your backend service URL

# @app.get('/', response_class=HTMLResponse)
# async def main_page(request: Request):
#     if not has_cookie(request):
#         return redirect_to_page('/login')
#     data = fetch_data(request)
#     if data == UNAUTHORIZED:
#         return redirect_to_page_with_cookie('/login', value='', expires=0)
#     if data == REFUSED:
#         return templates.TemplateResponse("pending.html", {"request": request, "message": "You are in the queue, pending admin authorization. Thank you for your patience!"})
#     images = [f'http://localhost:7245/images/{img}' for img in data]
#     return templates.TemplateResponse("main.html", {"request": request, "images": images})


# @app.get('/gradio', response_class=HTMLResponse)
# async def get_inference(request: Request):
#     if not has_cookie(request):
#         return redirect_to_page('/login')
#
#     return templates.TemplateResponse("gradio.html", {"request": request})

@app.get('/login')
def load_login_page(request: Request):
    return templates.TemplateResponse("Login_v3/index.html", {"request": request})

@app.post('/login')
def login(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):
    response = requests.post(f'{BACKEND_URL}/login', json={'email': email, 'password': password})
    if response.status_code == OK:
        session_token = response.json().get('access_token')
        is_admin = bool(response.json().get('admin'))
        if is_admin:
            return redirect_to_page_with_cookie('/admin', cookie_name='admin_session_token', value=session_token)
        return redirect_to_page_with_cookie('/inference', value=session_token)
    if response.status_code == REFUSED:
        return templates.TemplateResponse("Login_v3/index.html", {"request": request, "message": "You are not yet authorized!"})
    return templates.TemplateResponse("Login_v3/index.html", {"request": request, "message": "Invalid credentials!"})

@app.get('/logout')
def logout(request: Request):
    return redirect_to_page_with_cookie('/login', cookie_name=get_cookie_name(request), value='', expires=0)


@app.get('/reports')
def find_average_of_requests():
    return JSONResponse(status_code=200, content={"Date": ['1','2','3','4','5'], 'Average number of inferences':[3,4,5,6,7]})

# @app.get('/images/{name}')
# async def get_image(name):
#     #TODO - input sanitization
#     response = requests.get(f'{BACKEND_URL}/images/{name}')
#     if response.status_code == OK:
#         return Response(response.content, media_type='image/png')
#     else:
#         return ""

# @app.get('/admin', response_class=HTMLResponse)
# async def get_admin_page(request: Request):
#     if not has_cookie(request):
#         return redirect_to_page('/login')
#     data = fetch_admin_data(request)
#     if data is None:
#         return "UNAUTHORIZED ADMIN ACCESS!"
#     return templates.TemplateResponse("admin.html", {"request": request, "users": data})

# @app.put('/admin/authorizations')
# async def get_update_authorization(request: Request, email: Annotated[str, Body()], authorization: Annotated[bool, Body()]):
#     if not has_cookie(request):
#         return redirect_to_page('/login')
#     status = update_authorization(request, email, authorization)
#     return Response(status_code=status)

@app.get('/signup')
def load_signup_page(request: Request):
    return templates.TemplateResponse("Login_v3/signup.html", {"request": request})

@app.post('/signup')
def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    response = requests.post(f'{BACKEND_URL}/signup', json={'email': email, 'password': password})
    if response.status_code == 200:
        return redirect_to_page('/login')
    else:
        return JSONResponse(content={'error': 'Invalid credentials'}, status_code=401)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=7246)
