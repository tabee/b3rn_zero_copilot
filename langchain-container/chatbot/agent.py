from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def run_agent(prompt="Here can be your prompt!"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a helpful agent. {prompt}:\n\n",
            ),
            ("human", "{prompt}"),
            ]
        )
    model = ChatOpenAI(temperature=0.5)
    runnable = (
        {"prompt": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    result = runnable.invoke(prompt)
    print(result)
    return result