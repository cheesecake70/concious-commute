from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    source: str = Field(..., max_length=100, description="Starting station name")
    destination: str = Field(..., max_length=100, description="Destination station name")
    subject: str = Field(..., max_length=100, description="Subject name (e.g. Data Structures)")
    is_peak: bool = Field(default=False, description="Whether the travel is during peak train hours")
    module: str = Field(default="any module", max_length=100, description="Specific module or chapter to study")
