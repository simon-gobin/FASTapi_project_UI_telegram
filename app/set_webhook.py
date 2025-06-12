import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://9eeb-17-65-9-167.ngrok-free.app"

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
response = requests.get(url)

if response.status_code == 200:
    print("Webhook set successfully")
else:
    print("Failed to set webhook")