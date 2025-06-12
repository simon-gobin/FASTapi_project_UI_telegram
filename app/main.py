from fastapi import FastAPI
from app.bot import run_telegram_bot
import threading

app = FastAPI()

@app.on_event("startup")
def start_bot():
    threading.Thread(target=run_telegram_bot).start()

@app.get("/")
def root():
    return {"message": "FastAPI + Telegram Bot running"}