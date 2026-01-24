from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

class EvaluationSchema(BaseModel):
    feedback:str=Field(description='Detailed feedback the eassy')
    score:int=Field(description='score out of 10', ge=0, le=10)

structured_model=model.with_structured_output(EvaluationSchema)

class UPSCState(TypedDict):
    eassy:str
    language_feedback:str
    analysis_feedback:str
    overall_feedback:str
    indivitual_score:Annotated[list[int], operator.add]
    avg_score:float

graph =StateGraph(UPSCState)

def evaluate_language():
    prompt=f''
    output=structured_model.invoke(prompt)

    return {'language'}

graph.add_node('evaluate_language', evaluate_language)
graph.add_node('evaluate_analysis', evaluate_analysis)
graph.add_node('evaluate_thought', evaluate_thought)
graph.add_node('final_evaluation', final_evaluation)