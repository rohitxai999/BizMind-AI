import os
import sys
from pathlib import Path
import requests
import streamlit as st

# Add backend to path for local fallback if API server is not running
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

try:
    from app.schemas.copilot import CopilotQueryRequest, MultiAgentSynthesisRequest
    from app.services.copilot.engine import CopilotEngine
    from app.services.copilot.orchestrator import MultiAgentOrchestrator
    LOCAL_ENGINE_AVAILABLE = True
except Exception:
    LOCAL_ENGINE_AVAILABLE = False


st.set_page_config(
    page_title="BizMind AI - Business Copilot",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {font-size:36px; font-weight:800; color:#2563eb; margin-bottom:5px;}
    .subtitle {font-size:16px; color:#6b7280; margin-bottom:20px;}
    .badge {display:inline-block; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:600;}
    .badge-bullish {background:#dcfce7; color:#166534;}
    .badge-cautious {background:#fef9c3; color:#854d0e;}
    .badge-critical {background:#fee2e2; color:#991b1b;}
    .card {background:#ffffff; border-radius:12px; padding:18px; border:1px solid #e5e7eb; margin-bottom:15px; box-shadow:0 2px 6px rgba(0,0,0,0.04);}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🤖 BizMind AI Business Copilot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Autonomous Multi-Agent Business Intelligence, Scenario Reasoning & Strategic Consensus</div>',
    unsafe_allow_html=True,
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")


def check_api_health():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=1.5)
        return r.status_code == 200
    except Exception:
        return False


api_online = check_api_health()

with st.sidebar:
    st.title("⚙️ Business Context")
    if api_online:
        st.success("🟢 API Engine Connected")
    else:
        st.warning("🟡 Direct Service Mode (Local Engine)")

    st.subheader("Current Performance KPIs")
    revenue = st.number_input("Revenue ($)", min_value=0.0, value=250000.0, step=5000.0)
    expenses = st.number_input("Expenses ($)", min_value=0.0, value=170000.0, step=5000.0)
    customers = st.number_input("Customers", min_value=0, value=150, step=5)
    employees = st.number_input("Headcount", min_value=1, value=12, step=1)
    prev_rev = st.number_input("Previous Revenue ($)", min_value=0.0, value=220000.0, step=5000.0)

    business_data = {
        "revenue": float(revenue),
        "expenses": float(expenses),
        "customers": int(customers),
        "employees": int(employees),
        "previous_revenue": float(prev_rev),
        "profit": float(revenue - expenses),
        "revenue_growth": round(((revenue - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0, 2),
    }

tab_chat, tab_consensus = st.tabs(["💬 Interactive Copilot Chat", "👥 Multi-Agent Consensus & Debate"])


def execute_query(user_query: str):
    if api_online:
        try:
            resp = requests.post(
                f"{API_BASE_URL}/copilot/query",
                json={"query": user_query, "business_data": business_data},
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            st.error(f"API Error: {e}")

    if LOCAL_ENGINE_AVAILABLE:
        engine = CopilotEngine()
        res = engine.process_query(
            CopilotQueryRequest(query=user_query, business_data=business_data)
        )
        return res.model_dump()

    return {
        "answer": "Backend service unavailable. Please start the FastAPI backend.",
        "intent": "ERROR",
        "tool_invocations": [],
        "data_evidence": {},
        "recommended_actions": [],
        "suggested_follow_up_queries": [],
    }


with tab_chat:
    st.subheader("💡 Suggested Prompts")
    col1, col2, col3, col4 = st.columns(4)

    prompt_to_run = None
    if col1.button("🛡️ Assess Business Risk"):
        prompt_to_run = "What is our current business risk score, level, and driver breakdown?"
    if col2.button("🔬 What If Revenue Drops 15%?"):
        prompt_to_run = "What if our revenue drops by 15%?"
    if col3.button("📈 Forecast Q4 Run-Rate"):
        prompt_to_run = "Predict our future revenue and expense trajectory for the upcoming periods."
    if col4.button("🧭 Strategic Consensus Plan"):
        prompt_to_run = "What strategic action plan do the agents recommend for profitable growth?"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "evidence" in msg and msg["evidence"]:
                with st.expander("📊 View Data Evidence & Tool Invocations"):
                    st.json(msg["evidence"])

    user_input = st.chat_input("Ask BizMind AI Copilot anything about your business...") or prompt_to_run

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Synthesizing multi-agent intelligence..."):
                response_data = execute_query(user_input)
                answer = response_data.get("answer", "")
                tools = response_data.get("tool_invocations", [])
                evidence = response_data.get("data_evidence", {})
                intent = response_data.get("intent", "UNKNOWN")

                tools_str = " • ".join(tools) if tools else "Standard Analysis"
                st.caption(f"🎯 Intent: `{intent}` | 🛠️ Tools: `{tools_str}`")
                st.markdown(answer)

                if evidence:
                    with st.expander("📊 Quantitative Data Evidence Citations"):
                        st.json(evidence)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "evidence": {"tools": tools, "data": evidence},
                    }
                )


with tab_consensus:
    st.subheader("👥 Multi-Agent Collaborative Synthesis")
    st.write(
        "Domain-specific AI agents evaluate the business across Finance, Sales, Marketing, Risk, and Operations, "
        "identifying strategic tension points and generating an aligned consensus roadmap."
    )

    if st.button("🚀 Run Multi-Agent Cross-Domain Assessment", type="primary"):
        with st.spinner("Orchestrating domain agents..."):
            synthesis_data = None
            if api_online:
                try:
                    resp = requests.post(
                        f"{API_BASE_URL}/copilot/synthesize",
                        json={"business_data": business_data},
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        synthesis_data = resp.json()
                except Exception as e:
                    st.error(f"API Error: {e}")

            if not synthesis_data and LOCAL_ENGINE_AVAILABLE:
                orchestrator = MultiAgentOrchestrator()
                res = orchestrator.synthesize(
                    MultiAgentSynthesisRequest(business_data=business_data)
                )
                synthesis_data = res.model_dump()

            if synthesis_data:
                c1, c2, c3 = st.columns(3)
                score = synthesis_data["consensus_score"]
                status = synthesis_data["consensus_status"]
                risk_eval = synthesis_data.get("risk_assessment", {})

                c1.metric("Consensus Score", f"{score}%")
                c2.metric("Alignment Status", status)
                c3.metric(
                    "Risk Score",
                    f"{risk_eval.get('risk_score', 0)}/100 ({risk_eval.get('risk_level', 'Unknown')})",
                )

                st.info(f"**Executive Consensus Plan**: {synthesis_data['executive_consensus_plan']}")

                st.divider()
                st.subheader("⚖️ Strategic Debate & Tradeoffs")
                for d in synthesis_data.get("debate_points", []):
                    st.markdown(
                        f"""
                        **Topic**: {d['topic']}  
                        - *Advocating*: {', '.join(d.get('advocating_agents', []))}  
                        - *Dissenting*: {', '.join(d.get('dissenting_agents', [])) or 'None (Full Consensus)'}  
                        - *Tension*: {d['tension_description']}  
                        - **Resolution**: {d['resolution']}
                        """
                    )

                st.divider()
                st.subheader("📋 Domain Agent Perspectives")
                cols = st.columns(len(synthesis_data.get("perspectives", [])))
                for idx, p in enumerate(synthesis_data.get("perspectives", [])):
                    with cols[idx]:
                        st.markdown(f"**{p['agent_name']}**")
                        st.caption(f"Domain: {p['domain'].title()} | Priority: {p['priority_score']}/100")
                        st.write(f"Sentiment: **{p['sentiment']}**")
                        with st.expander("Key Findings"):
                            for f in p.get("key_findings", []):
                                st.write(f"- {f}")
                        with st.expander("Recommendations"):
                            for r in p.get("recommendations", []):
                                st.write(f"- {r}")

                st.divider()
                st.subheader("🎯 Explainable AI Recommendations")
                for rec in synthesis_data.get("prioritized_recommendations", []):
                    st.markdown(
                        f"""
                        #### [{rec['priority']} Priority] {rec['title']}
                        - **Category**: {rec['category']} | **Timeframe**: {rec['timeframe']} | **Feasibility**: {rec['feasibility_score']}/100
                        - **Why this was recommended**: {rec['rationale']}
                        - **Expected Impact**: {rec['expected_impact']}
                        - **Quantified ROI**: {rec.get('quantified_roi_estimate', 'N/A')} | **Risk Reduction**: -{rec['risk_reduction_potential']} pts
                        - **Action Plan**:
                        """
                    )
                    for step in rec.get("action_plan", []):
                        st.write(f"  1. {step}")
            else:
                st.error("Failed to generate multi-agent synthesis.")
