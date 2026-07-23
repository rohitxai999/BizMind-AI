import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load the .env file from the backend directory
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class BusinessAgent:
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
You are an experienced business consultant.

Analyze the following business idea.

Business Idea:
{idea}

Provide:

1. Business Summary

2. Target Customers

3. Main Problem Being Solved

4. Unique Value Proposition

5. Strengths

6. Weaknesses

7. Opportunities

8. Risks

Respond in clean Markdown.
""")

    def analyze(self, idea: str):
        chain = self.prompt | self.llm
        result = chain.invoke({"idea": idea})
        return result.content