from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from chuck_norris import chuck_norris_joke_about


app = FastAPI()

@app.get("/")
def read_root():
    res = chuck_norris_joke_about(topic="Ziegelsteine")
    print(res)
    return {"Jocke": res}


@app.get("/joke/{topic}")
def get_joke(topic: str):
    joke = chuck_norris_joke_about(topic=topic)
    return {"Joke": joke}