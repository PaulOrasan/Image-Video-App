import os
import uuid

import PIL
import numpy as np
from PIL import Image
import imageio
import gradio as gr
def zoom_in_image(image, scale):
    width, height = image.size
    # new_image = image.copy()
    new_x = int(width * scale)
    new_y = int(height * scale)
    image_c = image.crop((new_x, new_y, width - 2 * new_x, height - 2 * new_y))
    # image_c = image.crop((20, 100, 20, 100))
    resized_image = image_c.resize((width, height), Image.ANTIALIAS)
    return resized_image

def generate_zooming_video(image, output_path, num_frames):
    width, height = image.size
    scale_step = 0.3 / num_frames  # Adjust the zooming rate here
    scale = 0
    with imageio.get_writer(output_path, mode='I', fps=2) as writer:
        for i in range(num_frames):
            scale += scale_step
            zoomed_image = zoom_in_image(image, scale)
            writer.append_data(np.array(zoomed_image))

def api(image_path, num_frames):
    unique_id = uuid.uuid4()
    output_video_path = f'files/{unique_id}.mp4'
    generate_zooming_video(image_path, output_video_path, int(num_frames))
    return f'{unique_id}.mp4'

# Usage example
# input_image_path = 'images/first_frame.png'  # Replace with your input image path
# output_video_path = 'videos/output_video2.mp4'  # Replace with your desired output video path
# num_frames = 16

# generate_zooming_video(input_image_path, output_video_path, num_frames)
demo = gr.Interface(api, inputs=[gr.Image(type="pil"), gr.Number()], outputs=gr.Text())
demo.queue()
demo.launch(server_port=7423)