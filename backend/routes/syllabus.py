from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
import os
import uuid
import logging
from mcp_server.tools.syllabus_parser import parse_syllabus_pdf
from agents.module_extractor import module_extractor_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from google.genai.errors import APIError
from backend.security.api_key_manager import verify_gemini_api_key
from backend.security.rate_limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple mock database of modules as a fallback in case of rate limits or offline mode
MOCK_MODULES = {
    "engineering mathematics iii": [
        "Module 1: Laplace Transform",
        "Module 2: Inverse Laplace Transform",
        "Module 3: Fourier Series",
        "Module 4: Complex Variables",
        "Module 5: Linear Algebra & Matrices",
        "Module 6: Vector Integration"
    ],
    "data structures": [
        "Module 1: Introduction to Data Structures & Analysis",
        "Module 2: Linear Data Structures - Stacks and Queues",
        "Module 3: Linked Lists",
        "Module 4: Non-Linear Data Structures - Trees",
        "Module 5: Non-Linear Data Structures - Graphs",
        "Module 6: Sorting and Searching Techniques"
    ],
    "signals and systems": [
        "Module 1: Introduction to Signals and Systems",
        "Module 2: Linear Time-Invariant (LTI) Systems",
        "Module 3: Fourier Analysis of Continuous-Time Signals",
        "Module 4: Laplace Transform Analysis",
        "Module 5: Fourier Analysis of Discrete-Time Signals",
        "Module 6: Z-Transform Analysis"
    ],
    "engineering mechanics": [
        "Module 1: System of Coplanar Forces",
        "Module 2: Equilibrium of Coplanar Force Systems",
        "Module 3: Friction and Truss Analysis",
        "Module 4: Kinematics of Particles",
        "Module 5: Kinematics of Rigid Bodies",
        "Module 6: Kinetics of Particles (Newton's Laws, Work-Energy)"
    ],
    "corporate finance": [
        "Module 1: Introduction to Corporate Finance",
        "Module 2: Time Value of Money",
        "Module 3: Capital Budgeting Decisions",
        "Module 4: Cost of Capital & WACC",
        "Module 5: Working Capital Management",
        "Module 6: Dividend Policy and Decisions"
    ],
    "financial accounting": [
        "Module 1: Accounting Principles and Bookkeeping",
        "Module 2: Preparation of Financial Statements",
        "Module 3: Depreciation and Inventory Valuation",
        "Module 4: Partnership Accounts",
        "Module 5: Company Accounts (Shares & Debentures)",
        "Module 6: Financial Statement Ratio Analysis"
    ],
    "marketing management": [
        "Module 1: Introduction to Marketing & 4Ps",
        "Module 2: Consumer Buying Behavior",
        "Module 3: Market Segmentation, Targeting & Positioning (STP)",
        "Module 4: Product Life Cycle and Pricing Strategies",
        "Module 5: Distribution Channels and Promotion",
        "Module 6: Digital & Social Media Marketing"
    ],
    "human resource management": [
        "Module 1: HRM Foundations and Strategic HRM",
        "Module 2: HR Planning and Job Analysis",
        "Module 3: Recruitment, Selection & Induction",
        "Module 4: Training & Management Development",
        "Module 5: Performance Appraisal & Compensation Planning",
        "Module 6: Industrial Relations & Employee Welfare"
    ],
    "macroeconomics": [
        "Module 1: National Income Accounting (GDP & GNP)",
        "Module 2: Keynesian Demand Side Economics & Multiplier",
        "Module 3: Money Supply, Banking & Monetary Policy",
        "Module 4: Public Finance and Fiscal Policy",
        "Module 5: Business Cycles and Economic Growth",
        "Module 6: International Trade and Balance of Payments"
    ],
    "business law": [
        "Module 1: Indian Contract Act 1872",
        "Module 2: Indemnity, Guarantee, Pledge & Agency",
        "Module 3: Sale of Goods Act 1930",
        "Module 4: Negotiable Instruments Act 1881",
        "Module 5: Companies Act 2013 (MoA, AoA)",
        "Module 6: Consumer Protection Act 2019"
    ]}
