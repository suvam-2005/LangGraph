#Itrerative Workflow

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

generator_llm = ChatOpenAI(model='gpt-4o')
evaluator_llm = ChatOpenAI(model='gpt-4o-mini')
optimizer_llm = ChatOpenAI(model='gpt-40')

#Schema

class TweetEvaluation(BaseModel):
    evaluation:Literal["approved", "need_improvement"] = Field(..., description="Final evaluation")
    feedback:str=Field(..., description="")

structured_evaluator_llm=evaluator_llm.with_structured_output(TweetEvaluation)
# STATE

class TweetState(TypedDict):
    topic:str
    tweet:str
    evaluator:Literal["approved", "need_improvement"]
    feedback:str
    iteration:int
    max_iteration: int

def generate_tweet(state: TweetState):
    #prompt
    message=[
        SystemMessage(content=""),
        HumanMessage(content="")
    ]

    #send message
    response=generator_llm.invoke(message).content

    return{'tweet':response}

def evaluate(state:TweetState):
    #prompt
    message=[
        SystemMessage(content=""),
        HumanMessage(content="")
    ]
    response=structured_evaluator_llm.invoke(message)

    return {'evaluation':response.evaluation, 'feedback': response.feedback}

def optimize(state:TweetState):
    message=[
        SystemMessage(content=""),
        HumanMessage(content="")
    ]
    response =optimizer_llm.invoke(message).content
    iteration=state['iteration']+1

    return{'tweet':response, 'iteration':iteration}

def route_evaluation(state:TweetState):
    if state['evalustion']=='approved' or state['iteraton']>=state['max_iteration']:
        return 'approved'
    else:
        return 'need_improvement'

graph=StateGraph(TweetState)

graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate)
graph.add_node('optimize', optimize)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')

graph.add_conditional_edges('evaluate', route_evaluation, {'approved': END, 'needs_improvent':'optimize'})
graph.add_edge('optimize','evaluate')

workflow=graph.compile()

