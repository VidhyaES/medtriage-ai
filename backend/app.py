import os, sys, json, time, logging
import numpy as np
from flask import Flask, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.nlp_pipeline import extract_symptoms, build_feature_vector
from utils.triage_engine import get_triage
import joblib

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MedTriage")

MODEL_DIR = os.path.join(BASE_DIR, "models")

try:
    clf          = joblib.load(os.path.join(MODEL_DIR, "disease_classifier.pkl"))
    le           = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
    symptom_cols = joblib.load(os.path.join(MODEL_DIR, "symptom_columns.pkl"))
    with open(os.path.join(MODEL_DIR, "risk_map.json")) as f:
        risk_map = {r["disease"]: r["risk_level"] for r in json.load(f)}
    logger.info(f"✅ Models loaded — {len(symptom_cols)} symptoms, {len(le.classes_)} diseases")
except FileNotFoundError:
    logger.warning("⚠️  Models not found — run: python backend/train_model.py")
    clf = le = symptom_cols = risk_map = None

@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options(p): return jsonify({}), 200

@app.route("/api/health")
def health():
    return jsonify({"status":"ok","models_loaded": clf is not None})

@app.route("/api/symptoms")
def symptoms():
    if not symptom_cols: return jsonify({"error":"Models not loaded"}), 503
    return jsonify({"symptoms": symptom_cols})

def _predict(fvec, top_n=5):
    X   = np.array(fvec, dtype=np.float32).reshape(1,-1)
    proba = clf.predict_proba(X)[0]
    idx   = np.argsort(proba)[::-1][:top_n]
    out   = []
    for i in idx:
        p = float(proba[i])
        if p < 0.01: break
        out.append({"disease": le.classes_[i], "probability": round(p,4),
                    "probability_pct": round(p*100,1),
                    "risk_level": risk_map.get(le.classes_[i],"moderate")})
    return out

@app.route("/api/triage", methods=["POST"])
def triage():
    if clf is None: return jsonify({"error":"Model not loaded"}), 503
    body = request.get_json(silent=True) or {}
    text = body.get("text","").strip()
    dur  = body.get("duration_days")
    if not text: return jsonify({"error":"Field 'text' is required"}), 400

    feat, detected = extract_symptoms(text, symptom_cols)
    if sum(feat.values()) == 0:
        return jsonify({"error":"No recognizable symptoms found. Try: fever, headache, cough etc."}), 422

    fvec  = build_feature_vector(feat, symptom_cols)
    preds = _predict(fvec)
    result = get_triage(preds, detected, duration_days=dur)
    return jsonify({"input_text": text, "detected_symptoms": detected, "triage": result})

if __name__ == "__main__":
    logger.info("🚀 Starting MedTriage API on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)