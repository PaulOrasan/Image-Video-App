import time

import gradio as gr
import os
import requests
from flask import jsonify
from io import BytesIO

def computing_function(
            prompt,
            image,
            model_name,
            motion_field_strength_x,
            motion_field_strength_y,
            t0,
            t1,
            n_prompt,
            chunk_size,
            video_length,
            watermark,
            merging_ratio,
            seed,
            req: gr.Request,
            progress=gr.Progress()
):
    progress(0, desc='Starting pipeline...')
    headers = [i for i in req.headers.cookie.split() if i.startswith('session')]
    headers = headers[0].split('=')
    headers = headers[1].split(';')[0]
    head_obj = {}
    head_obj['Authorization'] = f'Bearer {headers}'
    byte_io = BytesIO()
    image.save(byte_io, 'png')
    byte_io.seek(0)
    files = {'files': ('1.png', byte_io, 'image/png') }
    resp = requests.post('http://localhost:5000/images', files=files, headers=head_obj)
    print(resp.status_code)
    data_dics = {
        'image_path': resp.text,
        'prompt':prompt,
                       'motion_field_strength_x':motion_field_strength_x,
                       'motion_field_strength_y':motion_field_strength_y,
                       't0':t0,
                       't1':t1,
                       'n_prompt':n_prompt,
                       'video_length':video_length,
                       'seed':seed
                       }
    resp2 = requests.post('http://localhost:5000/inference', json=data_dics, headers=head_obj)
    print(resp2.status_code)
    # time.sleep(5)
    # sock.sendall(str(request).encode())
    # response = sock.recv(1024)
    # if not response:
    #     return
    # progress(0.1, response.decode())
    # for i in range(10, 30):
    #     time.sleep(0.1)
    #     progress(i/100, response.decode())
    # response = sock.recv(1024)
    # if not response:
    #     return
    # for i in range(30, 80):
    #     time.sleep(0.1)
    #     progress(i/100, response.decode())
    # response = sock.recv(1024)
    # if not response:
    #     return
    # for i in range(80, 100):
    #     time.sleep(0.1)
    #     progress(i/100, response.decode())
    # response = sock.recv(1024)
    # if not response:
    #     return
    # progress(1, response.decode())
    # sock.close()
    return f"http://localhost:7245/images/{resp2.text}"
    # return "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('localhost', 8005))

on_huggingspace = os.environ.get("SPACE_AUTHOR_NAME") == "PAIR"

examples = [
    ["an astronaut waving the arm on the moon"],
    ["a sloth surfing on a wakeboard"],
    ["an astronaut walking on a street"],
    ["a cute cat walking on grass"],
    ["a horse is galloping on a street"],
    ["an astronaut is skiing down the hill"],
    ["a gorilla walking alone down the street"],
    ["a gorilla dancing on times square"],
    ["A panda dancing dancing like crazy on Times Square"],
]


def create_demo():

    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown('## Image2Video-Zero: Video Generation')
        with gr.Row():
            gr.HTML(
                """
                <div style="text-align: left; auto;">
                <h2 style="font-weight: 450; font-size: 1rem; margin: 0rem">
                    Description: Simply input <b>any textual prompt</b> to generate videos right away from your source image and unleash your creativity and imagination! For performance purposes, our current preview release allows to generate up to 16 frames, which can be configured in the Advanced Options.
                </h3>
                </div>
                """)

        with gr.Row():
            with gr.Column():
                image = gr.Image(label="Source image", type='pil', value="images/first_frame.png")
                prompt = gr.Textbox(label='Prompt')
                run_button = gr.Button(label='Run')
                with gr.Accordion('Advanced options', open=False):
                    if on_huggingspace:
                        video_length = gr.Slider(
                            label="Video length", minimum=8, maximum=16, step=1)
                    else:
                        video_length = gr.Number(
                            label="Video length", value=8, precision=0)

                    n_prompt = gr.Textbox(
                        label="Optional Negative Prompt", value='')
                    seed = gr.Slider(label='Seed',
                                     info="-1 for random seed on each run. Otherwise, the seed will be fixed.",
                                     minimum=-1,
                                     maximum=65536,
                                     value=0,
                                     step=1)
                    t0 = gr.Slider(label="Timestep t0", minimum=0,
                                   maximum=47, value=44, step=1,
                                   info="Perform DDPM steps from t0 to t1. The larger the gap between t0 and t1, the more variance between the frames. Ensure t0 < t1 ",
                                   )
                    t1 = gr.Slider(label="Timestep t1", minimum=1,
                                   info="Perform DDPM steps from t0 to t1. The larger the gap between t0 and t1, the more variance between the frames. Ensure t0 < t1",
                                   maximum=48, value=47, step=1)
                    motion_field_strength_x = gr.Slider(
                        label='Global Translation $\\delta_{x}$', minimum=-20, maximum=20,
                        value=12,
                        step=1)
                    motion_field_strength_y = gr.Slider(
                        label='Global Translation $\\delta_{y}$', minimum=-20, maximum=20,
                        value=12,
                        step=1)

                    chunk_size = gr.Slider(
                        label="Chunk size", minimum=2, maximum=16, value=8, step=1, visible=not on_huggingspace,
                        info="Number of frames processed at once. Reduce for lower memory usage."
                    )
            with gr.Column():
                result = gr.Video(value="images/horse.mp4", label="Generated Video",)

        inputs = [
            prompt,
            image,
            motion_field_strength_x,
            motion_field_strength_y,
            t0,
            t1,
            n_prompt,
            chunk_size,
            video_length,
            seed,
        ]

        run_button.click(fn=computing_function,
                         inputs=inputs,
                         outputs=result,)
    return demo
