import logging
import json
import dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, M2M100Config, M2M100ForConditionalGeneration, \
    M2M100Tokenizer

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("🚀 App is starting...")

load_dotenv()


class JSON_manager(self):
    def __init__(self, json_path):
        self.json_path = json_path

    def create_json(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.story_state = json.load(f)
                logger.info("🗂️ Loaded existing story state.")
        else:
            self.story_state = {
                "Language": None,
                "System Character": None,
                "User Character": None,
                "Situation": None,
                "chat": [],
                "Summary of the situation": None,
            }
            self.save_json()
            logger.info("📄 New story state initialized.")

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