from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class ChatState(TypedDict):
    messages= Annotated[list[BaseMessage],add_messages]

llm=ChatOpenAI()

def chat_node(state: ChatState):
    messages=state['messages']
    response=llm.invoke(messages)

    return {'messages': [response]}

checkpointer= MemorySaver()

graph=StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node', END)

chatbot=graph.compile(checkpointer=checkpointer)

initial_state={
    'messages': [HumanMessage(content='What is the capital of India')]
}

chatbot.invoke(initial_state)['messages'][-1].content

thread_id='1'
while True:
    user_message=input('enter query: ')
    print('user: ', user_message)

    config={'configurable':{'thread_id':thread_id}}

    response=chatbot.invoke({'messages':[HumanMessage(content=user_message)]}, config=config)

    print('AI', response['messages'][-1].content)

