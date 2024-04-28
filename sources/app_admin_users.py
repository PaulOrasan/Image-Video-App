import gradio as gr

def create_demo():
    with gr.Blocks() as demo:
        email_input = gr.inputs.Textbox(label="Email")
        registration_time_input = gr.inputs.Textbox(label="Registration Time")
        auth_status_input = gr.Checkbox(label="Authorization Status", interactive=True)
        with gr.Row():
            gr.Button("Clear")
            submit = gr.Button("Submit", variant="primary")
            submit.click(toggle_auth_status, [email_input, registration_time_input, auth_status_input], outputs=None)
        # toggle_block = gr.outputs.Checkbox(label="Toggle Status")
        # auth_status_input.on_change(toggle_auth_status, "email", "registration_time", "auth_status")
        gr.Examples(inputs=[email_input, registration_time_input, auth_status_input], outputs=None, examples=[
            ["paul.orasan@stud.ubbcluj.ro", "2023-06-10 10:30", True],
            ["john.smith@yahoo.com", "2023-06-15 19:48", False],
            ["jane.smith@gmail.com", "2023-06-14 12:19", True],
            ["joe.doe@outlook.com", "2023-06-14 7:09", False]], label="Users")
    return demo
# # import gradio as gr
# #
# import gradio as gr
#
def toggle_auth_status(email, registration_time, auth_status):
    # Perform any necessary actions based on the authorization status
    print(f"Email: {email} | Registration Time: {registration_time} | Authorization Status: {auth_status}")

# def create_demo():
#     iface = gr.Interface(
#         fn=toggle_auth_status,
#         inputs=[
#             gr.inputs.Textbox(label="Email"),
#             gr.inputs.Textbox(label="Registration Time"),
#             gr.inputs.Checkbox(label="Authorization Status")
#         ],
#         outputs=None,
#         examples=[["example@example.com", "2023-06-14 10:30:00", True]],
#         title="User Authorization Status",
#         description="Toggle the authorization status for each user."
#     )
#     return iface

