import os
from flask import Flask, request
import requests

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")

    file_id = None

    if "document" in message:
        file_id = message["document"]["file_id"]
    elif "video" in message:
        file_id = message["video"]["file_id"]
    elif "audio" in message:
        file_id = message["audio"]["file_id"]
    elif "photo" in message:
        file_id = message["photo"][-1]["file_id"]

    if not file_id:
        return "ok"

    # Get file path from Telegram
    r = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    )
    file_path = r.json()["result"]["file_path"]

    download_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Send link back instantly
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"⚡ High Speed Download Link:\n{download_link}"
        }
    )

    return "ok"