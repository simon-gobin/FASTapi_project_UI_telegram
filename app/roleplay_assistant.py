import logging

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("🚀 App is starting...")

load_dotenv()

class RoleplayAssistant:
    def __init__(self):
        self.json_path = json_path
        self.story_state = None
        self.model = None
        self.tokenizer = None
        self.pipe = None
        self.message_count = 0
        self.image_count = 0

    def creat_json(self): #use new JSON model




