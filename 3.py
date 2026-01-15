#prompt chaining

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI()

class BlogState(TypedDict):
    title:str
    outline:str
    content:str

graph=StateGraph(BlogState)

def create_outline(state:BlogState)-> BlogState:
    title =state['title']
    prompt=f'<YOUR PROMPT>'
    outline=model.invoke(prompt).content

    state['outline']=outline

    return state

def create_blog(state:BlogState)->BlogState:
    title =state['title']
    outline=state['outline']

    prompt=f'<YOUR PROMPT>'

    content=model.invoke(prompt).content

    state['content']=content

    return state

graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_outline)

graph.add_edge(START, 'content_outline')
graph.add_edge('create_content', 'create_blog')
graph.add_edge('create_blog', END)

workflow=graph.compile()

