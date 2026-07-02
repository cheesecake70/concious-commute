import pytest
from backend.security.input_validator import InputValidator

def test_sanitize_string():
    validator = InputValidator()
    # Should strip HTML-like injections and special characters but keep alphanumeric, spaces, hyphens, periods, colons
    assert validator.sanitize_string("hello <script>alert(1)</script>") == "hello scriptalert1script"
    assert validator.sanitize_string("Module 1: Laplace Transform") == "Module 1: Laplace Transform"
    assert validator.sanitize_string("A-B. C") == "A-B. C"
    assert validator.sanitize_string("") == ""

def test_validate_generate_request_success():
    validator = InputValidator()
    # Using valid stations in the graph
    res = validator.validate_generate_request("Churchgate", "Mumbai Central", "Data Structures", "Module 3: Linked Lists")
    assert res["source"] == "Churchgate"
    assert res["destination"] == "Mumbai Central"
    assert res["subject"] == "Data Structures"
    assert res["module"] == "Module 3: Linked Lists"

def test_validate_generate_request_failures():
    validator = InputValidator()
    
    # Invalid stations
    with pytest.raises(ValueError, match="Invalid source station"):
        validator.validate_generate_request("Nonexistent Station", "Mumbai Central", "Data Structures")
        
    # Unsupported subject
    with pytest.raises(ValueError, match="Unsupported subject"):
        validator.validate_generate_request("Churchgate", "Mumbai Central", "Astrophysics")
        
    # Missing fields
    with pytest.raises(ValueError, match="All fields"):
        validator.validate_generate_request("", "Mumbai Central", "Data Structures")
        
    # Input too long
    long_str = "a" * 101
    with pytest.raises(ValueError, match="Input fields must not exceed 100 characters"):
        validator.validate_generate_request(long_str, "Mumbai Central", "Data Structures")
