import os
from utils.pdf_loader import PDFLoader

def parse_syllabus_pdf(subject: str) -> str:
    """
    Reads the syllabus PDF file for a given subject and returns its raw text.
    
    Args:
        subject: The name of the subject. Supported subjects:
                 "Engineering Mathematics III", "Data Structures",
                 "Signals and Systems", "Engineering Mechanics".
                 
    Returns:
        The extracted syllabus text containing module topics.
    """
    subject_map = {
        "engineering mathematics iii": "engineering_maths_3.pdf",
        "engineering maths 3": "engineering_maths_3.pdf",
        "maths": "engineering_maths_3.pdf",
        "data structures": "data_structures.pdf",
        "signals and systems": "signals_and_systems.pdf",
        "engineering mechanics": "engineering_mechanics.pdf",
        "mechanics": "engineering_mechanics.pdf",
        "corporate finance": "corporate_finance.pdf",
        "finance": "corporate_finance.pdf",
        "financial accounting": "financial_accounting.pdf",
        "accounting": "financial_accounting.pdf",
        "marketing management": "marketing_management.pdf",
        "marketing": "marketing_management.pdf",
        "human resource management": "human_resource_management.pdf",
        "hrm": "human_resource_management.pdf",
        "macroeconomics": "macroeconomics.pdf",
        "economics": "macroeconomics.pdf",
        "business law": "business_law.pdf",
        "law": "business_law.pdf"
    }
    
    name = subject.lower().strip()
    matched_file = subject_map.get(name)
    
    if not matched_file:
        name_words = set(name.split())
        for k, v in subject_map.items():
            k_words = set(k.split())
            if name_words.issubset(k_words) or k_words.issubset(name_words):
                matched_file = v
                break
            
    if not matched_file:
        supported = [s.title() for s in set(subject_map.values())]
        raise ValueError(f"Subject '{subject}' is not supported. Please select from: {', '.join(supported)}")
        
    pdf_path = os.path.join("data", "syllabi", matched_file)
    return PDFLoader.extract_text(pdf_path)
