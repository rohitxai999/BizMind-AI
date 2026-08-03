import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="BizMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    .block-container {padding-top:2rem; padding-bottom:2rem; max-width:95%;}
    .main-title {font-size:42px; font-weight:800; color:#2563eb; margin-bottom:0px;}
    .subtitle {font-size:18px; color:#6b7280; margin-bottom:25px;}
    hr {margin-top:20px; margin-bottom:20px;}
    [data-testid="stMetric"] {background:#ffffff; border-radius:15px; padding:15px; border:1px solid #E5E7EB; box-shadow:0 5px 15px rgba(0,0,0,.08);}
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="main-title">🧠 BizMind AI Executive Dashboard</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">Autonomous Multi-Agent Business Intelligence Platform</div>
    """,
    unsafe_allow_html=True,
)

st.divider()


with st.sidebar:
    st.title("🧠 BizMind AI")
    st.caption("Executive Intelligence Platform")
    st.divider()
    st.success("🟢 Data Agent Online")
    st.success("🟢 Finance Agent Online")
    st.success("🟢 Health Agent Online")
    st.success("🟢 Strategy Agent Online")
    st.divider()
    st.metric("Platform Status", "ONLINE")
    st.metric("Running Agents", "4")
    st.metric("Version", "Day 5")
    st.divider()
    st.info("Upload a business CSV and run AI analysis to generate executive insights.")


def compute_local_finance(df):
    revenue = float(df["Revenue"].sum()) if "Revenue" in df.columns else 0.0
    expenses = float(df["Expenses"].sum()) if "Expenses" in df.columns else 0.0
    profit = revenue - expenses

    if revenue > 0:
        expense_ratio = (expenses / revenue) * 100
        profit_margin = (profit / revenue) * 100
    else:
        expense_ratio = 0.0
        profit_margin = 0.0

    if expense_ratio > 70 or profit_margin < 5:
        risk = "High"
    elif expense_ratio > 50 or profit_margin < 15:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "revenue": int(revenue),
        "profit": int(profit),
        "expenses": int(expenses),
        "risk": risk,
    }


def build_local_health(finance):
    score = 100

    if finance["profit"] < finance["revenue"] * 0.20:
        score -= 20

    if finance["expenses"] > finance["revenue"] * 0.70:
        score -= 20

    if finance["risk"] == "High":
        score -= 30
    elif finance["risk"] == "Medium":
        score -= 15

    score = max(0, min(100, score))

    if score >= 85:
        status = "Excellent"
    elif score >= 70:
        status = "Good"
    elif score >= 50:
        status = "Average"
    else:
        status = "Poor"

    return {"score": score, "status": status}


def build_local_strategy(finance):
    recommendations = []

    if finance["risk"] == "High":
        recommendations.append("Protect cash flow and reduce unnecessary spending immediately.")

    if finance["profit"] < finance["revenue"] * 0.2:
        recommendations.append("Focus on higher-margin products and tighten pricing discipline.")

    if finance["revenue"] < 100000:
        recommendations.append("Increase targeted marketing on the strongest-performing channels.")

    recommendations.append("Improve customer retention with loyalty and service programs.")
    recommendations.append("Automate repeatable workflows to improve operating efficiency.")

    return {"recommendations": recommendations[:5]}


def get_chart_columns(df):
    if df.empty:
        return None, None

    preferred_category = None
    preferred_value = None

    if "Product" in df.columns:
        preferred_category = "Product"
    elif "Category" in df.columns:
        preferred_category = "Category"
    elif "Name" in df.columns:
        preferred_category = "Name"

    if "Revenue" in df.columns:
        preferred_value = "Revenue"
    elif "sales" in df.columns:
        preferred_value = "sales"
    elif "amount" in df.columns:
        preferred_value = "amount"

    if preferred_category and preferred_value:
        return preferred_category, preferred_value

    string_columns = [
        col for col in df.columns
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])
    ]
    numeric_columns = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    if string_columns and numeric_columns:
        return string_columns[0], numeric_columns[0]

    if numeric_columns:
        return numeric_columns[0], numeric_columns[0]

    return None, None


uploaded_file = st.file_uploader(
    "📂 Upload Business CSV",
    type=["csv"],
    help="Supported format: CSV",
)

if uploaded_file is not None:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)

    st.success("✅ Business dataset loaded successfully.")

    with st.expander("Preview Dataset", expanded=False):
        st.dataframe(df.head())

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

    if st.button("🚀 Run Executive AI Analysis", use_container_width=True):
        file_bytes = uploaded_file.getvalue()

        with st.spinner("🤖 BizMind AI is analyzing your business..."):
            data = None
            finance = None
            health = None
            strategy = None

            try:
                data_response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files={"file": (uploaded_file.name, file_bytes, "text/csv")},
                    timeout=60,
                )
                data_response.raise_for_status()
                data = data_response.json()
            except Exception:
                data = {
                    "total_sales": int(df["Units_Sold"].sum()) if "Units_Sold" in df.columns else 0,
                    "total_revenue": int(df["Revenue"].sum()) if "Revenue" in df.columns else 0,
                    "best_product": df.loc[df["Revenue"].idxmax(), "Product"] if "Revenue" in df.columns and "Product" in df.columns else "N/A",
                    "insight": "Local fallback analysis used.",
                }

            try:
                finance_response = requests.post(
                    "http://127.0.0.1:8000/finance",
                    files={"file": (uploaded_file.name, file_bytes, "text/csv")},
                    timeout=60,
                )
                finance_response.raise_for_status()
                finance = finance_response.json()
            except Exception:
                finance = compute_local_finance(df)

            try:
                health_response = requests.post(
                    "http://127.0.0.1:8000/health",
                    json={
                        "revenue": finance["revenue"],
                        "profit": finance["profit"],
                        "expenses": finance["expenses"],
                        "risk": finance["risk"],
                    },
                    timeout=60,
                )
                health_response.raise_for_status()
                health = health_response.json()
            except Exception:
                health = build_local_health(finance)

            try:
                strategy_response = requests.post(
                    "http://127.0.0.1:8000/strategy",
                    json={
                        "revenue": finance["revenue"],
                        "profit": finance["profit"],
                        "risk": finance["risk"],
                    },
                    timeout=60,
                )
                strategy_response.raise_for_status()
                strategy = strategy_response.json()
            except Exception:
                strategy = build_local_strategy(finance)

        st.session_state.analysis_results = {
            "data": data,
            "finance": finance,
            "health": health,
            "strategy": strategy,
            "df": df,
        }
        st.success("✅ Analysis completed successfully.")

    if st.session_state.analysis_results is not None:
        analysis = st.session_state.analysis_results
        data = analysis["data"]
        finance = analysis["finance"]
        health = analysis["health"]
        strategy = analysis["strategy"]
        df = analysis["df"]

        st.subheader("📊 Executive Business Dashboard")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric("💰 Revenue", f"₹{finance['revenue']:,.2f}")

        with kpi2:
            st.metric("📈 Profit", f"₹{finance['profit']:,.2f}")

        with kpi3:
            st.metric("💸 Expenses", f"₹{finance['expenses']:,.2f}")

        with kpi4:
            st.metric("❤️ Health Score", f"{health['score']}/100")

        st.divider()

        overview1, overview2, overview3 = st.columns(3)

        with overview1:
            st.metric("🛒 Total Sales", data["total_sales"])

        with overview2:
            st.metric("🏆 Best Product", data["best_product"])

        with overview3:
            st.metric("⚠ Risk Level", finance["risk"])

        st.divider()

        health_col1, health_col2 = st.columns([2, 1])
        with health_col1:
            st.subheader("Business Health")
            st.progress(health["score"] / 100)

        with health_col2:
            st.metric("Current Status", health["status"])

        st.success(f"Overall Business Health: {health['status']} ({health['score']}/100)")
        st.divider()

        st.subheader("📈 Executive Analytics Dashboard")
        chart1, chart2 = st.columns(2)

        category_col, value_col = get_chart_columns(df)

        with chart1:
            if category_col and value_col and category_col != value_col:
                plot_df = df[[category_col, value_col]].dropna()
                fig = px.bar(plot_df, x=category_col, y=value_col, color=value_col, title=f"{value_col} by {category_col}", text=value_col)
                fig.update_layout(template="plotly_white", height=450)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ No compatible category/value columns were found for the bar chart.")

        with chart2:
            if category_col and value_col:
                plot_df = df[[category_col, value_col]].dropna()
                fig2 = px.pie(plot_df, values=value_col, names=category_col, hole=0.45, title="Value Distribution")
                fig2.update_layout(height=450)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("ℹ️ No compatible columns were found for the pie chart.")

        st.divider()

        st.subheader("📊 Business Insights")
        numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        if "Quantity" in df.columns and "Revenue" in df.columns:
            fig3 = px.scatter(df, x="Quantity", y="Revenue", color="Product" if "Product" in df.columns else None, size="Revenue", hover_name="Product" if "Product" in df.columns else None, title="Revenue vs Quantity")
            fig3.update_layout(template="plotly_white", height=500)
            st.plotly_chart(fig3, use_container_width=True)
        elif len(numeric_columns) >= 2:
            x_col, y_col = numeric_columns[0], numeric_columns[1]
            fig3 = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            fig3.update_layout(template="plotly_white", height=500)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("ℹ️ No suitable numeric columns were found for the scatter chart.")

        st.subheader("🏆 Top Performing Products")
        sort_col = "Revenue" if "Revenue" in df.columns else (numeric_columns[0] if numeric_columns else None)
        if sort_col:
            top_products = df.sort_values(by=sort_col, ascending=False)
        else:
            top_products = df
        st.dataframe(top_products, use_container_width=True)
        st.divider()

        st.subheader("🧠 AI CEO Recommendations")
        for i, recommendation in enumerate(strategy["recommendations"], start=1):
            st.success(f"**Recommendation {i}:** {recommendation}")
        st.divider()

        st.subheader("📋 Executive Summary")
        summary_col1, summary_col2 = st.columns([2, 1])

        with summary_col1:
            st.markdown(
                f"""
                ### Business Performance Overview
                **Revenue:** ₹{finance['revenue']:,.2f}
                **Profit:** ₹{finance['profit']:,.2f}
                **Expenses:** ₹{finance['expenses']:,.2f}
                **Business Health:** {health['status']}
                **Health Score:** {health['score']}/100
                **Risk Level:** {finance['risk']}
                **Top Product:** {data['best_product']}
                **Total Sales:** {data['total_sales']}
                """
            )

        with summary_col2:
            st.metric("Overall Health", f"{health['score']}/100")
            st.metric("Risk", finance["risk"])
            st.metric("Top Product", data["best_product"])

        st.info("BizMind AI recommends maintaining strong-performing products, optimizing operational expenses, and continuously monitoring business risk to improve long-term profitability.")
        st.divider()

        st.subheader("📄 Executive Business Report")
        report = f"""
        ======================================================
                        BIZMIND AI REPORT
        ======================================================

        EXECUTIVE SUMMARY

        Revenue           : ₹{finance['revenue']}
        Profit            : ₹{finance['profit']}
        Expenses          : ₹{finance['expenses']}

        Business Health   : {health['status']}
        Health Score      : {health['score']}/100

        Risk Level        : {finance['risk']}

        Best Product      : {data['best_product']}

        Total Sales       : {data['total_sales']}

        ======================================================

        AI CEO RECOMMENDATIONS
        """

        for i, rec in enumerate(strategy["recommendations"], start=1):
            report += f"\n{i}. {rec}"

        report += f"""

        ======================================================

        EXECUTIVE INSIGHT

        BizMind AI analysis indicates the business is currently
        rated "{health['status']}" with a health score of
        {health['score']}/100.

        Continuous monitoring of revenue, profitability,
        operational costs, and business risks is recommended.

        ======================================================

        Generated Automatically by BizMind AI
        Autonomous Multi-Agent Business Intelligence Platform

        ======================================================
        """

        st.download_button(
            "📥 Download Executive Report",
            report,
            file_name="BizMind_AI_Executive_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.balloons()

        st.divider()
        st.subheader("🤖 BizMind AI Copilot")
        st.caption("Ask for focused recommendations based on your current executive metrics.")
        user_question = st.text_input("Ask your business question", placeholder="Example: How can I increase profit?")

        if st.button("Generate AI Advice", use_container_width=True):
            question = user_question.lower()
            advice = []

            if finance["risk"] == "High":
                advice.append("• Prioritize cash preservation and trim discretionary spend immediately.")
            elif finance["risk"] == "Medium":
                advice.append("• Keep a close eye on operating leverage and review pricing discipline.")
            else:
                advice.append("• Maintain momentum and expand on the highest-performing channels.")

            if finance["profit"] < finance["revenue"] * 0.2:
                advice.append("• Improve margin mix by prioritizing higher-margin offerings.")
            else:
                advice.append("• Protect profitability while scaling the most efficient products.")

            if "profit" in question:
                advice.append("• Focus on margin expansion, pricing, and expense discipline.")
            elif "sales" in question:
                advice.append("• Increase targeted acquisition spend and promote your best-performing offers.")
            elif "risk" in question:
                advice.append("• Diversify revenue sources and strengthen contingency planning.")
            elif "expense" in question:
                advice.append("• Reduce overhead and automate repeatable processes.")
            else:
                advice.append("• Monitor weekly KPIs and turn insights into immediate operating actions.")

            st.success("\n".join(advice))

        st.divider()
        st.subheader("❤️ Executive Business Health")
        health_percentage = health["score"] / 100
        st.progress(health_percentage)

        if health["score"] >= 85:
            st.success("🟢 Excellent Business Performance")
        elif health["score"] >= 70:
            st.warning("🟡 Healthy Business")
        elif health["score"] >= 50:
            st.warning("🟠 Improvement Recommended")
        else:
            st.error("🔴 Immediate Action Required")

        st.divider()
        st.subheader("🎮 Business Scenario Simulator")
        marketing = st.slider("Marketing Budget Increase (%)", 0, 100, 20)
        cost = st.slider("Cost Reduction (%)", 0, 50, 10)
        predicted_growth = (marketing * 0.4) + (cost * 0.6)
        st.metric("Predicted Growth", f"{predicted_growth:.1f}%")

        if predicted_growth > 35:
            st.success("Excellent projected business growth.")
        elif predicted_growth > 20:
            st.info("Good projected business growth.")
        else:
            st.warning("Growth projection is limited. Consider increasing investment or improving efficiency.")
else:
    st.info("📂 Upload a CSV file to start the executive analysis workflow.")