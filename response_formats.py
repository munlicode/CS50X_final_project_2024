from typing import List, Literal, Union
from pydantic import BaseModel


class Step(BaseModel):
    type: Literal["step"]
    explanation: str
    output: str

class StepByStep(BaseModel):
    type: Literal["step-by-step"]
    steps: List[Step]
    final_answer: str

class Explanation(BaseModel):
    type: Literal["explanation"]
    explanation: str


class QuickAnswer(BaseModel):
    type: Literal["quick-answer"]
    answer: str


class VisualExplanation(BaseModel):
    type: Literal["visual-explanation"]
    graph: str
    explanation: str

class CompositeFormat(BaseModel):
    response: Union[StepByStep, Explanation, QuickAnswer] # VisualExplanation
