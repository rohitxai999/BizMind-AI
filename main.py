from utils.data_loader import DataLoader

from agents.analytics_agent import AnalyticsAgent
from agents.business_agent import BusinessAgent
from agents.strategy_agent import StrategyAgent



loader = DataLoader()


data = loader.load_business_data(
    "data/business_data.csv"
)



analytics = AnalyticsAgent()
business = BusinessAgent()
strategy = StrategyAgent()



metrics = analytics.analyze(data)


report = business.analyze_business(metrics)


advice = strategy.generate_strategy(report)



print("="*60)
print("🚀 BizMind AI Business Intelligence Report")
print("="*60)


print("\n📊 Analytics")

for key,value in metrics.items():
    print(key,":",value)



print("\n🧠 Business Analysis")

for key,value in report.items():
    print(key,":",value)



print("\n🎯 AI Strategy")

for item in advice:
    print("-",item)