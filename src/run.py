from langchain_core.messages import BaseMessage

from .agent import graph

from langchain_core.runnables import RunnableConfig

config: RunnableConfig = {"configurable": {"thread_id": "1"}, "callbacks": []}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                print("Assistant:", value["messages"][-1].content)