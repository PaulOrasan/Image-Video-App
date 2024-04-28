import gradio as gr
import numpy as np

from ui_utils import fetch_data

samples = [['images/first_frame.png', '2023-06-12 09:23'], ['images/first_frame_bear.png', '2023-06-12 09:40'], ['images/first_frame_cloud.png', '2023-06-12 10:03']]
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
    import os
    # samples.append([str(randint(0, 100)), str(randint(0, 100)), f'images/{os.listdir("images")[0]}', str(randint(0, 100))])
    samples.append([f'images/bird.png', 'a'])
    return samples
def create_demo():
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('# History page')
        with gr.Row():
            # dataset = gr.Dataset(components=[gr.Text(visible=False), gr.Text(visible=False), gr.Image(type="numpy", shape=(512,512), visible=False), gr.Text(visible=False)],
            #                      samples=samples, samples_per_page=3)
            gallery = gr.Gallery(samples, preview=True).style(columns=[6], rows=[2], object_fit="contain", height="auto")
        with gr.Row():
            button = gr.Button(value="Load prediction")
            button.click(add_sample, outputs=[gallery])


    return demo