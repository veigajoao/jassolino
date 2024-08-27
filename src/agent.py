from langgraph.graph import StateGraph, START, END
from .state import State

graph_builder = StateGraph(State)

################################
# Define a chatbot node (should go to nodes after)
################################
from langchain_anthropic import ChatAnthropic
from tools import tools


llm = ChatAnthropic(
    model_name="claude-3-sonnet-20240229",
    temperature=None,
    timeout=None,
    stop=None,
    base_url=None,
    api_key=None
    )
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


##################################
# Add nodes to the graph
##################################

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

# Add tool call node
from .nodes import BasicToolNode
from .tools import tools
tool_node = BasicToolNode(tools = tools)
graph_builder.add_node("tools", tool_node)


###################################
# Add edges to the graph
###################################

from typing import Literal
from .routers import route_tools


# Graph start point
graph_builder.add_edge(START, "chatbot")

# Graph can end or not depending on message
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", "__end__": "__end__"},
)
graph_builder.add_edge("tools", "chatbot")

### Compile with checkpointer
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Compile graph
graph = graph_builder.compile(memory)