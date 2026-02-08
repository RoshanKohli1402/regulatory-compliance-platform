from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import json
import re
import tempfile
import os
from pathlib import Path
from pydantic import BaseModel
from PyPDF2 import PdfReader
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------
# App initialization
# -----------------------
app = FastAPI(
    title="Global Regulatory Compliance Engine",
    description="Multi-jurisdiction regulatory compliance analyzer",
    version="2.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Data models
# -----------------------
class RegulationInfo(BaseModel):
    id: str
    name: str
    jurisdiction: str
    region: str
    regulatory_body: str
    description: str

class AnalysisResult(BaseModel):
    page: int
    clause: str
    business_unit: str
    risk_score: int
    priority: str
    decision_source: str
    confidence: float

class AnalysisResponse(BaseModel):
    filename: str
    detected_regulation: str
    regulation_name: str
    total_findings: int
    high_priority_count: int
    medium_priority_count: int
    results: List[AnalysisResult]

# -----------------------
# Global regulation loader
# -----------------------
REGULATIONS_DIR = Path(__file__).parent / "regulations"
REGULATIONS: Dict[str, dict] = {}

def load_regulations():
    """Load all regulation configurations from the regulations directory"""
    global REGULATIONS
    
    if not REGULATIONS_DIR.exists():
        print(f"Warning: Regulations directory not found at {REGULATIONS_DIR}")
        return
    
    for reg_file in REGULATIONS_DIR.glob("*.json"):
        if reg_file.name.startswith("_"):
            continue
        try:
            with open(reg_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                REGULATIONS[config["id"]] = config
                print(f"Loaded regulation: {config['name']}")
        except Exception as e:
            print(f"Error loading {reg_file}: {e}")

# Load regulations on startup
load_regulations()

# -----------------------
# PDF extraction using PyPDF2
# -----------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyPDF2"""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

# -----------------------
# Document type detection
# -----------------------
def detect_regulation(text: str) -> str:
    """
    Auto-detect which regulation applies to this document
    by matching document patterns
    """
    text_lower = text.lower()
    
    scores = {}
    for reg_id, config in REGULATIONS.items():
        score = 0
        patterns = config.get("document_patterns", [])
        
        for pattern in patterns:
            if pattern.lower() in text_lower:
                score += 1
        
        scores[reg_id] = score
    
    # Return regulation with highest score, or default to first available
    if scores:
        best_match = max(scores.items(), key=lambda x: x[1])
        if best_match[1] > 0:
            return best_match[0]
    
    # Default fallback
    return list(REGULATIONS.keys())[0] if REGULATIONS else "us_sec_10k"

# -----------------------
# Analysis functions
# -----------------------
def classify_obligation(sentence: str, config: dict) -> tuple:
    """Classify if sentence contains an obligation (rule-based only)"""
    s = sentence.lower()
    keywords = config["obligation_keywords"]
    
    # Rule-based classification
    if any(k in s for k in keywords):
        return 1, "rule", 1.0
    
    return 0, "none", 0.0

def map_business_unit(text: str, config: dict) -> str:
    """Map text to business unit based on keywords"""
    text_lower = text.lower()
    business_rules = config["business_unit_rules"]
    
    for unit, keywords in business_rules.items():
        for kw in keywords:
            if kw in text_lower:
                return unit
    
    return "Unclassified"

def get_risk_score(unit: str, config: dict) -> int:
    """Get risk score for business unit"""
    return config["risk_scores"].get(unit, 1)

# -----------------------
# API Endpoints
# -----------------------
@app.get("/")
def health_check():
    return {
        "status": "running",
        "version": "2.0.0",
        "regulations_loaded": len(REGULATIONS)
    }

@app.get("/regulations", response_model=List[RegulationInfo])
def list_regulations():
    """List all available regulation frameworks"""
    return [
        RegulationInfo(
            id=config["id"],
            name=config["name"],
            jurisdiction=config["jurisdiction"],
            region=config["region"],
            regulatory_body=config["regulatory_body"],
            description=config["description"]
        )
        for config in REGULATIONS.values()
    ]

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    regulation_id: Optional[str] = None
):
    """
    Analyze a regulatory document
    
    - **file**: PDF document to analyze
    - **regulation_id**: Optional - specify regulation framework, otherwise auto-detect
    """
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    results = []
    
    try:
        # Extract text from PDF
        full_text = extract_text_from_pdf(tmp_path)
        
        # Detect or use specified regulation
        if regulation_id and regulation_id in REGULATIONS:
            detected_reg = regulation_id
        else:
            detected_reg = detect_regulation(full_text)
        
        if detected_reg not in REGULATIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Regulation '{detected_reg}' not found"
            )
        
        config = REGULATIONS[detected_reg]
        
        # Split into sentences and analyze
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 30:
                continue
            
            label, source, confidence = classify_obligation(sentence, config)
            
            if label == 1:
                unit = map_business_unit(sentence, config)
                risk = get_risk_score(unit, config)
                
                results.append({
                    "page": 1,  # PyPDF2 doesn't track page numbers easily
                    "clause": sentence,
                    "business_unit": unit,
                    "risk_score": risk,
                    "priority": "HIGH" if risk >= 3 else "MEDIUM",
                    "decision_source": source,
                    "confidence": round(confidence, 3)
                })
        
        # Sort by risk score
        results.sort(key=lambda x: x["risk_score"], reverse=True)
        
        # Count priorities
        high_count = sum(1 for r in results if r["priority"] == "HIGH")
        medium_count = sum(1 for r in results if r["priority"] == "MEDIUM")
        
        return AnalysisResponse(
            filename=file.filename,
            detected_regulation=detected_reg,
            regulation_name=config["name"],
            total_findings=len(results),
            high_priority_count=high_count,
            medium_priority_count=medium_count,
            results=results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")
    
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/regulations/{regulation_id}")
def get_regulation_details(regulation_id: str):
    """Get details of a specific regulation framework"""
    if regulation_id not in REGULATIONS:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    return REGULATIONS[regulation_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    