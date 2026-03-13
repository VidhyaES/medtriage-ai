import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

DISEASES = {
    "Viral Fever":      {"risk":"moderate","core":["fever","headache","fatigue","body_ache","chills"],"secondary":["nausea","loss_of_appetite","sore_throat","runny_nose"]},
    "Dengue Fever":     {"risk":"high",    "core":["fever","severe_headache","joint_pain","muscle_pain","rash"],"secondary":["nausea","vomiting","eye_pain","fatigue"]},
    "Malaria":          {"risk":"high",    "core":["fever","chills","sweating","headache","muscle_pain"],"secondary":["nausea","vomiting","fatigue","anemia_symptoms"]},
    "Common Cold":      {"risk":"low",     "core":["runny_nose","sneezing","sore_throat","cough"],"secondary":["mild_fever","headache","fatigue","congestion"]},
    "Influenza":        {"risk":"moderate","core":["fever","cough","sore_throat","body_ache","fatigue"],"secondary":["headache","chills","runny_nose","vomiting"]},
    "Food Poisoning":   {"risk":"moderate","core":["nausea","vomiting","diarrhea","stomach_pain","cramps"],"secondary":["fever","fatigue","headache","loss_of_appetite"]},
    "Gastroenteritis":  {"risk":"moderate","core":["diarrhea","vomiting","stomach_pain","nausea"],"secondary":["fever","cramps","bloating","loss_of_appetite"]},
    "Migraine":         {"risk":"low",     "core":["severe_headache","nausea","light_sensitivity","sound_sensitivity"],"secondary":["vomiting","visual_disturbances","dizziness","fatigue"]},
    "Hypertension":     {"risk":"high",    "core":["headache","dizziness","chest_pain","shortness_of_breath"],"secondary":["nosebleed","blurred_vision","fatigue","palpitations"]},
    "Diabetes (Type 2)":{"risk":"high",    "core":["frequent_urination","excessive_thirst","fatigue","blurred_vision"],"secondary":["slow_healing","weight_loss","tingling","hunger"]},
    "Asthma":           {"risk":"high",    "core":["shortness_of_breath","wheezing","chest_tightness","cough"],"secondary":["fatigue","anxiety","sleep_disturbance","reduced_activity"]},
    "Pneumonia":        {"risk":"urgent",  "core":["fever","cough","shortness_of_breath","chest_pain","fatigue"],"secondary":["chills","sweating","nausea","confusion"]},
    "UTI":              {"risk":"moderate","core":["burning_urination","frequent_urination","pelvic_pain","cloudy_urine"],"secondary":["fever","back_pain","fatigue","strong_urine_odor"]},
    "Anemia":           {"risk":"moderate","core":["fatigue","pale_skin","shortness_of_breath","dizziness"],"secondary":["cold_hands","chest_pain","headache","weakness"]},
    "Appendicitis":     {"risk":"urgent",  "core":["severe_abdominal_pain","fever","nausea","vomiting","loss_of_appetite"],"secondary":["diarrhea","constipation","bloating","inability_to_pass_gas"]},
}

ALL_SYMPTOMS = sorted(set(s for d in DISEASES.values() for s in d["core"] + d["secondary"]))
RISK_MAP = {"low":0,"moderate":1,"high":2,"urgent":3}

def generate_sample(disease_name, info):
    row = {s: 0 for s in ALL_SYMPTOMS}
    for s in info["core"]:
        if s in row: row[s] = 1
    for s in random.sample(info["secondary"], min(random.randint(0,3), len(info["secondary"]))):
        if s in row: row[s] = 1
    noise = [s for s in ALL_SYMPTOMS if row[s] == 0]
    for s in random.sample(noise, min(random.randint(0,2), len(noise))):
        row[s] = 1
    row["disease"]    = disease_name
    row["risk_level"] = info["risk"]
    row["risk_score"] = RISK_MAP[info["risk"]]
    return row

def build_dataset(n_per_disease=300):
    rows = []
    for name, info in DISEASES.items():
        for _ in range(n_per_disease):
            rows.append(generate_sample(name, info))
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    return df

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "training_data.csv")
    df = build_dataset()
    df.to_csv(out, index=False)
    print(f"Dataset saved → {out}  |  Rows: {len(df)}")