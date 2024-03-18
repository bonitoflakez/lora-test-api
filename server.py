import os
import json
import time
import requests
from dotenv import load_dotenv

from flask import Flask, request, jsonify, send_file

load_dotenv()

# comfyUI prompt endpoint
PROMPT_URL = os.getenv('PROMPT_URL')
COMFY_OUTPUT_DIR = os.getenv('COMFY_OUTPUT_DIR')

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
def generate_image(user_prompt):
    with open("utils/workflow_api_1.json", "r") as workflow_config:
        workflow_prompt = json.load(workflow_config)

    # Generate a unique seed for each image generation
    unique_seed = int(time.time() * 1000) # Using current timestamp in milliseconds

    # Modify the workflow_prompt to include the unique_seed
    workflow_prompt['3']['inputs']['seed'] = unique_seed

    final_prompt = "miranowhere " + user_prompt

    # add custom user prompt
    workflow_prompt['6']['inputs']['text'] = final_prompt

    # check for any previously generated image
    prev_image = get_latest_image(COMFY_OUTPUT_DIR)

    start_queue(workflow_prompt)

    while True:
        latest_image = get_latest_image(COMFY_OUTPUT_DIR)
        if latest_image != prev_image:
            # print(latest_image)
            return latest_image

        time.sleep(1)

app = Flask(__name__)

@app.route('/getPrompt', methods=['POST'])
def get_prompt():
    try:
        # get data from request
        user_prompt = request.json.get('prompt')

        # check if data is present
        if user_prompt is None:
            return jsonify({'error': 'No data provided'}), 400

        img_output = generate_image(user_prompt)

        # check if image was generated successfully
        if img_output:
            return send_file(img_output), 200

        else:
            return jsonify({'error': 'Failed to generate image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
