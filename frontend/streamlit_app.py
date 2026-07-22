import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="BizMind AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 BizMind AI")
st.subheader("Autonomous AI Business Intelligence Platform")

st.divider()

# ============================
# Sidebar
# ============================

st.sidebar.title("BizMind AI")

st.sidebar.success("🟢 Data Agent Online")
st.sidebar.success("🟢 Finance Agent Online")
st.sidebar.success("🟢 Health Agent Online")
st.sidebar.success("🟢 Strategy Agent Online")

# ============================
# Upload CSV
# ============================

uploaded_file = st.file_uploader(
    "Upload Business CSV",
    type=["csv"]
)

if uploaded_file is not None:

    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)

    st.success("Business data loaded successfully ✅")

    if st.button("🚀 Run AI Analysis"):

        file_bytes = uploaded_file.getvalue()

        # ----------------------------
        # Data Agent
        # ----------------------------

        data_response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files={
                "file": (
                    uploaded_file.name,
                    file_bytes,
                    "text/csv"
                )
            }
        )

        if data_response.status_code != 200:
            st.error("Data Agent Error")
            st.code(data_response.text)
            st.stop()

        data = data_response.json()

        # ----------------------------
        # Finance Agent
        # ----------------------------

        finance_response = requests.post(
            "http://127.0.0.1:8000/finance",
            files={
                "file": (
                    uploaded_file.name,
                    file_bytes,
                    "text/csv"
                )
            }
        )

        if finance_response.status_code != 200:
            st.error("Finance Agent Error")
            st.code(finance_response.text)
            st.stop()

        finance = finance_response.json()

        # ----------------------------
        # Health Agent
        # ----------------------------

        health_response = requests.post(
            "http://127.0.0.1:8000/health",
            json={
                "revenue": finance["revenue"],
                "profit": finance["profit"],
                "expenses": finance["expenses"],
                "risk": finance["risk"]
            }
        )

        if health_response.status_code != 200:
            st.error("Health Agent Error")
            st.code(health_response.text)
            st.stop()

        health = health_response.json()

        # ----------------------------
        # Strategy Agent
        # ----------------------------

        strategy_response = requests.post(
            "http://127.0.0.1:8000/strategy",
            json={
                "revenue": finance["revenue"],
                "profit": finance["profit"],
                "risk": finance["risk"]
            }
        )

        if strategy_response.status_code != 200:
            st.error("Strategy Agent Error")
            st.code(strategy_response.text)
            st.stop()

        strategy = strategy_response.json()

        # ============================
        # Business Overview
        # ============================

        st.header("📊 Business Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Sales", data["total_sales"])

        with col2:
            st.metric("Revenue", f"₹{data['total_revenue']}")

        with col3:
            st.metric("Best Product", data["best_product"])

        st.divider()

        # ============================
        # Finance Dashboard
        # ============================

        st.header("💰 Financial Intelligence")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Expenses", f"₹{finance['expenses']}")

        with col5:
            st.metric("Profit", f"₹{finance['profit']}")

        with col6:
            st.metric("Risk Level", finance["risk"])

        st.divider()

        # ============================
        # Business Health
        # ============================

        st.header("❤️ Business Health")

        col7, col8 = st.columns(2)

        with col7:
            st.metric(
                "Health Score",
                f"{health['score']} / 100"
            )

        with col8:
            st.metric(
                "Status",
                health["status"]
            )

        st.progress(health["score"] / 100)

        st.divider()

        # ============================
        # Charts
        # ============================

        st.header("📈 Revenue Analysis")

        chart1, chart2 = st.columns(2)

        with chart1:
            fig = px.bar(
                df,
                x="Product",
                y="Revenue",
                title="Revenue by Product"
            )
            st.plotly_chart(fig, use_container_width=True)

        with chart2:
            fig2 = px.pie(
                df,
                values="Revenue",
                names="Product",
                title="Revenue Distribution"
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # ============================
        # Strategy
        # ============================

        st.header("🧠 AI CEO Recommendations")

        for recommendation in strategy["recommendations"]:
            st.success(recommendation)

        st.divider()

        # ============================
        # Executive Summary
        # ============================

        st.header("📋 Executive Summary")

        st.info(
            f"""
Revenue Generated : ₹{finance['revenue']}

Profit : ₹{finance['profit']}

Business Health : {health['status']}

Health Score : {health['score']} / 100

Risk Level : {finance['risk']}

Top Product : {data['best_product']}

BizMind AI recommends focusing on high-performing products while controlling operational expenses for sustainable business growth.
"""
        )

        # ============================
        # Download Report
        # ============================

        report = f"""
==========================
      BIZMIND AI REPORT
==========================

BUSINESS OVERVIEW

Total Sales : {data['total_sales']}
Revenue : ₹{finance['revenue']}
Expenses : ₹{finance['expenses']}
Profit : ₹{finance['profit']}

Best Product : {data['best_product']}

Business Health : {health['status']}
Health Score : {health['score']} / 100

Risk Level : {finance['risk']}

==========================

AI RECOMMENDATIONS

"""

        for rec in strategy["recommendations"]:
            report += f"\n• {rec}"

        report += """

==========================

Generated by BizMind AI
Autonomous Business Intelligence Platform

==========================
"""

        st.download_button(
            label="📄 Download AI Business Report",
            data=report,
            file_name="BizMind_AI_Report.txt",
            mime="text/plain"
        )

else:
    st.info("Upload a CSV file to start AI analysis.")