RISK_CONFIG = {
    "low":      {"label":"Low Risk",     "color":"#22c55e","icon":"✅","action":"Self-Care",                "recommendation":"Your symptoms appear mild. Rest, stay hydrated, and monitor your condition. If symptoms worsen or persist beyond 3–5 days, consult a healthcare provider.","urgency":0},
    "moderate": {"label":"Moderate Risk","color":"#f59e0b","icon":"⚠️","action":"Doctor Consultation",     "recommendation":"Your symptoms warrant professional medical evaluation. Schedule an appointment with a doctor within 24–48 hours. If symptoms escalate suddenly, seek care immediately.","urgency":1},
    "high":     {"label":"High Risk",    "color":"#f97316","icon":"🚨","action":"Urgent Medical Attention","recommendation":"Your symptoms indicate a condition requiring prompt medical care. Visit a clinic or urgent care facility today. Do not delay.","urgency":2},
    "urgent":   {"label":"Emergency",    "color":"#ef4444","icon":"🆘","action":"Go to Emergency Room",    "recommendation":"This is a medical emergency. Go to the nearest emergency room or call emergency services (112 / 108) immediately.","urgency":3},
}

DISEASE_ADVICE = {
    "Dengue Fever":     "Avoid aspirin/ibuprofen — use paracetamol only. Watch for bleeding or persistent vomiting.",
    "Malaria":          "Requires blood smear test. Start antimalarials only under physician guidance.",
    "Pneumonia":        "Chest X-ray and antibiotic therapy may be needed. Hospitalization likely for elderly.",
    "Appendicitis":     "Surgical evaluation is urgent. Do not eat or drink until assessed by a doctor.",
    "Hypertension":     "Monitor BP regularly. Low-salt diet. Medication compliance is critical.",
    "Asthma":           "Use rescue inhaler as prescribed. Avoid known triggers.",
    "Diabetes (Type 2)":"Monitor blood glucose. Follow dietary plan. Medication adherence is essential.",
    "Migraine":         "Rest in a quiet, dark room. Track triggers in a headache diary.",
    "UTI":              "Complete the full antibiotic course. Increase fluid intake.",
}

DISCLAIMER = "⚠️ This AI triage is for informational purposes only. It does not constitute medical advice. Always consult a qualified healthcare professional."

def get_triage(predictions, detected_symptoms, duration_days=None):
    if not predictions:
        return {"risk_level":"unknown","recommendation":"Unable to assess. Please describe symptoms in more detail.","disclaimer":DISCLAIMER}

    urgency_score = 0
    for pred in predictions[:3]:
        rl  = pred.get("risk_level","low")
        cfg = RISK_CONFIG.get(rl, RISK_CONFIG["low"])
        urgency_score += cfg["urgency"] * pred["probability"]

    if urgency_score >= 2.5:   risk_key = "urgent"
    elif urgency_score >= 1.5: risk_key = "high"
    elif urgency_score >= 0.7: risk_key = "moderate"
    else:                      risk_key = "low"

    if duration_days and duration_days > 7  and risk_key == "low":      risk_key = "moderate"
    if duration_days and duration_days > 14 and risk_key == "moderate": risk_key = "high"

    ri  = RISK_CONFIG[risk_key]
    top = predictions[0]["disease"]
    advice = DISEASE_ADVICE.get(top,"")
    rec = ri["recommendation"]
    if advice:
        rec += f"\n\n💊 Note for {top}: {advice}"

    return {
        "risk_level":        risk_key,
        "risk_info":         {"label":ri["label"],"color":ri["color"],"icon":ri["icon"],"action":ri["action"]},
        "top_prediction":    top,
        "predictions":       predictions,
        "detected_symptoms": detected_symptoms,
        "recommendation":    rec,
        "duration_days":     duration_days,
        "disclaimer":        DISCLAIMER,
    }