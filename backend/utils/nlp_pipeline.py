import re

SYMPTOM_ALIASES = {
    "fever":                ["fever","high temperature","pyrexia","febrile"],
    "headache":             ["headache","head pain","head ache","head hurts"],
    "severe_headache":      ["severe headache","throbbing headache","intense headache"],
    "nausea":               ["nausea","nauseous","queasy","feel sick"],
    "vomiting":             ["vomiting","vomit","throwing up","puking"],
    "diarrhea":             ["diarrhea","diarrhoea","loose stools","loose motions"],
    "cough":                ["cough","coughing","dry cough","wet cough"],
    "shortness_of_breath":  ["shortness of breath","breathless","difficulty breathing","dyspnea"],
    "chest_pain":           ["chest pain","chest tightness","chest pressure"],
    "chest_tightness":      ["chest tightness","tight chest","chest constriction"],
    "fatigue":              ["fatigue","tired","exhausted","weakness","lethargy","weak"],
    "body_ache":            ["body ache","body pain","aching all over","myalgia"],
    "muscle_pain":          ["muscle pain","muscle ache","muscular pain"],
    "joint_pain":           ["joint pain","joint ache","arthralgia"],
    "chills":               ["chills","shivering","rigors","shaking cold"],
    "sweating":             ["sweating","excessive sweating","night sweats"],
    "rash":                 ["rash","skin rash","hives","red spots"],
    "sore_throat":          ["sore throat","throat pain","throat ache"],
    "runny_nose":           ["runny nose","nasal discharge","dripping nose"],
    "congestion":           ["congestion","stuffy nose","blocked nose"],
    "sneezing":             ["sneezing","sneeze"],
    "dizziness":            ["dizziness","dizzy","vertigo","lightheaded","light headed"],
    "stomach_pain":         ["stomach pain","abdominal pain","belly pain","tummy ache"],
    "severe_abdominal_pain":["severe abdominal pain","acute abdomen","sharp stomach pain"],
    "cramps":               ["cramps","cramping","stomach cramps"],
    "bloating":             ["bloating","bloated","distended abdomen"],
    "loss_of_appetite":     ["loss of appetite","not hungry","no appetite"],
    "frequent_urination":   ["frequent urination","urinating often","polyuria"],
    "burning_urination":    ["burning urination","painful urination","dysuria"],
    "pelvic_pain":          ["pelvic pain","lower abdominal pain","groin pain"],
    "back_pain":            ["back pain","lower back pain","backache"],
    "eye_pain":             ["eye pain","painful eyes","eyes hurt"],
    "light_sensitivity":    ["light sensitivity","photophobia","sensitive to light"],
    "sound_sensitivity":    ["sound sensitivity","sensitive to sound"],
    "blurred_vision":       ["blurred vision","blurry vision","vision problems"],
    "visual_disturbances":  ["visual disturbances","aura","seeing spots"],
    "palpitations":         ["palpitations","heart racing","rapid heartbeat"],
    "nosebleed":            ["nosebleed","nose bleed","epistaxis"],
    "excessive_thirst":     ["excessive thirst","very thirsty","always thirsty"],
    "weight_loss":          ["weight loss","losing weight","unexplained weight loss"],
    "tingling":             ["tingling","pins and needles","numbness"],
    "hunger":               ["hunger","always hungry","excessive hunger"],
    "slow_healing":         ["slow healing","wounds not healing"],
    "wheezing":             ["wheezing","wheeze","whistling breath"],
    "pale_skin":            ["pale skin","pallor","paleness"],
    "cold_hands":           ["cold hands","cold extremities"],
    "anemia_symptoms":      ["anemia","low blood","iron deficiency"],
    "confusion":            ["confusion","confused","disoriented"],
    "anxiety":              ["anxiety","anxious","nervous"],
    "sleep_disturbance":    ["sleep disturbance","insomnia","cant sleep"],
    "reduced_activity":     ["reduced activity","exercise intolerance"],
    "inability_to_pass_gas":["inability to pass gas","cant pass gas"],
    "constipation":         ["constipation","constipated","hard stools"],
    "mild_fever":           ["mild fever","slight fever","low grade fever"],
    "strong_urine_odor":    ["strong urine odor","smelly urine"],
    "cloudy_urine":         ["cloudy urine","turbid urine"],
    "weakness":             ["weakness","weak","no strength"],
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_symptoms(text, symptom_columns):
    norm = normalize_text(text)
    detected = set()
    for key, aliases in sorted(SYMPTOM_ALIASES.items(), key=lambda x: -max(len(a) for a in x[1])):
        for alias in aliases:
            if alias in norm:
                if key in symptom_columns:
                    detected.add(key)
                break
    feature_vec = {col: 1 if col in detected else 0 for col in symptom_columns}
    return feature_vec, sorted(detected)

def build_feature_vector(feature_dict, symptom_columns):
    return [feature_dict.get(col, 0) for col in symptom_columns]