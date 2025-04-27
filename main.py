from agents.research_agent import ResearchLangGraphAgent
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.resource_agent import ResourceAgent
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
import json

load_dotenv()

class MasterAgent:
    def __init__(self):
        self.research_agent = ResearchLangGraphAgent()
        self.market_agent = MarketAnalysisAgent()
        self.resource_agent = ResourceAgent()

    def execute_workflow(self, company: str):
        # Step 1: Company Research
        analysis = self.research_agent.research_and_analyze(company)

        print("*" * 50)
        print(type(analysis))
        print(analysis)
        print("*" * 50)
        
        # Step 2: Market Analysis
        use_cases = self.market_agent.execute_workflow(analysis)
        use_cases = use_cases.get("generated_use_cases", [])

        print("*" * 50)
        print(type(use_cases))
        print(use_cases)
        print("*" * 50)

        
        # Step 3: Resource Collection
        resources = []
        for use_case in use_cases[:3]:
            result = self.resource_agent.process_resources(use_case)
            resources.append(result)

        print("*" * 50)
        print(type(resources))
        print(resources)
        print("*" * 50)
        
        return analysis, use_cases, resources

if __name__ == "__main__":
    agent = MasterAgent()
    company = input("Enter company/industry to analyze: ")
    report = agent.execute_workflow(company)
    print("Report generated successfully!")