import gradio as gr
import numpy as np

from PredictionDTO import PredictionDTO
from ui_fast_utils import fetch_data

samples = [['images/first_frame.png', '2023-06-12 09:23'], ['images/first_frame_bear.png', '2023-06-12 09:40'], ['images/first_frame_cloud.png', '2023-06-12 10:03']]
# samples = gr.State([])
history = []

def fetch_data_wrapper(photos, req:gr.Request):
    data = fetch_data(req)
    preds = [PredictionDTO.decode_prediction_from_json(d) for d in data]
    return preds, [[f'http://localhost:7245/images/{p.source_image}', p.request_time] for p in preds]

def change_selection(evt: gr.SelectData):
    return evt.index

def load_prediction(curr):
    print(curr)
    return curr, gr.Tabs.update(selected=0)


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

def create_demo(predictions_state, selected_prediction_state, tabs):
    with gr.TabItem('See your past predictions', id=1) as tab:
        with gr.Blocks() as demo:
            # photos = gr.State([])
            with gr.Row():
                gr.Markdown('# History page')
            with gr.Row():
                # dataset = gr.Dataset(components=[gr.Text(visible=False), gr.Text(visible=False), gr.Image(type="numpy", shape=(512,512), visible=False), gr.Text(visible=False)],
                #                      samples=samples, samples_per_page=3)
                current_selection = gr.State(-1)
                gallery = gr.Gallery([], preview=True).style(columns=[6], rows=[2], object_fit="contain", height="auto")
                gallery.select(change_selection, inputs=[], outputs=[current_selection])
            with gr.Row():
                button = gr.Button(value="Load prediction")
                button.click(load_prediction, inputs=[current_selection], outputs=[selected_prediction_state, tabs])
        demo.queue()
    tab.select(fetch_data_wrapper, inputs=[predictions_state], outputs=[predictions_state, gallery])
    return tab