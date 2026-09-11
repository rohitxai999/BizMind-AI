# 🧠 BizMind AI - Autonomous Business Intelligence Platform

[![Build & Test Status](https://img.shields.io/badge/Tests-38%20Passed-brightgreen)](https://github.com/rohitxai999/BizMind-AI)
[![Milestone](https://img.shields.io/badge/Milestone-Day%2016%20of%2044-blue)](https://github.com/rohitxai999/BizMind-AI)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.139-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://python.org)

**BizMind AI** is a production-ready, portfolio-quality AI business intelligence and autonomous decision support platform designed to turn raw business KPIs into actionable executive intelligence, predictive forecasts, risk evaluations, and simulated strategic pathways.

---

## 🚀 Development Roadmap & Current Milestone

BizMind AI is an intensive 44-day build towards an enterprise-ready autonomous business intelligence copilot.

- **Day 1–5**: Initial architecture, multi-agent foundational prototypes, KPI engine, CSV uploads, and Streamlit executive dashboard.
- **Day 6–9**: FastAPI integration, agent managers, health endpoints, executive dashboard analytics, and monthly trend tracking.
- **Day 10**: Executive Dashboard API and AI Business Insights Engine.
- **Day 11**: Unified Business Assessment Engine combining multi-agent outputs and KPI signals.
- **Day 12**: Explainable Decision Engine and Opportunity Discovery Engine with evidence cards.
- **Day 13**: Executive Intelligence Engine and prioritized strategic action synthesis.
- **Day 14**: Centralized Business Risk Engine for standardized, explainable risk scoring (0-100).
- **Day 15**: Business Scenario Simulator (what-if analysis, pre-packaged stress tests, multi-scenario comparison), clean versioned API (`/api/v1`), and centralized configuration/logging.
- **Day 16 (Current Milestone)**:
  - **Predictive Analytics & Forecasting Engine**: Time-series statistical trend extrapolation, exponential trend fitting, prediction confidence bands, historical anomaly detection, and forward risk trajectory evaluation via `RiskEngine`.
  - **Forecast API Endpoints**: Dedicated `/api/v1/forecast/predict` and `/api/v1/forecast/sample` endpoints.
  - **Comprehensive Test Suite**: Expanded to **38 automated tests** covering all AI/BI engines, forecasting models, and API routes.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    Client[Web UI / Streamlit / API Client] --> FastAPI[FastAPI Backend Application]
    
    FastAPI --> V1Router[/api/v1 Router]
    FastAPI --> LegacyRouter[Legacy Compatible Routes]

    subgraph "AI & Business Intelligence Engines"
        V1Router --> RiskEngine[Risk Engine (Day 14)]
        V1Router --> SimEngine[Scenario Simulator Engine (Day 15)]
        V1Router --> ForecastEngine[Predictive Analytics & Forecasting (Day 16)]
        V1Router --> DecisionEngine[Decision Engine (Day 12)]
        V1Router --> OppEngine[Opportunity Engine (Day 12)]
        V1Router --> ExecEngine[Executive Intelligence Engine (Day 13)]
        V1Router --> InsightsEngine[Insights Engine (Day 10-14)]
        V1Router --> AgentManager[Multi-Agent System]
    end

    subgraph "Multi-Agent System"
        AgentManager --> FinanceAgent[Finance Agent]
        AgentManager --> SalesAgent[Sales Agent]
        AgentManager --> MarketingAgent[Marketing Agent]
        AgentManager --> RiskAgent[Risk Agent]
    end

    ForecastEngine --> RiskEngine
    SimEngine --> RiskEngine
    InsightsEngine --> RiskEngine
    InsightsEngine --> DecisionEngine
    InsightsEngine --> OppEngine
    InsightsEngine --> ExecEngine
```

---

## 🌟 Key Capabilities

### 1. Predictive Analytics & Forecasting Engine (`app.services.forecast.engine`) - *New in Day 16*
- **Time-Series Extrapolation**: Multi-period forward forecasting for top-line revenue and operational expenses.
- **Dynamic Prediction Bands**: Statistical confidence intervals (80%, 90%, 95%) modeling uncertainty growth across future forecast horizons.
- **Forward Risk Projection**: Evaluates projected future financials through the centralized `RiskEngine` to predict future risk scores, levels, and trajectories (*Improving*, *Deteriorating*, or *Stable*).
- **Historical Anomaly Detection**: Scans time-series data using Z-score outlier detection ($|z| \ge 2.0$) to highlight anomalous periods.
- **Annual Run-Rate & Momentum Analysis**: Evaluates revenue momentum direction, expense expansion pacing, and coefficient of variation volatility scores.

### 2. Business Scenario Simulator (`app.services.simulator.engine`) - *Day 15*
- **What-If Simulations**: Quantify impact on revenue, expenses, headcount, customer volume, profit margins, and health score.
- **Risk Trajectory Modeling**: Evaluates how simulated levers alter business risk scores (0–100) using the centralized `RiskEngine`.
- **Pre-packaged Stress Tests**: *Recession Stress Test*, *Aggressive Expansion*, *Cost Optimization*, *Pricing Power*, and *Severe Supply/Cost Shock*.
- **Multi-Scenario Comparison**: Benchmarks scenarios side-by-side to recommend the optimal strategic path.

### 3. Centralized Risk Engine (`app.services.risk.engine`) - *Day 14*
- Standardized, explainable risk scoring (0–100) and risk level assignment (*Low*, *Medium*, *High*, *Critical*).
- Evaluates profit margin, expense ratio, and growth momentum with explicit factor drivers.

### 4. Versioned REST API (`/api/v1`)
Full separation of concerns with clean schemas, strong typing, and input validation:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Health check & AI/BI engines readiness status |
| `POST` | `/api/v1/forecast/predict` | Generate time-series forecasts with confidence bands and future risk |
| `POST` | `/api/v1/forecast/sample` | Generate benchmark sample forecast |
| `POST` | `/api/v1/risk/calculate` | Direct risk score, level, and driver calculation |
| `POST` | `/api/v1/scenarios/simulate` | Run custom what-if scenario simulation |
| `POST` | `/api/v1/scenarios/compare` | Compare multiple scenarios side-by-side |
| `POST` | `/api/v1/scenarios/stress-test` | Run recession and cost-shock stress tests |
| `GET` | `/api/v1/scenarios/presets` | List pre-configured scenario presets |
| `POST` | `/api/v1/decisions/analyze` | Generate explainable decision evidence cards |
| `POST` | `/api/v1/opportunities/analyze`| Discover growth and value creation opportunities |
| `GET` | `/api/v1/dashboard/executive-summary` | Unified executive dashboard intelligence |

*(Legacy endpoints `/`, `/health`, `/analysis`, `/upload`, and `/dashboard/summary` remain fully backward-compatible).*

---

## 🛠️ Installation & Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/rohitxai999/BizMind-AI.git
cd BizMind-AI
```

### 2. Configure Environment
```bash
cp .env.example .env
```

### 3. Run Automated Tests
```bash
cd backend
python -m pytest tests -v
```
All **38 tests** will run and validate the multi-agent system, predictive analytics engine, scenario simulator, and API endpoints.

### 4. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📋 Recommended Day 17 Objective
- **AI Business Copilot Service (`CopilotEngine`)**: Interactive conversational business assistant capable of querying multi-agent outputs, scenario simulations, and forecasts with natural language reasoning.
- **Database Persistence**: Integrate SQLAlchemy / SQLite / PostgreSQL repository layer to persist simulation runs, forecast snapshots, and executive audit logs.
