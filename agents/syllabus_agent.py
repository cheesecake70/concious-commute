from google.adk.agents import Agent
from google.adk.models import Gemini
from mcp_server.tools.syllabus_parser import parse_syllabus_pdf

syllabus_agent = Agent(
    name="syllabus_agent",
    model=Gemini(model="gemini-2.0-flash-lite"),
    instruction="""
    You are a Syllabus Parser Agent. Your goal is to extract the structured syllabus modules and topics for a given subject.
    
    1. Call the `parse_syllabus_pdf` tool using the subject name from the user's input.
    2. Extract all module names and key sub-topics/concepts listed under each module.
    3. Format the output clearly. Group topics by Module number and title.
    4. Provide only the extracted modules and topics list in the final response. Do not include conversational filler.
    """,
    tools=[parse_syllabus_pdf],
    output_key="syllabus_topics"
)
