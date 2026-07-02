from google.adk.agents import Agent
from google.adk.models import Gemini
from pydantic import BaseModel, Field
from typing import List

class ModuleList(BaseModel):
    modules: List[str] = Field(description="List of modules or chapters extracted from the syllabus, e.g., 'Module 1: ...'")

module_extractor_agent = Agent(
    name="module_extractor_agent",
    model=Gemini(model="gemini-2.0-flash-lite"),
    instruction="""
    You are a Module Extractor Agent. Your task is to analyze the syllabus text and extract a list of module or chapter titles.
    Ensure each module name is clear, concise, and structured, e.g., 'Module X: [Title]'.
    Do not include sub-topics, only the high-level module names.
    Output the list of modules structured as requested.
    """,
    output_schema=ModuleList,
    output_key="modules"
)
