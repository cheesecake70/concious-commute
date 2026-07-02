from agents.syllabus_agent import syllabus_agent
from google.adk.agents import Agent

def test_syllabus_agent_properties():
    assert syllabus_agent.name == "syllabus_agent"
    assert isinstance(syllabus_agent, Agent)
    assert syllabus_agent.output_key == "syllabus_topics"
    assert len(syllabus_agent.tools) == 1
