import { useState, useEffect, useRef } from "react";

const API_BASE = "http://localhost:5000/api";

// ── Mock API response (for demo without backend) ──────────────────────────
const MOCK_RESPONSE = {
  detected_symptoms: ["fever", "severe_headache", "joint_pain", "nausea"],
  triage: {
    risk_level: "high",
    risk_info: {
      label: "High Risk",
      color: "#f97316",
      badge: "orange",
      icon: "🚨",
      action: "Urgent Medical Attention",
    },
    top_prediction: "Dengue Fever",
    predictions: [
      { disease: "Dengue Fever", probability: 0.68, probability_pct: 68, risk_level: "high" },
      { disease: "Malaria", probability: 0.19, probability_pct: 19, risk_level: "high" },
      { disease: "Viral Fever", probability: 0.09, probability_pct: 9, risk_level: "moderate" },
      { disease: "Influenza", probability: 0.03, probability_pct: 3, risk_level: "moderate" },
    ],
    recommendation:
      "Your symptoms indicate a condition requiring prompt medical care. Visit a clinic or urgent care facility today.\n\n💊 Note for Dengue Fever: Avoid aspirin/ibuprofen — use paracetamol only. Watch for warning signs: bleeding, persistent vomiting.",
    disclaimer:
      "⚠️ This AI triage is for informational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.",
  },
};

const RISK_COLORS = {
  low: { bg: "bg-green-500/10", border: "border-green-500/30", text: "text-green-400", dot: "bg-green-400" },
  moderate: { bg: "bg-yellow-500/10", border: "border-yellow-500/30", text: "text-yellow-400", dot: "bg-yellow-400" },
  high: { bg: "bg-orange-500/10", border: "border-orange-500/30", text: "text-orange-400", dot: "bg-orange-400" },
  urgent: { bg: "bg-red-500/10", border: "border-red-500/30", text: "text-red-400", dot: "bg-red-400" },
};

const SYMPTOM_CHIPS = [
  "Fever", "Headache", "Nausea", "Vomiting", "Fatigue", "Cough",
  "Sore throat", "Body ache", "Diarrhea", "Shortness of breath",
  "Chest pain", "Dizziness", "Rash", "Chills", "Joint pain",
];

function ProbBar({ disease, probability_pct, risk_level }) {
  const colors = RISK_COLORS[risk_level] || RISK_COLORS.moderate;
  return (
    <div className="mb-3">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm text-gray-300 font-medium">{disease}</span>
        <span className={`text-sm font-bold ${colors.text}`}>{probability_pct}%</span>
      </div>
      <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${colors.dot}`}
          style={{ width: `${probability_pct}%` }}
        />
      </div>
    </div>
  );
}

function SymptomChip({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-all duration-200 ${
        active
          ? "bg-cyan-500/20 border-cyan-500/50 text-cyan-300"
          : "bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-300"
      }`}
    >
      {label}
    </button>
  );
}

