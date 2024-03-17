<div align=center> <em> <strong> LoRa API </strong> </em> </div>

---

### Setup

#### Requirements

```sh
python3 -m pip install requests Pillow gradio python-dotenv
```

Sample `.env`

```txt
PROMPT_URL="<comfyui-prompt-route>"
COMFY_OUTPUT_DIR="<output-directory-of-comfyui>"
```

#### Run

```sh
# clone this repo
git clone https://github.com/bonitoflakez/lora-test-api.git && cd lora-test-api

# run gradio
python app.py

# run gradio with watch
gradio app.py
```

---

### ToDo

- [x] **Ensure Unique Seed for Each Image Generation:** Implement a mechanism to generate a unique seed for each image generation process. This can be achieved by using the current timestamp, a counter, or any other method that ensures each seed is unique and different for each image. This ensures that each generated image is completely different from the others, even if the seed values are close.
- [ ] Parse prompt input through a string
