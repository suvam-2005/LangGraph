from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI()

class LLMstate(TypedDict):
    question : str
    answer : str

def llm_qa(state:LLMstate)->LLMstate:
    question=state['question']
    prompt=f'Answer the following question {question}'
    answer=model.invoke(prompt).content
    state['answer']=answer
    return state

graph=StateGraph(LLMstate)

graph.add_node('llm_qa', llm_qa)

graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)

workflow = graph.compile()

initial_state={'question':'<your question>'}

final_state=final_state=workflow.invoke(initial_state)

print(final_state['answer'])