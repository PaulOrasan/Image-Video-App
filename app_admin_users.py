import gradio as gr

from comm_utils import OK
from ui_fast_utils import fetch_admin_data, update_authorization


def get_users(req: gr.Request):
    data = fetch_admin_data(req)
    processed = [[el['email'], el['registration_time'], el['authorization']] for el in data]
    return processed, processed

def select_user(users, ex: gr.SelectData):
    print("selected")
    return users[ex.index[0]][0], users[ex.index[0]][1], users[ex.index[0]][2]

def update_user(users, email, authorization_status, req: gr.Request):
    resp = update_authorization(req, email, authorization_status)
    if resp == OK:
        for u in users:
            if u[0] == email:
                u[2] = authorization_status
    return users, users

def create_demo(users):
    with gr.TabItem(id=1, label='Users') as tab:
        with gr.Blocks() as demo:
            email_input = gr.Textbox(label="Email", interactive=False)
            registration_time_input = gr.Textbox(label="Registration Time", interactive=False)
            auth_status_input = gr.Checkbox(label="Authorization Status", interactive=True)
            with gr.Row():
                gr.Button("Clear")
                submit = gr.Button("Submit", variant="primary")
            # toggle_block = gr.outputs.Checkbox(label="Toggle Status")
            # auth_status_input.on_change(toggle_auth_status, "email", "registration_time", "auth_status")
            # examples = gr.Examples(inputs=[email_input, registration_time_input, auth_status_input], outputs=None, examples=[], label="Users")
            # examples = gr.Dataset(components=[email_input, registration_time_input, auth_status_input], samples=[['a','a','true'], ['b','b','false']], label="Users")
            # examples.click(select_user, inputs=[examples], outputs=[email_input, registration_time_input, auth_status_input])
            tabel = gr.DataFrame(headers=['Email', 'Registration time', 'Authorization status'], type='array',
                                 label='Users', interactive=False)
            tabel.select(select_user, inputs=[users], outputs=[email_input, registration_time_input, auth_status_input])
            submit.click(update_user, [users, email_input, auth_status_input], outputs=[users, tabel])
    tab.select(get_users, inputs=[], outputs=[users, tabel])
    return tab
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

