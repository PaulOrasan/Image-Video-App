import gradio as gr
import tensorflow as tf
import os
model = tf.keras.models.load_model('old/checkpoint.h5')
import requests
def image_classifier(inp):
    img = inp.resize((224, 224))
    input = tf.convert_to_tensor(img)
    input = tf.expand_dims(input, 0)
    output = model(input)
    return {'non-fire': float(output[0][0]), 'fire': float(output[0][1])}


def my_auth(username, password):
    # if request:
    #     print("Request headers dictionary:", request.headers)
    #     print("IP address:", request.client.host)
    #     print("Username:", request.username)
    return True
    # response = requests.post(f'http://localhost:5000/login', json={'username': username, 'password': password})
    # return response.status_code == 200

if __name__=='__main__':
    example_files = [f'./images/{file}' for file in os.listdir('images/')]
    demo = gr.Interface(fn=image_classifier, inputs=gr.Image(type="pil"), outputs="label", examples=example_files)
    demo.launch(
        # auth=my_auth
    )