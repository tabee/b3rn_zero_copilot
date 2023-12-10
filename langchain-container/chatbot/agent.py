from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def agent_for(topic="Elefanten"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Erzähle etwas wissenswertes über {topic}:\n\n",
            ),
            ("human", "{topic}"),
            ]
        )
    model = ChatOpenAI(temperature=0.1)
    runnable = (
        {"topic": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    for chunk in runnable.stream(topic):
        print(chunk, end="", flush=True)
        yield chunk
