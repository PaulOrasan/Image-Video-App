import gradio as gr

from app_inference import create_demo as create_demo_text_to_video
from app_history_page import create_demo as create_demo_history_page, get_history
import argparse
import os

from gradio_app import my_auth

on_huggingspace = os.environ.get("SPACE_AUTHOR_NAME") == "PAIR"
parser = argparse.ArgumentParser()
parser.add_argument('--public_access', action='store_true',
                    help="if enabled, the app can be access from a public url", default=False)
args = parser.parse_args()
theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="fuchsia",
)


with gr.Blocks(theme=theme) as demo:

    with gr.Tab('Run inference'):
        create_demo_text_to_video()
    with gr.Tab('See your past predictions') as history_tab:
        create_demo_history_page()
    # with gr.Tab('Pose Conditional'):
    #     create_demo_pose(model)
    # with gr.Tab('Edge Conditional'):
    #     create_demo_canny(model)
    # with gr.Tab('Edge Conditional and Dreambooth Specialized'):
    #     create_demo_canny_db(model)
    # with gr.Tab('Depth Conditional'):
    #     create_demo_depth(model)
    '''
    '''
    # gr.HTML(
    #     """
    #     <div style="text-align: justify; max-width: 1200px; margin: 20px auto;">
    #     <h3 style="font-weight: 450; font-size: 0.8rem; margin: 0rem">
    #     <b>Version: v1.0</b>
    #     </h3>
    #     <h3 style="font-weight: 450; font-size: 0.8rem; margin: 0rem">
    #     <b>Caution</b>:
    #     We would like the raise the awareness of users of this demo of its potential issues and concerns.
    #     Like previous large foundation models, Text2Video-Zero could be problematic in some cases, partially we use pretrained Stable Diffusion, therefore Text2Video-Zero can Inherit Its Imperfections.
    #     So far, we keep all features available for research testing both to show the great potential of the Text2Video-Zero framework and to collect important feedback to improve the model in the future.
    #     We welcome researchers and users to report issues with the HuggingFace community discussion feature or email the authors.
    #     </h3>
    #     <h3 style="font-weight: 450; font-size: 0.8rem; margin: 0rem">
    #     <b>Biases and content acknowledgement</b>:
    #     Beware that the synthesis may output content that reinforces or exacerbates societal biases, as well as realistic faces, pornography, and violence.
    #     Text2Video-Zero in this demo is meant only for research purposes.
    #     </h3>
    #     </div>
    #     """)

demo.queue()
if on_huggingspace:
    demo.queue(max_size=20)
    demo.launch(debug=True)
else:
    _, _, link = demo.queue(api_open=False).launch(
        # auth=my_auth,
        file_directories=['temporal'], share=args.public_access)
    print(link)
