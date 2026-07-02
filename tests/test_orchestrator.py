from agents.orchestrator import orchestrator, app
from google.adk.agents import SequentialAgent
from google.adk.apps import App

def test_orchestrator_structure():
    assert orchestrator.name == "orchestrator"
    assert isinstance(orchestrator, SequentialAgent)
    assert len(orchestrator.sub_agents) == 2
    assert orchestrator.sub_agents[0].name == "syllabus_agent"
    assert orchestrator.sub_agents[1].name == "content_agent"
    assert isinstance(app, App)
    assert app.name == "conscious_commute_app"
