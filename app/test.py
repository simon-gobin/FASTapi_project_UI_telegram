import torch
import transformers
import os
from dotenv import load_dotenv
import subprocess

# Load the .env token
load_dotenv(dotenv_path="/Users/simon/PycharmProjects/FastAPIProject/.env")
token = os.getenv("HF_TOKEN")
if token:
    subprocess.run(
        ["huggingface-cli", "login", "--token", token, "--add-to-git-credential"],
        check=True
    )
else:
    raise EnvironmentError("HF_TOKEN not found in environment.")


import transformers
import torch

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

outputs = pipeline(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])
