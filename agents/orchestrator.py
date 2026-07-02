from google.adk.agents import SequentialAgent
from google.adk.apps import App
from agents.syllabus_agent import syllabus_agent
from agents.content_agent import content_agent

orchestrator = SequentialAgent(
    name="orchestrator",
    sub_agents=[syllabus_agent, content_agent],
)

app = App(
    root_agent=orchestrator,
    name="conscious_commute_app",
)
