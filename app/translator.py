from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from dotenv import load_dotenv
import torch

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("🗣️ Translator is starting...")

load_dotenv()
class Translator():
    def __init__(self):
        self.translation_model = None
        self.translation_tokenizer = None

    def load_translate():
            # translate
            logger.info("🗣️ Loading translation pipeline...")
            self.translation_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
            self.translation_tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    def translation_to_eng(self, input_text):
            if self.story_state['Language'] == "en":
                return input_text
            tokenizer = self.translation_tokenizer
            tokenizer.src_lang = self.story_state['Language']
            tokenizer.tgt_lang = "en"
            encoded = tokenizer(input_text, return_tensors="pt")
            generated = self.translation_model.generate(**encoded)
            return tokenizer.decode(generated[0], skip_special_tokens=True)

    def translation_from_eng(self, input_text):
            if self.story_state['Language'] == "en":
                return input_text  # no need to translate
            tokenizer = self.translation_tokenizer
            tokenizer.src_lang = 'en'
            tokenizer.tgt_lang = self.story_state['Language']
            encoded = tokenizer(input_text, return_tensors="pt")
            generated = self.translation_model.generate(**encoded)
            return tokenizer.decode(generated[0], skip_special_tokens=True)