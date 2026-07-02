import re
from utils.railway_graph import RailwayGraph

class InputValidator:
    def __init__(self):
        self.rg = RailwayGraph()
        self.valid_stations = set(self.rg.get_stations())
        self.valid_subjects = {
            "engineering mathematics iii",
            "engineering maths 3",
            "maths",
            "data structures",
            "signals and systems",
            "engineering mechanics",
            "mechanics",
            "corporate finance",
            "finance",
            "financial accounting",
            "accounting",
            "marketing management",
            "marketing",
            "human resource management",
            "human resource",
            "hrm",
            "macroeconomics",
            "economics",
            "business law",
            "law"
        }

    def sanitize_string(self, val: str) -> str:
        if not val:
            return ""
        # Remove any non-alphanumeric/spaces/hyphen/period/colon characters to prevent injections.
        # Allowing colons (:) is necessary to preserve structured chapter prefixes like 'Module 1: ...'
        # while stripping out potential scripting or shell tags (<, >, ', ", etc.).
        return re.sub(r"[^\w\s\-\.\:]", "", val).strip()

    def validate_generate_request(self, source: str, destination: str, subject: str, module: str = "any module") -> dict:
        """
        Validates the source, destination, subject and module inputs.
        Returns a dict of sanitized inputs, or raises ValueError.
        """
        # Sanitize all string parameters using our strict allowed-characters pattern
        san_source = self.sanitize_string(source)
        san_destination = self.sanitize_string(destination)
        san_subject = self.sanitize_string(subject)
        san_module = self.sanitize_string(module)

        if not san_source or not san_destination or not san_subject or not san_module:
            raise ValueError("All fields (source, destination, subject, module) are required.")

        # Enforce max length bounds (100 characters) on all input strings to prevent 
        # regex-based Denial of Service (ReDoS) and memory exhaustion from oversized payloads.
        if len(san_source) > 100 or len(san_destination) > 100 or len(san_subject) > 100 or len(san_module) > 100:
            raise ValueError("Input fields must not exceed 100 characters.")

        # Check if stations exist in railway graph
        if san_source not in self.valid_stations:
            raise ValueError(f"Invalid source station: '{source}'")
        if san_destination not in self.valid_stations:
            raise ValueError(f"Invalid destination station: '{destination}'")

        # Check if subject is supported
        if san_subject.lower() not in self.valid_subjects:
            raise ValueError(f"Unsupported subject: '{subject}'. Please select a valid subject.")

        return {
            "source": san_source,
            "destination": san_destination,
            "subject": san_subject,
            "module": san_module
        }
