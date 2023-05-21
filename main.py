from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import random
from os import getenv

openai.organization = getenv("OPENAI_API_ORG")
openai.api_key = getenv("OPENAI_API_KEY")


class Message(BaseModel):
    text: str
    views: int | None = 0


starter = Message(text="Have a nice day!", views=0)

# will be replaced later
DATABASE = [starter]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# use open api to determine this
def check_is_good_message(msg: str):
    # other classification systems work but this is an experiment
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"respond with only YES if the following message is\
                    exclusively positive and nice and is relevant to being kind\
                    to another person: {msg}",
            },
        ],
    )

    is_yes = completion["choices"][0]["message"]["content"]
    print(is_yes)
    return is_yes == "YES" or is_yes == "YES."


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

    return "Sent"
