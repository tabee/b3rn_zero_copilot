import ipywidgets as widgets
from IPython.display import clear_output, display



import os
from getpass import getpass

model_api_key = os.getenv("HF_API_KEY", None) or getpass("Enter HF API key:")

from haystack.nodes import PromptNode

prompt_node = PromptNode(
    model_name_or_path="HuggingFaceH4/zephyr-7b-beta", api_key=model_api_key, max_length=256, stop_words=["Human"]
)




from haystack.agents.memory import ConversationSummaryMemory

summary_memory = ConversationSummaryMemory(prompt_node)




from haystack.agents.conversational import ConversationalAgent

conversational_agent = ConversationalAgent(prompt_node=prompt_node, memory=summary_memory)


conversational_agent = ConversationalAgent(
   prompt_node=prompt_node,
   memory=summary_memory,
   tools=[search_tool]
)








conversational_agent.run("Tell me three most interesting things about Istanbul, Turkey")
conversational_agent.run("Can you elaborate on the second item?")
conversational_agent.run("Can you turn this info into a twitter thread?")

print(conversational_agent.memory.load())

conversational_agent.memory.clear()






## Text Input
user_input = widgets.Textarea(
    value="",
    placeholder="Type your prompt here",
    disabled=False,
    style={"description_width": "initial"},
    layout=widgets.Layout(width="100%", height="100%"),
)

## Submit Button
submit_button = widgets.Button(
    description="Submit", button_style="success", layout=widgets.Layout(width="100%", height="80%")
)


def on_button_clicked(b):
    user_prompt = user_input.value
    user_input.value = ""
    print("\nUser:\n", user_prompt)
    conversational_agent.run(user_prompt)


submit_button.on_click(on_button_clicked)

## Show Memory Button
memory_button = widgets.Button(
    description="Show Memory", button_style="info", layout=widgets.Layout(width="100%", height="100%")
)


def on_memory_button_clicked(b):
    memory = conversational_agent.memory.load()
    if len(memory):
        print("\nMemory:\n", memory)
    else:
        print("Memory is empty")


memory_button.on_click(on_memory_button_clicked)

## Clear Memory Button
clear_button = widgets.Button(
    description="Clear Memory", button_style="warning", layout=widgets.Layout(width="100%", height="100%")
)


def on_clear_button_button_clicked(b):
    conversational_agent.memory.clear()
    print("\nMemory is cleared\n")


clear_button.on_click(on_clear_button_button_clicked)

## Layout
grid = widgets.GridspecLayout(3, 3, height="200px", width="800px", grid_gap="10px")
grid[0, 2] = clear_button
grid[0:2, 0:2] = user_input
grid[2, 0:] = submit_button
grid[1, 2] = memory_button
display(grid)
