import requests

from fastapi import FastAPI, Request, Form, Response, Body
from fastapi.middleware.cors import CORSMiddleware

from comm_utils import OK
from fast_ui import BACKEND_URL
app2 = FastAPI()
app2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app2.get('/images/{name}')
async def get_image(name):
    #TODO - input sanitization
    response = requests.get(f'{BACKEND_URL}/files/{name}')
    if response.status_code == OK:
        return Response(response.content, media_type='image/png')
    else:
        return ""

@app2.get('/videos/{name}')
async def get_video(name):
    #TODO - input sanitization
    response = requests.get(f'{BACKEND_URL}/files/{name}')
    if response.status_code == OK:
        return Response(response.content, media_type='video/mp4')
    else:
        return ""

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app2, port=7245)
