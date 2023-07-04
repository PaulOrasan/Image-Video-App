from fastapi import FastAPI, Response
import gradio as gr

CUSTOM_PATH = "/gradio"

app = FastAPI()


@app.get("/")
def read_main(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "This is your main app"}

def compute_fn(req: gr.Request):
    print(req.headers)

with gr.Blocks() as demo:
    button = gr.Button()
    button.click(compute_fn)
demo.queue()
# from app_gr import demo
app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)