''' This is the main file for the chatbot agent. It is called by the main.py file in the same directory. '''
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

async def run_agent(user_input="Tell me something about the next open ai model!"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpfull assistant 
                for this prompt: {user_input}:\n\n 
                Your answer is as short as possible.
                And long answer is not needed.""",
            ),
            ("human", "{user_input}"),
            ]
        )
    model = ChatOpenAI(temperature=0.05)
    runnable = (
        {"user_input": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    #result = await runnable.ainvoke(user_input)
    for chunk in runnable.stream(user_input):
        print(chunk, end="", flush=True)
    return chunk


async def get_agent_runnable():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpfull assistant 
                for this prompt: {user_input}:\n\n 
                Your answer is as short as possible.
                And long answer is not needed.""",
            ),
            ("human", "{user_input}"),
            ]
        )
    model = ChatOpenAI(temperature=0.05)
    runnable = (
        {"user_input": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )
    return runnable

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent(user_input="wie viele Einwohner hat Thailand?"))

