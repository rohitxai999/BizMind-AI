# 🧠 BizMind AI - Autonomous Business Intelligence Platform

[![Build & Test Status](https://img.shields.io/badge/Tests-58%20Passed-brightgreen)](https://github.com/rohitxai999/BizMind-AI)
[![Milestone](https://img.shields.io/badge/Milestone-Day%2018%20of%2044-blue)](https://github.com/rohitxai999/BizMind-AI)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.139-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://python.org)

**BizMind AI** is a production-ready, portfolio-quality AI business intelligence and autonomous decision support platform designed to turn raw business KPIs into actionable executive intelligence, predictive forecasts, risk evaluations, simulated strategic pathways, and multi-agent collaborative consensus.

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
- **Day 16**: Predictive Analytics & Forecasting Engine (time-series trend extrapolation, prediction confidence intervals, anomaly detection, forward risk projections via `RiskEngine`).
- **Day 17**: Explainable Risk Findings Engine with evidence-based explanations, severity classifications, mitigation recommendations, and strict input validation.
- **Day 18 (Current Milestone)**:
  - **Autonomous Business Copilot (`CopilotEngine`)**: Interactive conversational intelligence engine equipped with multi-intent classification (`SCENARIO_SIMULATION`, `FORECAST_INQUIRY`, `RISK_ANALYSIS`, `STRATEGIC_PLANNING`, `PERFORMANCE_DIAGNOSIS`), automatic tool routing across analytical engines, executive briefings, and data evidence citations.
  - **Collaborative Multi-Agent Orchestrator (`MultiAgentOrchestrator`)**: Cross-domain synthesis across Finance, Sales, Marketing, Risk & Compliance, and Operations & Strategy agents with cross-agent consensus scoring, strategic tension detection, and trade-off debate resolutions.
  - **Explainable AI Recommendations Engine**: Structured, evidence-backed recommendations featuring quantitative ROI estimates, risk reduction potential, execution feasibility scoring, and time-phased implementation roadmaps.
  - **Persistent SQLite Audit Repository (`CopilotAuditRepository`)**: Session-aware audit logging tracking all queries, analytical intents, summaries, and tool invocations.
  - **Versioned API Endpoints (`/api/v1/copilot` and `/api/v1/agents`)**: Dedicated endpoints for conversational queries, multi-agent synthesis, interaction history management, and agent collaboration.
  - **Interactive Streamlit Copilot UI (`frontend/pages/copilot.py`)**: Full-featured executive UI with prompt chips, real-time tool inspection, consensus gauges, debate visualization, and recommendation cards.
  - **Comprehensive Test Suite**: Expanded to **58 automated tests** covering all AI/BI engines, multi-agent orchestration, audit persistence, and API endpoints.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    Client[Web UI / Streamlit / API Client] --> FastAPI[FastAPI Backend Application]
    
    FastAPI --> V1Router[/api/v1 Router]
    FastAPI --> LegacyRouter[Legacy Compatible Routes]

    subgraph "AI & Business Intelligence Engines"
        V1Router --> CopilotEngine[Autonomous Business Copilot (Day 18)]
        V1Router --> MultiAgentOrchestrator[Multi-Agent Orchestrator (Day 18)]
        V1Router --> RiskEngine[Risk Engine (Day 14 & 17)]
        V1Router --> SimEngine[Scenario Simulator Engine (Day 15)]
        V1Router --> ForecastEngine[Predictive Analytics & Forecasting (Day 16)]
        V1Router --> DecisionEngine[Decision Engine (Day 12)]
        V1Router --> OppEngine[Opportunity Engine (Day 12)]
        V1Router --> ExecEngine[Executive Intelligence Engine (Day 13)]
        V1Router --> InsightsEngine[Insights Engine (Day 10-14)]
    end

    subgraph "Persistence & Audit Layer"
        CopilotEngine --> CopilotAuditRepo[(SQLite Audit Repository)]
    end

    subgraph "Collaborative Multi-Agent System"
        MultiAgentOrchestrator --> FinAgent[Finance Intelligence Agent]
        MultiAgentOrchestrator --> SalesAgent[Sales Intelligence Agent]
        MultiAgentOrchestrator --> MktAgent[Marketing Intelligence Agent]
        MultiAgentOrchestrator --> RiskAgent[Risk & Compliance Agent]
        MultiAgentOrchestrator --> OpsAgent[Operations & Strategy Agent]
    end

    CopilotEngine --> MultiAgentOrchestrator
    CopilotEngine --> RiskEngine
    CopilotEngine --> ForecastEngine
    CopilotEngine --> SimEngine
    CopilotEngine --> InsightsEngine
    MultiAgentOrchestrator --> RiskEngine
    ForecastEngine --> RiskEngine
    SimEngine --> RiskEngine
    InsightsEngine --> RiskEngine
```

---

## 🌟 Key Capabilities

### 1. Autonomous Business Copilot (`app.services.copilot.engine`) - *New in Day 18*
- **Intent-Driven Routing**: Classifies leadership inquiries into 5 core intents (`SCENARIO_SIMULATION`, `FORECAST_INQUIRY`, `RISK_ANALYSIS`, `STRATEGIC_PLANNING`, `PERFORMANCE_DIAGNOSIS`).
- **Dynamic Tool Invocation**: Automatically dispatches and queries underlying analytical engines (`RiskEngine`, `ForecastEngine`, `ScenarioSimulatorEngine`, `InsightsEngine`, `MultiAgentOrchestrator`).
- **Natural Language Executive Synthesis**: Grounded answers supported by exact computed evidence metrics and follow-up guidance.
- **Audit Persistence**: Tracks and logs all user interactions into a persistent SQLite repository with session continuity.

### 2. Multi-Agent Orchestrator & Consensus Engine (`app.services.copilot.orchestrator`) - *New in Day 18*
- **Specialized Domain Intelligence**: Deploys 5 domain agents (Finance, Sales, Marketing, Risk, Operations) with distinct analytical metrics, sentiments, and priority scores.
- **Cross-Agent Consensus Debate**: Detects friction points (e.g. Growth vs Capital Preservation, Volume Discounting vs Margin Expansion), assesses alignment scores (0-100%), and formulates resolved executive compromises.
- **Explainable Recommendations**: Delivers structured action plans with evidence metrics, quantitative ROI projections, risk reduction points, and feasibility scores.

### 3. Predictive Analytics & Forecasting Engine (`app.services.forecast.engine`) - *Day 16*
- **Time-Series Extrapolation**: Multi-period forward forecasting for top-line revenue and operational expenses.
- **Dynamic Prediction Bands**: Statistical confidence intervals (80%, 90%, 95%) modeling uncertainty growth across future horizons.
- **Forward Risk Projection**: Evaluates projected financials through the centralized `RiskEngine` to predict future risk trajectories.

### 4. Business Scenario Simulator (`app.services.simulator.engine`) - *Day 15*
- **What-If Simulations**: Quantify impact on revenue, expenses, headcount, customer volume, profit margins, and health score.
- **Risk Trajectory Modeling**: Evaluates how simulated levers alter business risk scores (0–100) using the centralized `RiskEngine`.
- **Pre-packaged Stress Tests**: *Recession Stress Test*, *Aggressive Expansion*, *Cost Optimization*, *Pricing Power*, and *Severe Supply/Cost Shock*.

### 5. Centralized Risk Engine (`app.services.risk.engine`) - *Day 14 & 17*
- Standardized, explainable risk scoring (0–100) and risk level assignment (*Low*, *Medium*, *High*, *Critical*).
- Evidence-based findings with observed values, severity levels, and actionable mitigation recommendations.

---

## 🌐 Versioned REST API (`/api/v1`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Platform health & all AI/BI engines readiness status |
| `POST` | `/api/v1/copilot/query` | Natural language business queries with multi-engine routing |
| `POST` | `/api/v1/copilot/synthesize` | Multi-agent consensus debate & explainable strategic roadmap |
| `GET` | `/api/v1/copilot/history` | Retrieve interaction audit trail from SQLite persistence |
| `DELETE` | `/api/v1/copilot/history` | Clear session or complete copilot interaction history |
| `POST` | `/api/v1/agents/collaborate` | Cross-domain multi-agent collaborative assessment |
| `GET` | `/api/v1/agents/list` | List registered domain agents and their analytical scopes |
| `POST` | `/api/v1/forecast/predict` | Generate time-series forecasts with confidence bands and future risk |
| `POST` | `/api/v1/forecast/sample` | Generate benchmark sample forecast |
| `POST` | `/api/v1/risk/calculate` | Direct risk score, level, findings, and driver calculation |
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
All **58 tests** will run and validate the multi-agent system, copilot engine, audit repository, scenario simulator, predictive forecasting, and API endpoints.

### 4. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Start the Streamlit Executive Frontend
```bash
streamlit run frontend/streamlit_app.py
```
Access the **Business Copilot** directly via the multi-page sidebar navigation (`pages/copilot.py`).

---

## 📋 Recommended Day 19 Objective
- **Automated Executive Report Generator (`ExecutiveReportingEngine`)**: Export publication-grade PDF and Markdown business intelligence briefings combining multi-agent consensus, scenario simulation comparisons, forward predictive risk trajectories, and audit trails.
- **Enterprise RBAC & Multi-Tenant Organization Support**: Role-based access control (Admin, Executive, Analyst) for simulation management and copilot query audits.
