import os
from dotenv import load_dotenv

load_dotenv()

from .db.database import engine, get_session, close_session
from .db import models, py_models, db_worker
from .exceptions import OpenAIException
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from openai import OpenAI, OpenAIError
from starlette.websockets import WebSocketDisconnect


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=engine)
    get_session()


@app.on_event("shutdown")
async def shutdown():
    close_session()


@app.get("/")
async def main():
    """
    Starting endpoint
    :return: index html page
    """
    return FileResponse("public/index.html")


@app.get("/ws")
async def main_ws():
    """
    Starting endpoint with websocket
    :return: websocket index page
    """
    return FileResponse("public/index_ws.html")


@app.get("/api/v1/get/history", response_model=list[py_models.HistoryItem])
def get_history(skip: int = 0, limit: int = 50) -> list:
    """
    Endpoint for getting history records from DB.
    :param skip: start record
    :param limit: maximum number of records
    :return: list of history records
    """
    try:
        resp = db_worker.get_history(get_session(), skip, limit)
        return resp
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@app.post("/api/v1/ask", response_model=py_models.HistoryItem)
def ask_gpt(item: py_models.HistoryCreate) -> models.History:
    """
    Endpoint for interaction with chat gpt.
    :param item: item with user and message information
    :return: dict with chatgpt answer
    """
    try:
        db_worker.add_history(get_session(), item)

        answer = call_gpt(item.message)

        ai_resp = db_worker.add_history(get_session(), py_models.HistoryCreate(user='AI', message=answer))
        return ai_resp
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@app.websocket("/api/v1/ask/stream")
async def ask_gpt_websocket(websocket: WebSocket):
    """
    Websocket endpoint. Allows to interact with chatGPT via websocket.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                db_worker.add_history(get_session(), py_models.HistoryCreate(user="ws_user", message=data))
                answer = call_gpt(data)
                ai_resp = db_worker.add_history(get_session(), py_models.HistoryCreate(user='AI', message=answer))
                ai_resp = py_models.HistoryItem.model_validate(ai_resp).model_dump_json()
                await websocket.send_json(ai_resp)
            except Exception as ex:
                await websocket.send_json({"user": "Error", "message": repr(ex)})
    except WebSocketDisconnect:
        print("Websocket was closed")


def call_gpt(message: str) -> str:
    """
    This method creates a query for chat gpt and return its response.
    :param message: user message for chat gpt
    :return: str with chat gpt answer
    """
    try:
        completion = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL"),
            messages=[
                {"role": "system", "content": "You’re a kind helpful assistant"},
                {"role": "user", "content": message},
                {
                    "role": "system",
                    "content": "You are TranslateGPT. You translate user messages from Russian to English. "
                               "And you return answers in Russian."
                },
            ]
        )
        resp = completion.choices[0].message.content
        print(resp)
        # There can be an error
        if "Error: Error code: 403" in resp:
            raise OpenAIException(resp)
        return resp
    except OpenAIError as ex:
        print(f"Open AI Error: {ex}")
        raise
