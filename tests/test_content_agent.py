from agents.content_agent import content_agent
from google.adk.agents import Agent

def test_content_agent_properties():
    assert content_agent.name == "content_agent"
    assert isinstance(content_agent, Agent)
    assert content_agent.output_key == "study_plan"
    assert len(content_agent.tools) == 1
