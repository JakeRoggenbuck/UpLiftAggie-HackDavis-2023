from fastapi import FastAPI
from pydantic import BaseModel

# will be replaced later
DATABASE = []


class Message(BaseModel):
    text: str
    views: int | None = None


app = FastAPI()

# use open api to determine this
def check_is_good_message(msg: str):
    return False


@app.get("/get_message")
def get_message():
    return {"Hack": "Davis"}


@app.post("/send_message")
def send_message(msg: Message):
    msg.views = 0

    if check_is_good_message(msg.text):
        DATABASE.append(msg)

    return "Thanks!"
