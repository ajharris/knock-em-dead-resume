
import JobPreferencesForm from "./JobPreferencesForm";
import KeywordStep from "./KeywordStep";

const steps = [
  "Job Preferences",
  "Experience Summary",
  "Keywords",
  "Key Strengths",
  "Education",
  // ...add more steps as you implement
];

export default function Stepper() {
  const [step, setStep] = useState(0);
  // For demo, use a static userId. In production, get from auth/session.
  const userId = 1;

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2 style={{ textAlign: "center" }}>Knock 'Em Dead Resume Builder</h2>
      <div style={{ display: "flex", justifyContent: "center", margin: "1.5rem 0" }}>
        {steps.map((label, idx) => (
          <div key={label} style={{
            padding: "0.5rem 1rem",
            background: idx === step ? "#007bff" : "#eee",
            color: idx === step ? "#fff" : "#333",
            borderRadius: 4,
            marginRight: idx < steps.length - 1 ? 8 : 0,
            fontWeight: idx === step ? "bold" : "normal"
          }}>{label}</div>
        ))}
      </div>
      <div style={{ minHeight: 200 }}>
        {step === 0 && <JobPreferencesForm userId={userId} onComplete={() => setStep(s => s + 1)} />}
        {step === 1 && <div>Experience Summary form goes here</div>}
        {step === 2 && (
          <KeywordStep
            jobAdId={1} // TODO: Replace with real jobAdId
            jobDescription={"We are seeking a Data Analyst with experience in Python, SQL, and data visualization. Must have strong communication skills and experience with Tableau or Power BI. Familiarity with cloud platforms like AWS is a plus."}
            onKeywordsChange={keywords => {}}
          />
        )}
        {step === 3 && <div>Key Strengths form goes here</div>}
        {step === 4 && <div>Education form goes here</div>}
        {/* Add more forms as needed */}
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24 }}>
        <button onClick={() => setStep(s => Math.max(0, s - 1))} disabled={step === 0}>
          Back
        </button>
        <button onClick={() => setStep(s => Math.min(steps.length - 1, s + 1))} disabled={step === steps.length - 1}>
          Next
        </button>
      </div>
    </div>
  );
}