export default function App() {
  const [text, setText] = useState("");
  const [duration, setDuration] = useState("");
  const [activeChips, setActiveChips] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [useMock, setUseMock] = useState(false);
  const resultRef = useRef(null);

  const toggleChip = (chip) => {
    setActiveChips((prev) =>
      prev.includes(chip) ? prev.filter((c) => c !== chip) : [...prev, chip]
    );
  };

  // Sync chips to textarea
  useEffect(() => {
    if (activeChips.length > 0) {
      setText(activeChips.join(", "));
    }
  }, [activeChips]);

  const handleSubmit = async () => {
    if (!text.trim() && activeChips.length === 0) return;
    setLoading(true);
    setError(null);
    setResult(null);

    if (useMock) {
      await new Promise((r) => setTimeout(r, 1400));
      setResult(MOCK_RESPONSE);
      setLoading(false);
      return;
    }

    try {
      const payload = {
        text: text.trim(),
        duration_days: duration ? parseInt(duration) : null,
      };
      const res = await fetch(`${API_BASE}/triage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Server error");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [result]);

  const risk = result?.triage?.risk_level;
  const riskColors = risk ? RISK_COLORS[risk] : null;

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100" style={{ fontFamily: "'Outfit', sans-serif" }}>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-950/90 backdrop-blur sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-lg">
              🩺
            </div>
            <div>
              <div className="font-bold text-white leading-none">MedTriage AI</div>
              <div className="text-xs text-gray-500 leading-none mt-0.5">Symptom Analysis Platform</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer">
              <input
                type="checkbox"
                checked={useMock}
                onChange={(e) => setUseMock(e.target.checked)}
                className="w-3.5 h-3.5"
              />
              Demo mode
            </label>
            <span className="px-2.5 py-1 bg-green-500/10 border border-green-500/30 text-green-400 text-xs rounded-full font-medium">
              ● Live
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Hero */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-white mb-3">
            AI-Powered{" "}
            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              Symptom Triage
            </span>
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto">
            Describe your symptoms in natural language. Our ML model analyzes patterns and provides risk-stratified triage recommendations.
          </p>
        </div>

        {/* Input Card */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-6">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Describe Your Symptoms</h2>

          {/* Quick chips */}
          <div className="flex flex-wrap gap-2 mb-4">
            {SYMPTOM_CHIPS.map((chip) => (
              <SymptomChip
                key={chip}
                label={chip}
                active={activeChips.includes(chip)}
                onClick={() => toggleChip(chip)}
              />
            ))}
          </div>

          {/* Textarea */}
          <textarea
            value={text}
            onChange={(e) => { setText(e.target.value); setActiveChips([]); }}
            placeholder="e.g. I have had fever, severe headache, joint pain and nausea for the past 2 days..."
            className="w-full bg-gray-800 border border-gray-700 rounded-xl p-4 text-gray-100 placeholder-gray-600 resize-none focus:outline-none focus:border-cyan-500/50 transition-colors"
            rows={4}
            style={{ fontFamily: "'Outfit', sans-serif" }}
          />

          {/* Duration + Submit */}
          <div className="flex items-center gap-4 mt-4">
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-400">Duration:</label>
              <input
                type="number"
                min="1"
                max="365"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                placeholder="Days"
                className="w-24 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-100 focus:outline-none focus:border-cyan-500/50"
              />
            </div>
            <button
              onClick={handleSubmit}
              disabled={loading || (!text.trim() && activeChips.length === 0)}
              className="ml-auto px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-xl disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity flex items-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>Analyze Symptoms →</>
              )}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-4 mb-6 text-sm">
            ❌ {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div ref={resultRef} className="space-y-4 animate-fadeIn">
            {/* Risk Banner */}
            <div className={`rounded-2xl p-5 border ${riskColors.bg} ${riskColors.border}`}>
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-white flex items-center gap-2">
                    <span>{result.triage.risk_info.icon}</span>
                    <span>{result.triage.risk_info.label}</span>
                  </div>
                  <div className={`text-sm font-medium mt-1 ${riskColors.text}`}>
                    Action: {result.triage.risk_info.action}
                  </div>
                </div>
                <div className={`text-right`}>
                  <div className="text-sm text-gray-400">Top Diagnosis</div>
                  <div className="text-lg font-bold text-white">{result.triage.top_prediction}</div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Predictions */}
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
                <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                  Possible Conditions
                </h3>
                {result.triage.predictions.map((p) => (
                  <ProbBar key={p.disease} {...p} />
                ))}
              </div>

              {/* Detected Symptoms */}
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
                <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                  Detected Symptoms ({result.detected_symptoms?.length || 0})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {(result.detected_symptoms || []).map((s) => (
                    <span key={s} className="px-3 py-1.5 bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-sm rounded-full">
                      {s.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Recommendation */}
            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Clinical Recommendation
              </h3>
              {result.triage.recommendation.split("\n\n").map((para, i) => (
                <p key={i} className="text-gray-300 text-sm leading-relaxed mb-2">{para}</p>
              ))}
            </div>

            {/* Disclaimer */}
            <p className="text-xs text-gray-600 text-center px-4">{result.triage.disclaimer}</p>
          </div>
        )}
      </main>

      <style>{`
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fadeIn { animation: fadeIn 0.4s ease-out; }
      `}</style>
    </div>
  );
}
