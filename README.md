# 🧠 BizMind AI - Autonomous Business Intelligence Platform

[![Build & Test Status](https://img.shields.io/badge/Tests-30%20Passed-brightgreen)](https://github.com/rohitxai999/BizMind-AI)
[![Milestone](https://img.shields.io/badge/Milestone-Day%2015%20of%2044-blue)](https://github.com/rohitxai999/BizMind-AI)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.139-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://python.org)

**BizMind AI** is a production-ready, portfolio-quality AI business intelligence and autonomous decision support platform designed to turn raw business KPIs into actionable executive intelligence, risk evaluations, and simulated strategic pathways.

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
- **Day 15 (Current Milestone)**:
  - **Business Scenario Simulator**: What-if simulation, sensitivity analysis, pre-packaged industry stress tests, and multi-scenario comparison.
  - **Centralized Configuration & Structured Logging**: Pydantic-based configuration management (`app.core.config`) and centralized logging (`app.core.logging`).
  - **Clean Versioned API Architecture**: Standardized `/api/v1` structure with CORS support and robust error handling.
  - **Standalone Risk Engine API**: Dedicated endpoint for direct risk calculation.
  - **Expanded Test Suite**: 30 comprehensive automated tests covering all engines and APIs.

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

    SimEngine --> RiskEngine
    InsightsEngine --> RiskEngine
    InsightsEngine --> DecisionEngine
    InsightsEngine --> OppEngine
    InsightsEngine --> ExecEngine
```

---

## 🌟 Key Features (Day 15)

### 1. Business Scenario Simulator (`app.services.simulator.engine`)
- **What-If Simulations**: Quantify impact on revenue, expenses, headcount, customer volume, profit margins, and health score.
- **Risk Trajectory Modeling**: Evaluates how simulated levers alter business risk scores (0–100) using the centralized `RiskEngine`.
- **Pre-packaged Stress Tests**:
  - *Recession Stress Test* (-20% revenue, +5% expenses)
  - *Aggressive Expansion* (+25% revenue, +18% expenses, +3 staff)
  - *Cost Optimization* (-15% expenses)
  - *Pricing Power & Margin Expansion* (+10% revenue, 0% expenses)
  - *Severe Supply / Cost Shock* (-10% revenue, +15% expenses)
- **Multi-Scenario Comparison**: Benchmarks scenarios side-by-side to recommend the optimal strategic path that balances net profit against downside risk.

### 2. Centralized Configuration & Structured Logging (`app.core`)
- Centralized settings managed with `pydantic-settings` reading from `.env` or system environment.
- Configurable CORS origins, environment modes (`development`, `production`), and logging levels.
- Unified structured logger for tracing engine operations.

### 3. Versioned REST API (`/api/v1`)
Full separation of concerns with clean schemas, strong typing, and input validation:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Health check & AI/BI engines readiness status |
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
All **30 tests** will run and validate the multi-agent system, engines, and API endpoints.

### 4. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📋 Recommended Day 16 Objective
- **Predictive Analytics & Forecasting Engine**: Introduce time-series revenue and expense forecasting (Holt-Winters / ARIMA / Prophet foundation) integrated into the executive dashboard.
- **Database Persistence**: Integrate SQLAlchemy / PostgreSQL repository layer for scenario save/history and executive audit logs.
