import gradio as gr

from app_admin_users import create_demo as create_users_page
from app_admin_reports import create_demo as create_reports_page

theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="fuchsia",
)

def create_admin_page():
    with gr.Blocks(theme=theme) as demo:
        users = gr.State([])
        with gr.Row():
            with gr.Column():
                gr.Markdown('# Image2Video-Zero: Video Generation')
            with gr.Column():
                logout = gr.Button("Log out")
                logout.click(None, None, None, _js="window.location.assign('http://127.0.0.1:7246/logout')")
        with gr.Tabs() as tabs:
            create_reports_page()
            create_users_page(users)
    return demo
