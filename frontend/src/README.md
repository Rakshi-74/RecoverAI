# RecoverAI

## Autonomous Revenue Recovery & Payment Intelligence

RecoverAI is an AI-native revenue recovery platform that detects payment failures, predicts recovery probability, recommends intelligent recovery actions, applies safety guardrails, and maintains an audit trail.

## Problem

Payment failures can cause significant revenue leakage for businesses. Traditional retry systems use fixed rules and often retry payments without considering customer behavior, recovery probability, or safety constraints.

## Solution

RecoverAI uses machine learning and an autonomous decision pipeline to determine the best recovery action for each failed payment.

## Recovery Pipeline

Payment Failure
↓
AI Risk Prediction
↓
Decision Engine
↓
Guardrail Check
↓
Recovery Action
↓
Audit Trail

## Key Features

- ML-based recovery probability prediction
- Intelligent recovery decision engine
- Safety guardrails
- Autonomous recovery action execution
- Revenue-at-risk calculation
- Expected recovery estimation
- Recovery metrics dashboard
- Audit trail for every decision
- FastAPI backend
- React frontend
- SQLite database
- Razorpay payment integration

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Scikit-learn
- Pandas
- NumPy
- React
- Vite
- SQLite

## Live Demo

Add the deployed frontend URL here.

## Backend API

Add the deployed backend URL here.

## Project Structure

```text
RecoverAI/
├── backend/
├── frontend/
├── ml/
├── scripts/
├── ml_dataset.csv
├── recoverai.db
├── requirements.txt
└── README.md
Objective

To build an AI-native revenue recovery system that makes data-driven recovery decisions while balancing recovery probability, expected revenue, customer behavior, and safety constraints.

Author

Kuruva Rakshitha