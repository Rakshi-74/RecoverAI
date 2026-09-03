import { useEffect, useState } from "react";
import "./App.css";

// RecoverAI production backend
const API = "https://recoverai-zzx4.onrender.com";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  const [paymentId, setPaymentId] = useState("DEMO_FRONTEND_001");
  const [amount, setAmount] = useState(5000);

  const [recoveryResult, setRecoveryResult] = useState(null);
  const [testing, setTesting] = useState(false);
  const [error, setError] = useState("");

  // Load dashboard metrics
  const loadMetrics = async () => {
    try {
      setError("");

      const response = await fetch(`${API}/api/metrics`);

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      setMetrics(data);
    } catch (err) {
      console.error("Failed to load metrics:", err);

      setError(
        "Unable to connect to RecoverAI backend. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  // Test AI recovery
  const testRecovery = async () => {
    setTesting(true);
    setError("");
    setRecoveryResult(null);

    const paymentData = {
      payment_id: paymentId,
      amount: Number(amount),
      attempt_number: 1,
      checkout_started: 1,
      checkout_duration_seconds: 60,
      customer_age_days: 30,
      lifetime_value: Number(amount),
      successful_payments: 5,
      failed_payments: 1,
      previous_recoveries: 1,
      contact_opted_out: 0,
      failure_rate: 0.16,
      recovery_history_rate: 0.5,
      high_value_customer: Number(amount) >= 5000 ? 1 : 0,
      high_amount: Number(amount) >= 5000 ? 1 : 0,
      multiple_attempt: 0
    };

    try {
      const response = await fetch(`${API}/api/recover`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(paymentData)
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      if (data.status === "ERROR") {
        throw new Error(data.error || "Recovery API returned an error");
      }

      setRecoveryResult(data);

      // Refresh dashboard metrics
      await loadMetrics();
    } catch (err) {
      console.error("Recovery test failed:", err);

      setError(
        "Recovery request failed. Please check the RecoverAI backend."
      );
    } finally {
      setTesting(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  // Loading screen
  if (loading) {
    return (
      <div className="loading">
        Loading RecoverAI...
      </div>
    );
  }

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>RecoverAI</h1>

          <p>
            Autonomous Revenue Recovery & Payment Intelligence
          </p>
        </div>

        <div className="status">
          <span className="dot"></span>
          System Online
        </div>
      </header>

      <main>

        {/* HERO */}
        <section className="hero">
          <div>
            <h2>
              Revenue Recovery Command Center
            </h2>

            <p>
              AI-driven detection, decisioning, guardrails
              and recovery execution.
            </p>
          </div>

          <button onClick={loadMetrics}>
            Refresh Metrics
          </button>
        </section>

        {/* ERROR */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* METRIC CARDS */}
        <section className="cards">

          <div className="card">
            <span>Total Payments</span>

            <strong>
              {metrics?.total_payments ?? 0}
            </strong>
          </div>

          <div className="card">
            <span>Revenue at Risk</span>

            <strong>
              ₹{Number(
                metrics?.revenue_at_risk ?? 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="card">
            <span>Expected Recovery</span>

            <strong>
              ₹{Number(
                metrics?.expected_recovery ?? 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="card">
            <span>Recovery Rate</span>

            <strong>
              {metrics?.expected_recovery_rate ?? 0}%
            </strong>
          </div>

        </section>

        {/* PERFORMANCE + PIPELINE */}
        <section className="grid">

          {/* AGENT PERFORMANCE */}
          <div className="panel">

            <h3>
              Agent Performance
            </h3>

            <div className="metric-row">
              <span>
                Approved Actions
              </span>

              <b>
                {metrics?.approved_actions ?? 0}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Blocked Actions
              </span>

              <b>
                {metrics?.blocked_actions ?? 0}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Actual Recovered
              </span>

              <b>
                ₹{Number(
                  metrics?.actual_recovered ?? 0
                ).toLocaleString()}
              </b>
            </div>

          </div>

          {/* RECOVERY PIPELINE */}
          <div className="panel">

            <h3>
              Recovery Pipeline
            </h3>

            <div className="pipeline">

              <div>
                01 <span>Payment Failure</span>
              </div>

              <div>
                02 <span>AI Risk Prediction</span>
              </div>

              <div>
                03 <span>Decision Engine</span>
              </div>

              <div>
                04 <span>Guardrail Check</span>
              </div>

              <div>
                05 <span>Recovery Action</span>
              </div>

            </div>

          </div>

        </section>

        {/* TEST RECOVERY */}
        <section className="panel">

          <h3>
            Test Recovery Agent
          </h3>

          <div className="metric-row">

            <span>
              Payment ID
            </span>

            <input
              value={paymentId}
              onChange={(e) =>
                setPaymentId(e.target.value)
              }
              placeholder="Enter payment ID"
            />

          </div>

          <div className="metric-row">

            <span>
              Payment Amount
            </span>

            <input
              type="number"
              min="1"
              value={amount}
              onChange={(e) =>
                setAmount(e.target.value)
              }
              placeholder="Enter amount"
            />

          </div>

          <button
            onClick={testRecovery}
            disabled={testing}
          >
            {testing
              ? "Running AI Recovery..."
              : "Run Recovery Test"}
          </button>

        </section>

        {/* AI RESULT */}
        {recoveryResult && (
          <section className="panel">

            <h3>
              AI Recovery Decision
            </h3>

            <div className="metric-row">
              <span>
                Payment ID
              </span>

              <b>
                {recoveryResult.payment_id ?? "-"}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Recovery Probability
              </span>

              <b>
                {typeof recoveryResult.recovery_probability === "number"
                  ? (
                      recoveryResult.recovery_probability * 100
                    ).toFixed(2)
                  : "0.00"}
                %
              </b>
            </div>

            <div className="metric-row">
              <span>
                Recommended Action
              </span>

              <b>
                {recoveryResult.recommended_action ?? "-"}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Final Action
              </span>

              <b>
                {recoveryResult.final_action ?? "-"}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Decision Status
              </span>

              <b>
                {recoveryResult.status ?? "-"}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Execution Status
              </span>

              <b>
                {recoveryResult.execution?.status ?? "-"}
              </b>
            </div>

            <div className="metric-row">
              <span>
                Expected Recovery Value
              </span>

              <b>
                ₹{Number(
                  recoveryResult.expected_recovery_value ?? 0
                ).toLocaleString()}
              </b>
            </div>

          </section>
        )}

        {/* FOOTER */}
        <section className="footer-panel">

          <h3>
            RecoverAI Intelligence
          </h3>

          <p>
            Every recovery decision is evaluated by ML,
            checked against safety guardrails and recorded
            through an audit trail.
          </p>

        </section>

      </main>

    </div>
  );
}

export default App;