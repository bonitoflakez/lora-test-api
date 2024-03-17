import os
import json
import time
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# comfyUI prompt endpoint
PROMPT_URL = os.getenv('PROMPT_URL')
COMFY_OUTPUT_DIR = os.getenv('COMFY_OUTPUT_DIR')

"""
TODO
- do the seed cache thingy to check for newly generated images
"""

# get generated image and display on gradio
def get_latest_image(folder):
	files = os.listdir(folder)
	image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
	image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
	latest_image = os.path.join(folder, image_files[-1] if image_files else None)
	return latest_image

# start queue
def start_queue(prompt_workflow):
	p = {"prompt": prompt_workflow}
	queue_data = json.dumps(p).encode('utf-8')
	requests.post(PROMPT_URL, data=queue_data)

# generate image using workflow
def generate_image():
	with open("utils/workflow_api.json", "r") as workflow_config:
		workflow_prompt = json.load(workflow_config)

	# check for any previously generated image
	prev_image = get_latest_image(COMFY_OUTPUT_DIR)

	start_queue(workflow_prompt)

	while True:
		latest_image = get_latest_image(COMFY_OUTPUT_DIR)
		if latest_image != prev_image:
			return latest_image

		time.sleep(1)

# print(workflow_data)

demo = gr.Interface(fn=generate_image, inputs=[], outputs=["image"])

demo.launch()