from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def chuck_norris_joke_about(topic):
    prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "erfinde einen Chuck Norris Witz über {topic}:\n\n",
                ),
                ("human", "{topic}"),
            ]
        )
        model = ChatOpenAI(temperature=0.5)
        runnable = (
            {"topic": RunnablePassthrough()} | prompt | model | StrOutputParser()
        )

        result = runnable.invoke("Elefanten")
        print(result)
    return result