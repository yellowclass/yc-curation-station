import uvicorn
from dotenv import dotenv_values
from starlette.applications import Starlette
from utils.http import ping
from chatBot.chat import get_bot_info, get_full_chat, retrieve_nearest_documents, send_message
from starlette.staticfiles import StaticFiles

config = dotenv_values(".env")

BASE_URL = "/api/curationStation"

app = Starlette()

app.add_route(BASE_URL + "/ping", ping, methods=["GET"])
app.add_route(BASE_URL + "/send-message", send_message, methods=["POST"])
app.add_route(BASE_URL + "/get-full-chat", get_full_chat, methods=["POST"])
app.add_route(BASE_URL + "/get-bot-info", get_bot_info, methods=["POST"])
# app.add_route(BASE_URL + "/retrieve-nearest-documents", retrieve_nearest_documents, methods=["POST"])
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config["PORT"] or 3000))
