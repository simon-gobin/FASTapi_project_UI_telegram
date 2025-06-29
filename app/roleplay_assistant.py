import os
import json
import logging
import subprocess
from dotenv import load_dotenv
from transformers import pipeline
import torch

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---- JSON Manager ----
class JSON_manager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.story_state = {}

    def create_json(self):
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

        default_state = {
            "Language": None,
            "System Character": None,
            "User Character": None,
            "Situation": None,
            "chat": [],
            "Summary of the situation": None,
        }

        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.story_state = json.load(f)
                logger.info("🗂️ Loaded existing story state.")
        else:
            self.story_state = {}

        for key, value in default_state.items():
            self.story_state.setdefault(key, value)

        self.save_json()

    def reset_json(self):
        self.story_state = {
            "Language": None,
            "System Character": None,
            "User Character": None,
            "Situation": None,
            "chat": [],
            "Summary of the situation": None,
        }
        self.save_json()
        logger.info("📄 Story state reset.")

    def save_json(self):
        with open(self.json_path, "w") as f:
            json.dump(self.story_state, f, indent=2)
        logger.info("💾 Story state saved.")

    def update_state(self, key, value):
        self.story_state[key] = value
        self.save_json()

    def add_chat(self, role, content):
        self.story_state["chat"].append({"role": role, "content": content})
        self.save_json()

    def is_setup_complete(self):
        return all([
            self.story_state["Language"],
            self.story_state["System Character"],
            self.story_state["User Character"],
            self.story_state["Situation"]
        ])

# ---- Loader ----
class Loader:
    def __init__(self):
        self.token = None
        self.pipe = None

    def token_load(self):
        load_dotenv(dotenv_path="/Users/simon/PycharmProjects/FastAPIProject/.env")
        self.token = os.getenv("HF_TOKEN")
        if self.token:
            subprocess.run(
                ["huggingface-cli", "login", "--token", self.token, "--add-to-git-credential"],
                check=True
            )
        else:
            raise EnvironmentError("HF_TOKEN not found in environment.")

    def load_llama(self):
        model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )
        return self.pipe

# ---- Roleplay Assistant ----
class RoleplayAssistant:
    def __init__(self, json_path):
        self.json_path = json_path
        self.manager = JSON_manager(json_path)
        self.manager.create_json()
        self.manager.add_chat()
        self.story_state = self.manager.story_state
        self.loader = Loader()

    def manage_input(self):
        while True:
            self.loader.token_load()
            pipe = self.loader.load_llama()

            if not self.story_state["System Character"]:
                prompt = (
                    f"You are a roleplay assistant. Please ask the user who you are in their story "
                    f"(language: {self.story_state['Language']}). JSON state:\n{json.dumps(self.story_state)}"
                )
                output = pipe(prompt, max_new_tokens=256)
                generated =  output[0]["generated_text"]
                self.manager.add_chat("assistant", generated)
                return generated


            elif not self.story_state["User Character"]:
                prompt = (
                    f"You are playing the character '{self.story_state['System Character']}'. Ask the user who they are in the story "
                    f"(language: {self.story_state['Language']}). JSON state:\n{json.dumps(self.story_state)}"
                )
                output = pipe(prompt, max_new_tokens=256)
                generated =  output[0]["generated_text"]
                self.manager.add_chat("assistant", generated)
                return generated


            elif not self.story_state["Situation"]:
                prompt = (
                    f"You are a roleplay assistant and both characters are defined. Now ask the user what is the story or situation. "
                    f"(language: {self.story_state['Language']}). JSON state:\n{json.dumps(self.story_state)}"
                )
                output = pipe(prompt, max_new_tokens=256)
                generated =  output[0]["generated_text"]
                self.manager.add_chat("assistant", generated)
                return generated

            elif self.story_state['chat'][-1] startwith "1": #trigger create a telegram ui interface for model can now how to call last message
                prompt = (
                    f"You are this Character : {story_state["System Character"]} and speak with {story_state["User Character"]}, this is the Situation of you converstion so far {self.story_state['Situation']}"
                    f"and this is the last message you have with the user :  {self.story_state['chat']}, you need to answer in carathere with a disciption of the scen with didacaly in this languag"
                    f"(language: {self.story_state['Language']}). JSON state:\n{json.dumps(self.story_state)}"
                )
                output = pipe(prompt, max_new_tokens=256)
                generated =  output[0]["generated_text"]
                self.manager.add_chat("assistant", generated)
                return generated


            else:
                time.sleep(60)