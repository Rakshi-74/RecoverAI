import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./recoverai.db"

engine = create_engine(DATABASE_URL)

query = """
SELECT
    p.payment_id,
    p.amount,
    p.payment_method,
    p.status,
    p.failure_reason,
    p.attempt_number,
    p.checkout_started,
    p.checkout_duration_seconds,

    c.customer_age_days,
    c.lifetime_value,
    c.successful_payments,
    c.failed_payments,
    c.previous_recoveries,
    c.contact_opted_out

FROM payments p
JOIN customers c
ON p.customer_id = c.customer_id

WHERE p.status = 'failed'
"""

df = pd.read_sql(query, engine)

df["failure_rate"] = (
    df["failed_payments"]
    / (df["successful_payments"] + df["failed_payments"] + 1)
)

df["recovery_history_rate"] = (
    df["previous_recoveries"]
    / (df["failed_payments"] + 1)
)

df["high_value_customer"] = (
    df["lifetime_value"] >= df["lifetime_value"].median()
).astype(int)

df["high_amount"] = (
    df["amount"] >= df["amount"].median()
).astype(int)

df["multiple_attempt"] = (
    df["attempt_number"] > 1
).astype(int)

score = (
    0.30 * df["recovery_history_rate"].clip(0, 1)
    + 0.20 * (1 - df["failure_rate"])
    + 0.15 * df["high_value_customer"]
    + 0.10 * (1 - df["contact_opted_out"])
    + 0.10 * (df["checkout_started"] == 1)
    + 0.10 * (df["attempt_number"] <= 2)
    + 0.05 * (df["amount"] < df["amount"].median())
)

df["recovery_success"] = (
    score >= score.median()
).astype(int)

output_columns = [
    "payment_id",
    "amount",
    "attempt_number",
    "checkout_started",
    "checkout_duration_seconds",
    "customer_age_days",
    "lifetime_value",
    "successful_payments",
    "failed_payments",
    "previous_recoveries",
    "contact_opted_out",
    "failure_rate",
    "recovery_history_rate",
    "high_value_customer",
    "high_amount",
    "multiple_attempt",
    "recovery_success"
]

dataset = df[output_columns]

dataset.to_csv("ml_dataset.csv", index=False)

print("ML dataset created successfully!")
print(f"Rows: {len(dataset)}")
print(f"Columns: {len(dataset.columns)}")

print("\nTarget distribution:")
print(dataset["recovery_success"].value_counts())