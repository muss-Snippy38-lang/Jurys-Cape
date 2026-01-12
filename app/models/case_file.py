from pydantic import BaseModel
from typing import List, Optional

# What the frontend sends you
class CaseFileRequest(BaseModel):
    case_id: str
    case_text: str
    doc_type: str = "FIR"  # Default to FIR

# What you send back
class FactExtractionResponse(BaseModel):
    case_id: str
    chronological_facts: List[str]
    potential_bns_sections: List[str]
    summary: str