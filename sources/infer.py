import torch
from model import Model

model = Model(device = "cuda", dtype = torch.float16)

# prompt = "a cat sitting next to a mirror"
prompt = "a high quality realistic photo of a cute cat running in a beautiful meadow"
params = {"t0": 44, "t1": 47 , "motion_field_strength_x" : 12, "motion_field_strength_y" : 12, "video_length": 8}

out_path, fps = f"outputs/text2video_{prompt.replace(' ','_')}.mp4", 2
model.process_text2video(prompt, model_name="CompVis/stable-diffusion-v1-4",
                         fps = fps, path = out_path, **params)

# from hf_utils import get_model_list
# model_list = get_model_list()
# for idx, name in enumerate(model_list):
#   print(idx, name)
# idx = int(input("Select the model by the listed number: ")) # select the model of your choice
# model.process_text2video(prompt, model_name = model_list[idx], fps = fps, path = out_path, **params)