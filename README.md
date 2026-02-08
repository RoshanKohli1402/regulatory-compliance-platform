# 🌍 Global Regulatory Compliance Auditor

A powerful AI-driven regulatory compliance analysis tool that supports multiple international frameworks with automatic regulation detection, ML-powered clause extraction, and a beautiful modern UI.

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Jurisdiction Support**: Pre-configured for US SEC 10-K, EU GDPR, SOC 2, HIPAA, and easily extensible
- **Auto-Detection**: Automatically identifies the regulation type from document content
- **Hybrid Classification**: Combines rule-based and ML approaches for accurate obligation detection
- **Risk Scoring**: Intelligent risk assessment and prioritization
- **Business Unit Mapping**: Routes compliance items to relevant departments
- **Modern UI**: Professional React-based dashboard with real-time analysis

### 🌐 Supported Regulations
1. **US SEC Form 10-K** - Annual financial reporting
2. **EU GDPR** - Data protection and privacy
3. **SOC 2 Type II** - Service organization controls
4. **US HIPAA** - Healthcare data protection

### 🚀 Easy to Extend
Adding a new regulation takes just **5 minutes**:
1. Create a JSON config file
2. Define obligation keywords
3. Map business units
4. Set risk scores

## 📁 Project Structure

```
regulatory-auditor/
├── app.py                          # FastAPI backend
├── frontend.html                   # React UI
├── requirements.txt                # Python dependencies
├── regulations/                    # Regulation configs
│   ├── us_sec_10k.json
│   ├── eu_gdpr.json
│   ├── soc2.json
│   └── us_hipaa.json
├── models/                         # ML models (optional)
│   ├── tfidf_vectorizer.joblib
│   └── logistic_model.joblib
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone or create the project directory**
```bash
mkdir regulatory-auditor
cd regulatory-auditor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create the regulations directory**
```bash
mkdir regulations
mkdir models  # Optional, for ML models
```

4. **Copy regulation configs** to the `regulations/` folder
   - us_sec_10k.json
   - eu_gdpr.json
   - soc2.json
   - us_hipaa.json

5. **(Optional) Add ML models** to the `models/` folder
   - tfidf_vectorizer.joblib
   - logistic_model.joblib

## 🚀 Running the Application

### Start the Backend

```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### Open the Frontend

Simply open `frontend.html` in your web browser. The UI will connect to the backend at `http://localhost:8000`.

Alternatively, serve it with a simple HTTP server:
```bash
python -m http.server 3000
```

Then visit: `http://localhost:3000/frontend.html`

## 📊 Usage

### Via Web UI

1. Open `frontend.html` in your browser
2. Upload a PDF regulatory document
3. Choose a regulation framework (or use auto-detect)
4. Click "Analyze Document"
5. View compliance findings with risk scores and business unit assignments

### Via API

#### List Available Regulations
```bash
curl http://localhost:8000/regulations
```

#### Analyze a Document (Auto-detect)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@document.pdf"
```

#### Analyze with Specific Regulation
```bash
curl -X POST "http://localhost:8000/analyze?regulation_id=eu_gdpr" \
  -F "file=@gdpr_policy.pdf"
```

#### Response Format
```json
{
  "filename": "document.pdf",
  "detected_regulation": "eu_gdpr",
  "regulation_name": "EU General Data Protection Regulation",
  "total_findings": 45,
  "high_priority_count": 12,
  "medium_priority_count": 33,
  "results": [
    {
      "page": 5,
      "clause": "The data controller must implement appropriate technical measures...",
      "business_unit": "Technology / IT",
      "risk_score": 3,
      "priority": "HIGH",
      "decision_source": "rule",
      "confidence": 1.0
    }
  ]
}
```

## 🔧 Adding a New Regulation

### 1. Create a Configuration File

Create `regulations/your_regulation.json`:

```json
{
  "id": "your_regulation_id",
  "name": "Your Regulation Name",
  "jurisdiction": "Country/Region",
  "region": "Geographic Region",
  "regulatory_body": "Regulatory Authority",
  "language": "en",
  "description": "Brief description",
  
  "document_patterns": [
    "keyword1",
    "keyword2"
  ],
  
  "obligation_keywords": [
    "must",
    "shall",
    "is required to"
  ],
  
  "business_unit_rules": {
    "Department Name": [
      "keyword1",
      "keyword2"
    ]
  },
  
  "risk_scores": {
    "Department Name": 3,
    "Unclassified": 1
  },
  
  "ml_threshold": 0.8
}
```

### 2. Restart the Server

The new regulation will be automatically loaded!

### 3. Examples

Check the existing configs in the `regulations/` folder:
- `us_sec_10k.json` - Financial reporting
- `eu_gdpr.json` - Data privacy
- `soc2.json` - Security controls
- `us_hipaa.json` - Healthcare compliance

## 🎨 UI Features

- **Drag & Drop**: Upload PDFs by dragging them onto the upload area
- **Auto-Detection**: Smart identification of regulation type
- **Real-time Analysis**: Instant processing and results
- **Priority Filtering**: Filter by High/Medium priority
- **Risk Visualization**: Visual risk indicators for each finding
- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Easy on the eyes with a modern aesthetic

## 🤖 ML Enhancement (Optional)

The system works with rule-based classification out of the box. For enhanced accuracy:

1. **Train a model** using your existing training code
2. **Save the models**:
   - `tfidf_vectorizer.joblib`
   - `logistic_model.joblib`
3. **Place them** in the `models/` directory
4. **Restart** the server

The system will automatically use ML for edge cases where rule-based detection is uncertain.

## 🌍 Global Use Cases

### Financial Services
- SEC filings (US)
- MiFID II (EU)
- Basel III (Global)

### Healthcare
- HIPAA (US)
- GDPR (EU)
- PIPEDA (Canada)

### Technology
- SOC 2 (Global)
- ISO 27001 (Global)
- GDPR (EU)

### Government
- FISMA (US)
- DORA (EU)
- ITAR (US)

## 📈 Roadmap

- [ ] Multi-language support (Spanish, French, German, Chinese)
- [ ] Excel/Word export of findings
- [ ] Batch processing of multiple documents
- [ ] Compliance tracking dashboard
- [ ] Integration with GRC platforms
- [ ] PDF annotation with highlighted clauses
- [ ] Custom regulation builder UI

## 🤝 Contributing

To add a new regulation:
1. Create a JSON config following the schema
2. Test with sample documents
3. Submit with example results

## 📝 License

MIT License - feel free to use and modify!

## 💡 Tips

1. **Better Detection**: Add more `document_patterns` for accurate auto-detection
2. **Granular Units**: Create specific business units for better routing
3. **Risk Tuning**: Adjust risk scores based on your organization's priorities
4. **ML Training**: Train on your specific document types for best results

## 🐛 Troubleshooting

### "Regulations not loading"
- Ensure the `regulations/` directory exists in the same folder as `app.py`
- Check JSON syntax in config files

### "ML models not found"
- This is normal! The system works without ML models
- ML is only used as a fallback for edge cases

### "CORS errors in UI"
- Make sure the backend is running
- Check that `API_URL` in `frontend.html` matches your backend URL

## 📞 Support

For issues or questions:
1. Check the existing regulation configs for examples
2. Review the API documentation at `http://localhost:8000/docs`
3. Test with small sample PDFs first

---

**Built with ❤️ for regulatory compliance professionals worldwide**
