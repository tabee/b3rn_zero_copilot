from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from fastapi import FastAPI

app = FastAPI()

@app.get("/langchain")
def hello_langchain():
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Write out the following equation using algebraic symbols then solve it. Use the format\n\nEQUATION:...\nSOLUTION:...\n\n",
            ),
            ("human", "{equation_statement}"),
        ]
    )
    model = ChatOpenAI(temperature=0)
    runnable = (
        {"equation_statement": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    print(runnable.invoke("x raised to the third plus seven equals 12"))
    
    return {"message": "Hello from Langchain"}











