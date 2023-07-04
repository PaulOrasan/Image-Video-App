import gradio as gr

from app_inference import create_demo as create_demo_text_to_video
from app_history_page import create_demo as create_demo_history_page, get_history
import argparse
import os


on_huggingspace = os.environ.get("SPACE_AUTHOR_NAME") == "PAIR"
parser = argparse.ArgumentParser()
parser.add_argument('--public_access', action='store_true',
                    help="if enabled, the app can be access from a public url", default=False)
args = parser.parse_args()
theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="fuchsia",
)

def create_main_page():
    with gr.Blocks(theme=theme) as demo:
        predictions = gr.State([])
        selected_prediction = gr.State(-1)
        with gr.Row():
            with gr.Column():
                gr.Markdown('# Image2Video-Zero: Video Generation')
            with gr.Column():
                logout = gr.Button("Log out")
                logout.click(None, None, None, _js="window.location.assign('http://127.0.0.1:7246/logout')")
        with gr.Tabs() as tabs:
            create_demo_text_to_video(predictions, selected_prediction)
            create_demo_history_page(predictions, selected_prediction, tabs)
        demo.queue()
        return demo
