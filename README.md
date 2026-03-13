# 🩺 MedTriage AI — AI-Powered Medical Symptom Triage

> End-to-end healthcare AI system: NLP symptom extraction → ML disease prediction → risk-stratified triage.
> Built by **Vidhya ES** | AI/ML Engineer

---

## 🏗️ Architecture

```
Patient Input (free text / symptom checklist)
        │
        ▼
NLP Pipeline (symptom_aliases.py + spaCy)
 - Text normalization
 - Multi-word phrase matching
 - Symptom synonym expansion
        │
        ▼
Feature Vector (binary symptom encoding)
        │
        ▼
RandomForestClassifier (300 trees, calibrated)
 - 15 disease classes
 - Trained on 4,500 synthetic samples
 - Cross-validated accuracy ~92%
        │
        ▼
Triage Engine
 - Urgency scoring (low / moderate / high / urgent)
 - Disease-specific clinical advice
 - Duration-based risk escalation
        │
        ▼
React Frontend (real-time results + probability bars)
```

---

## 🚀 Quick Start

### Backend

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Train the model (generates synthetic data + saves artifacts)
python backend/train_model.py

# 3. Run the API server
python backend/app.py
# → http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

---

## 📂 Project Structure

```
medtriage/
├── backend/
│   ├── app.py                    # Flask REST API
│   ├── train_model.py            # Model training pipeline
│   ├── data/
│   │   └── generate_dataset.py   # Synthetic dataset builder
│   ├── models/                   # Trained model artifacts (auto-generated)
│   │   ├── disease_classifier.pkl
│   │   ├── label_encoder.pkl
│   │   ├── symptom_columns.pkl
│   │   ├── risk_map.json
│   │   └── symptoms_list.json
│   └── utils/
│       ├── nlp_pipeline.py       # Symptom extraction from free text
│       └── triage_engine.py      # Risk classification & recommendations
├── frontend/
│   ├── src/
│   │   └── App.jsx               # React UI
│   ├── package.json
│   └── vite.config.js
├── notebooks/
│   └── model_exploration.ipynb   # Jupyter EDA + model analysis
└── requirements.txt
```

---

## 🔌 API Endpoints

### `POST /api/triage`
Free-text symptom analysis.
```json
{
  "text": "fever, severe headache and joint pain for 3 days",
  "duration_days": 3
}
```

### `POST /api/triage/symptoms`
Structured symptom checkbox input.
```json
{
  "symptoms": ["fever", "joint_pain", "rash"],
  "duration_days": 2
}
```

### `GET /api/symptoms`
Returns all known symptom names for frontend autocomplete.

### `GET /api/health`
Health check endpoint.

---

## 🧪 Disease Classes

| Disease | Risk Level |
|---------|-----------|
| Common Cold | Low |
| Migraine | Low |
| Viral Fever | Moderate |
| Influenza | Moderate |
| Food Poisoning | Moderate |
| Gastroenteritis | Moderate |
| UTI | Moderate |
| Anemia | Moderate |
| Dengue Fever | High |
| Malaria | High |
| Hypertension | High |
| Diabetes (Type 2) | High |
| Asthma | High |
| Pneumonia | Urgent |
| Appendicitis | Urgent |

---

## 🔮 Future Roadmap

- [ ] LLM integration (Claude/GPT) for clinical reasoning
- [ ] Medical knowledge graph (UMLS / SNOMED CT)
- [ ] EHR compatibility (HL7 FHIR)
- [ ] Docker + AWS deployment
- [ ] Multilingual support (Hindi, Tamil)
- [ ] Telemedicine handoff integration

---

## ⚠️ Disclaimer

This project is **for educational and research purposes only**. It does not constitute medical advice. Always consult a qualified healthcare professional.

---

**Author:** Vidhya ES · AI/ML Engineer  
**GitHub:** https://github.com/VidhyaES  
**Portfolio:** https://vidhya-es-portfolio.vercel.app/
