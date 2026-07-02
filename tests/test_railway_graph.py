from utils.railway_graph import RailwayGraph
from utils.pdf_loader import PDFLoader
import os

def test_railway_calculations():
    rg = RailwayGraph()
    # Test Western Line same-line travel (Churchgate -> Andheri)
    time, path = rg.calculate_travel_time("Churchgate", "Andheri")
    print(f"Churchgate to Andheri: {time} mins, Path: {path}")
    assert time is not None
    assert time == 33  # 2+2+2+2+2+3+2+2+2+2+3+2+2+2+3
    assert "Churchgate" in path
    assert "Andheri" in path

    # Test transfer Dadar (Western to Central: Churchgate -> Thane)
    time, path = rg.calculate_travel_time("Churchgate", "Thane")
    print(f"Churchgate to Thane: {time} mins, Path: {path}")
    # Western to Dadar is 19 mins. Transfer is 5 mins. Dadar to Thane on Central is 34 mins. Total = 58 mins.
    assert time is not None
    assert time == 58
    assert "Dadar" in path

    # Test that peak hour calculation is disabled (no delay added)
    peak_time, _ = rg.calculate_travel_time("Churchgate", "Thane", is_peak=True)
    assert peak_time == 58

def test_pdf_extraction():
    # Test reading data_structures.pdf
    pdf_path = "data/syllabi/data_structures.pdf"
    assert os.path.exists(pdf_path)
    text = PDFLoader.extract_text(pdf_path)
    print(f"Extracted {len(text)} chars from data_structures.pdf")
    assert "Data Structures" in text
    assert "Module 1" in text

if __name__ == "__main__":
    test_railway_calculations()
    test_pdf_extraction()
    print("All utility checks passed successfully!")
