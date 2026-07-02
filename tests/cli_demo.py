import sys
import asyncio
from utils.railway_graph import RailwayGraph
from backend.security.api_key_manager import verify_gemini_api_key
from agents.orchestrator import app
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import uuid

async def main():
    if len(sys.argv) < 4:
        print("Usage: uv run python tests/cli_demo.py <Source> <Destination> <Subject> [peak]")
        sys.exit(1)
        
    source = sys.argv[1]
    destination = sys.argv[2]
    subject = sys.argv[3]
    is_peak = len(sys.argv) > 4 and sys.argv[4].lower() == "peak"
    
    # 1. Verify API Key
    try:
        verify_gemini_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    # 2. Calculate Travel Time
    rg = RailwayGraph()
    duration, path = rg.calculate_travel_time(source, destination, is_peak=is_peak)
    
    if duration is None:
        print(f"Error: Route between '{source}' and '{destination}' not found.")
        sys.exit(1)
        
    print("=" * 60)
    print("CONSCIOUS COMMUTE - LOCAL ROUTE SUMMARY")
    print("=" * 60)
    print(f"Route: {source} -> {destination}")
    print(f"Path: {' -> '.join(path)}")
    print(f"Duration: {duration} minutes {'(Peak Hour adjustment applied)' if is_peak else ''}")
    print(f"Subject: {subject}")
    print("=" * 60)
    
    if duration < 5:
        print(f"Guardrail Alert: Travel time is {duration} minutes. Commute is too short for a study session (minimum 5 minutes required).")
        return
        
    # 3. Invoke ADK Agent Orchestrator
    print("Initializing ADK Agent Orchestrator...")
    runner = InMemoryRunner(app=app)
    session_service = runner.session_service
    
    session_id = str(uuid.uuid4())
    user_id = "cli_commuter"
    
    print("Pre-seeding session state with commute duration...")
    await session_service.create_session(
        app_name=app.name,
        user_id=user_id,
        session_id=session_id,
        state={"commute_duration": duration}
    )
    
    print("Invoking syllabus_agent & content_agent (sequential pipeline)...")
    user_message = Content(parts=[Part(text=subject)])
    
    # Execute
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        pass
        
    # Retrieve final state
    updated_session = await session_service.get_session(
        app_name=app.name,
        user_id=user_id,
        session_id=session_id
    )
    
    study_plan = updated_session.state.get("study_plan")
    
    print("\n" + "=" * 60)
    print("GENERATED STUDY PLAN FOR COMMUTE")
    print("=" * 60)
    if study_plan:
        print(study_plan)
    else:
        print("Error: Could not generate study plan.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