SUBJECT_ALIASES = {
    "engineering mathematics iii": "engineering mathematics iii",
    "engineering maths 3": "engineering mathematics iii",
    "maths": "engineering mathematics iii",
    "data structures": "data structures",
    "signals and systems": "signals and systems",
    "signals & systems": "signals and systems",
    "engineering mechanics": "engineering mechanics",
    "mechanics": "engineering mechanics",
    "corporate finance": "corporate finance",
    "finance": "corporate finance",
    "financial accounting": "financial accounting",
    "accounting": "financial accounting",
    "marketing management": "marketing management",
    "marketing": "marketing management",
    "human resource management": "human resource management",
    "human resource": "human resource management",
    "hrm": "human resource management",
    "macroeconomics": "macroeconomics",
    "economics": "macroeconomics",
    "business law": "business law",
    "law": "business law"
}

@router.get("/syllabi", response_model=List[str])
def get_available_syllabi():
    return [
        "Engineering Mathematics III",
        "Data Structures",
        "Signals and Systems",
        "Engineering Mechanics",
        "Corporate Finance",
        "Financial Accounting",
        "Marketing Management",
        "Human Resource Management",
        "Macroeconomics",
        "Business Law"
    ]

@router.get("/modules", response_model=List[str], dependencies=[Depends(limiter.check_rate_limit)])
async def get_modules(subject: str = Query(...), api_key: str = Depends(verify_gemini_api_key)):
    """
    Invokes the Module Extractor Agent to read the syllabus PDF text
    and extract a list of module/chapter names.
    Falls back to mock modules on API limits.
    """
    subject_key = subject.lower().strip()
    
    # Match subject key using exact match or word subsets to prevent false-positives
    matched_subject = SUBJECT_ALIASES.get(subject_key)
    
    if not matched_subject:
        subject_words = set(subject_key.split())
        for alias, canonical in SUBJECT_ALIASES.items():
            alias_words = set(alias.split())
            if subject_words.issubset(alias_words) or alias_words.issubset(subject_words):
                matched_subject = canonical
                break
            
    if not matched_subject:
        raise HTTPException(status_code=400, detail=f"Subject '{subject}' not supported.")

    runner = InMemoryRunner(agent=module_extractor_agent)
    session_id = str(uuid.uuid4())
    user_id = "commuter"

    try:
        # Extract text from syllabus
        raw_text = parse_syllabus_pdf(subject)
        
        # Run agent flow
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        user_message = Content(parts=[Part(text=raw_text)])
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            pass
            
        updated_session = await runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Output schema guarantees dict/object containing modules
        agent_output = updated_session.state.get("modules")
        
        # Cleanup session to prevent memory leaks
        await runner.session_service.delete_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Ensure it is a list of strings
        if agent_output and isinstance(agent_output, dict):
            modules = agent_output.get("modules", [])
        elif agent_output and isinstance(agent_output, list):
            modules = agent_output
        else:
            modules = []
            
        if not modules:
            raise ValueError("No modules extracted by agent")
            
        return modules
        
    except APIError as e:
        # Try session cleanup
        try:
            await runner.session_service.delete_session(app_name=runner.app_name, user_id=user_id, session_id=session_id)
        except Exception:
            pass
            
        if e.code == 429:
            logger.warning(f"Module agent rate limited (429). Falling back to mock modules for '{matched_subject}'.")
        else:
            logger.error(f"Module agent API error (code={e.code}): {e.message}", exc_info=True)
        return MOCK_MODULES[matched_subject]
        
    except Exception as e:
        logger.error(f"Unexpected error in get_modules: {str(e)}", exc_info=True)
        # Try session cleanup
        try:
            await runner.session_service.delete_session(app_name=runner.app_name, user_id=user_id, session_id=session_id)
        except Exception:
            pass
        return MOCK_MODULES[matched_subject]
