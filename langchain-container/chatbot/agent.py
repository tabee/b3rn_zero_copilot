from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def run_agent(topic="Here can be your prompt!"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a helpful agent. {topic}:\n\n",
            ),
            ("human", "{topic}"),
            ]
        )
    model = ChatOpenAI(temperature=0.5)
    runnable = (
        {"topic": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    result = runnable.invoke(topic)
    print(result)
    return result