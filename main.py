from fastapi import FastAPI
from pydantic import BaseModel
import random


class Message(BaseModel):
    text: str
    views: int | None = 0


starter = Message(text="Have a nice day!", views=0)

# will be replaced later
DATABASE = [starter]


app = FastAPI()

# use open api to determine this
def check_is_good_message(msg: str):
    return True


@app.get("/get_message")
def get_message():
    msg = random.choice(DATABASE)

    # no guaranties in python
    if msg.views is not None:
        msg.views += 1
    else:
        msg.views = 0
    return msg


@app.post("/send_message")
def send_message(msg: Message):
    msg.views = 0

    if check_is_good_message(msg.text):
        DATABASE.append(msg)

    return "Thanks!"
