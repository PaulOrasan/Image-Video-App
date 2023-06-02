import gradio as gr
import numpy as np

from ui_utils import fetch_data

samples = []
history = []

def get_history(request: gr.Request):
    if request:
        print("Request headers dictionary:", request.headers)
        print("IP address:", request.client.host)
        print("Username:", request.username)
    global history
    history = fetch_data()

def add_sample():
    from random import randint
    global samples
    samples.append([str(randint(0, 100)), str(randint(0, 100)), f'http://localhost:5000/images/{history[0]}', str(randint(0, 100))])
    return samples
def create_demo():
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('# History page')
        with gr.Row():
            dataset = gr.Dataset(components=[gr.Text(visible=False), gr.Text(visible=False), gr.Image(type="numpy", visible=False), gr.Text(visible=False)],
                                 samples=samples, samples_per_page=3)
        with gr.Row():
            button = gr.Button(value="Add sample")
            button.click(add_sample, outputs=[dataset])


    return demo