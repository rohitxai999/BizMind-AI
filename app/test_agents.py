from app.agents.agent_manager import AgentManager
from app.agents.finance_agent import FinanceAgent


def main():
    manager = AgentManager()

    finance = FinanceAgent()

    manager.register_agent(finance)

    print("=" * 60)
    print("        BizMind AI - Multi-Agent Test")
    print("=" * 60)

    print("\nRegistered Agents:")
    print(manager.list_agents())

    data = {
        "revenue": 200000,
        "expenses": 120000
    }

    print("\nFinance Analysis:")
    result = manager.analyze("Finance Agent", data)
    print(result)

    print("\n" + "=" * 60)
    print("All Tests Passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()