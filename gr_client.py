from gradio_client import Client
from PIL import Image
client = Client("http://127.0.0.1:7860")
print(client.view_api())
print(client.predict(Image.open('images/first_frame_bear.png')))