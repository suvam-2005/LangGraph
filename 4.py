#parallel workflow

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

class BatsmanState(TypedDict):
    runs: int
    balls:int
    fours:int
    sixex:int

    sr:float
    bpb:float
    boundary_percentage:float
    summary:str

def calculate_sr(state: BatsmanState):
    sr=(state['runs']/state['balls'])*100
    return {'sr':sr}

def calculated_bpb(state: BatsmanState):
    bpb=state['balls']/(state['fours']+state['sixes'])
    return {'bpb':bpb}

def calculate_boundary_percent(state: BatsmanState):
    boundary_percent=(((state['fours']*4)+(state['sixes']*6))/state['runs'])*100
    return {'boundary_percent':boundary_percent}

def summary(state: BatsmanState):
    summary=f"""
strike Rate-{state['sr']} \n
Balls per boundary-{state['bpb']}\n
Boundary percent-{state['boundary_percent']}   
"""
    return {'summary':summary}

graph=StateGraph(BatsmanState)

graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculated_bpb)
graph.add_node('calculate_boundary_percent', calculate_boundary_percent)
graph.add_node('summary', summary)

#edges

graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percent')

graph.add_edge('calculate_sr','summary')
graph.add_edge('calculate_bpb','summary')
graph.add_edge('calculate_boundary_percent','summary')

graph.add_edge('summary', END)

workflow=graph.compile()

initial_state={
    'runs':100,
    'balls':50,
    'fours':6,
    'sixes':4
}

workflow.invoke(initial_state)
