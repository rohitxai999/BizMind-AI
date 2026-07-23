import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load the .env file from the backend directory
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class MarketAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please create backend/.env and add:\n"
                "GROQ_API_KEY=your_groq_api_key"
            )

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.4,
        )

        self.prompt = ChatPromptTemplate.from_template("""
You are an expert market research analyst.

Analyze the following business idea.

Business Idea:
{idea}

Generate a detailed market research report including:

# Industry Overview

# Market Size

# Target Audience

# Customer Pain Points

# Competitor Analysis

# Market Trends

# Business Opportunities

# Threats

Respond in professional Markdown.
""")

    def analyze(self, idea: str):
        chain = self.prompt | self.llm
        result = chain.invoke({"idea": idea})
        return result.content