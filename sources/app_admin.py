import gradio as gr

from app_admin_users import create_demo as create_users_page
from app_admin_reports import create_demo as create_reports_page

theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="fuchsia",
)

with gr.Blocks(theme=theme) as demo:
    with gr.Tab('Maintenance Status'):
        create_reports_page()
    with gr.Tab('Users'):
        create_users_page()

demo.launch()