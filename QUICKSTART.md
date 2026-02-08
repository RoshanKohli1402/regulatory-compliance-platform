# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Option 1: Standard Setup (Recommended)

### Step 1: Install Dependencies

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
setup.bat
```

### Step 2: Start the Backend

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat  # Windows

# Start server
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Loaded regulation: US SEC Form 10-K
Loaded regulation: EU General Data Protection Regulation
Loaded regulation: SOC 2 Type II
Loaded regulation: US HIPAA
```

### Step 3: Open the UI

Open `frontend.html` in your web browser, or:

```bash
# Serve with Python
python -m http.server 3000
# Then visit: http://localhost:3000/frontend.html
```

### Step 4: Test It!

1. Click "Select PDF File" or drag a regulatory PDF
2. Choose a regulation framework (or use auto-detect)
3. Click "Analyze Document"
4. View your compliance findings!

---

## Option 2: Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Steps

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## First Time Testing

### Get Sample Documents

If you don't have regulatory documents handy, you can:

1. **SEC 10-K**: Download from https://www.sec.gov/edgar/
2. **GDPR**: Search for "GDPR compliance policy PDF"
3. **SOC 2**: Use your organization's SOC 2 report
4. **HIPAA**: Search for "HIPAA privacy policy PDF"

### What to Expect

The analyzer will:
- ✅ Extract regulatory obligations from your PDF
- ✅ Classify them by business unit
- ✅ Assign risk scores (1-3)
- ✅ Prioritize HIGH vs MEDIUM priority items
- ✅ Show confidence scores

---

## Common Issues & Solutions

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Regulations not loading"
Check that regulation JSON files are in the `regulations/` folder:
```bash
ls regulations/
# Should show: us_sec_10k.json, eu_gdpr.json, soc2.json, us_hipaa.json
```

### CORS errors in browser
Make sure:
1. Backend is running on port 8000
2. You're opening `frontend.html` (not a random HTML file)
3. Check browser console for specific errors

### "ML models not available" warning
This is **normal** and **OK**! The system works without ML models using rule-based detection. ML is only for edge cases.

---

## Next Steps

### Add Your Own Regulation

1. Copy `regulations/_TEMPLATE.json`
2. Rename to `regulations/your_regulation.json`
3. Fill in the details:
   - Document patterns (for auto-detection)
   - Obligation keywords
   - Business unit mappings
   - Risk scores
4. Restart the server
5. Your regulation appears in the UI!

### Train ML Models (Optional)

Use your existing training code or:

```python
# Example training script
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Your training code here...
# Then save:
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")
joblib.dump(model, "models/logistic_model.joblib")
```

Restart the server and ML will be used automatically.

---

## API Testing

### Using curl

```bash
# List regulations
curl http://localhost:8000/regulations

# Analyze document
curl -X POST http://localhost:8000/analyze \
  -F "file=@your_document.pdf"

# Specify regulation
curl -X POST "http://localhost:8000/analyze?regulation_id=eu_gdpr" \
  -F "file=@privacy_policy.pdf"
```

### Using Python

```python
import requests

# Analyze document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f}
    )
    results = response.json()
    
print(f"Found {results['total_findings']} compliance items")
for item in results['results'][:5]:  # First 5
    print(f"- {item['clause'][:100]}...")
```

### Using Postman

1. Create new request: `POST http://localhost:8000/analyze`
2. Go to Body → form-data
3. Add key: `file`, type: File
4. Upload your PDF
5. Send!

---

## Production Deployment

### Environment Variables

Create `.env` file:
```bash
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourdomain.com
```

### Security Considerations

1. **Add authentication** for API endpoints
2. **Rate limiting** to prevent abuse
3. **File size limits** for uploads
4. **HTTPS** in production
5. **Input validation** for regulation_id parameter

### Scaling

- Use **Gunicorn** or **Nginx** for production
- Deploy on **AWS**, **GCP**, **Azure**
- Use **Docker Swarm** or **Kubernetes** for orchestration

---

## Support & Resources

- 📖 Full documentation: `README.md`
- 🔧 API documentation: http://localhost:8000/docs
- 📝 Regulation template: `regulations/_TEMPLATE.json`
- 🐳 Docker setup: `docker-compose.yml`

**You're all set!** Start analyzing regulatory documents! 🎉
