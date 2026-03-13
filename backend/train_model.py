import os, sys, json, joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, accuracy_score

BASE      = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "data", "training_data.csv")
MODEL_DIR = os.path.join(BASE, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# ── Generate data if missing ──────────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    print("Generating dataset...")
    sys.path.insert(0, os.path.join(BASE, "data"))
    from generate_dataset import build_dataset
    df = build_dataset()
    df.to_csv(DATA_PATH, index=False)
else:
    df = pd.read_csv(DATA_PATH)

print(f"Loaded {len(df)} rows")

# ── Features & labels ─────────────────────────────────────────────────────────
DROP   = ["disease","risk_level","risk_score"]
SCOLS  = [c for c in df.columns if c not in DROP]
X      = df[SCOLS].values.astype(np.float32)
le     = LabelEncoder()
y      = le.fit_transform(df["disease"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# ── Train ─────────────────────────────────────────────────────────────────────
print("Training model...")
clf = RandomForestClassifier(n_estimators=300, max_depth=20, class_weight="balanced", random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

cv  = cross_val_score(clf, X, y, cv=StratifiedKFold(5), scoring="accuracy")
acc = accuracy_score(y_test, clf.predict(X_test))
print(f"CV Accuracy : {cv.mean():.4f} ± {cv.std():.4f}")
print(f"Test Accuracy: {acc:.4f}")
print(classification_report(y_test, clf.predict(X_test), target_names=le.classes_))

# ── Save ──────────────────────────────────────────────────────────────────────
joblib.dump(clf,   os.path.join(MODEL_DIR, "disease_classifier.pkl"))
joblib.dump(le,    os.path.join(MODEL_DIR, "label_encoder.pkl"))
joblib.dump(SCOLS, os.path.join(MODEL_DIR, "symptom_columns.pkl"))

risk_map = df.drop_duplicates("disease")[["disease","risk_level","risk_score"]]
risk_map.to_json(os.path.join(MODEL_DIR, "risk_map.json"), orient="records")

with open(os.path.join(MODEL_DIR, "symptoms_list.json"),"w") as f:
    json.dump(SCOLS, f, indent=2)

print("✅ All model artifacts saved to backend/models/")