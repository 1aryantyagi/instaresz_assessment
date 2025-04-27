from typing import List, Dict
from langchain_openai import ChatOpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ResourceAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)

    def safe_invoke(self, prompt: str) -> List[Dict]:
        """Safely invoke LLM and parse JSON response."""
        try:
            response = self.llm.invoke(prompt)

            if not response.content:
                print("Warning: Empty response from LLM.")
                return []

            return json.loads(response.content)
        
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []
        
        except Exception as e:
            print(f"Unexpected error during LLM invoke: {e}")
            return []

    def generate_plan(self, use_case: str, market_trend: str) -> List[Dict]:
        """Generate a step-by-step implementation plan."""
        prompt = f"""
You are an AI assistant tasked with creating an implementation plan.
Given the AI use case and market trend below, list the key steps in clear order.
Output as a JSON list of dictionaries with "step" (number) and "description" (brief action).

Use Case: {use_case}
Market Trend: {market_trend}
"""
        return self.safe_invoke(prompt)

    def find_datasets(self, use_case: str) -> List[Dict]:
        """Find datasets for the use case."""
        prompt = f"""
You are an AI assistant tasked with finding datasets.
Find at least 3 datasets related to: {use_case}.
Source them from Kaggle, HuggingFace, or GitHub.
Output as JSON list of dictionaries with "name", "platform", and "url".
"""
        return self.safe_invoke(prompt)

    def find_models(self, use_case: str) -> List[Dict]:
        """Find pre-trained models for the use case."""
        prompt = f"""
You are an AI assistant tasked with finding pre-trained models.
Find at least 3 models suitable for: {use_case}.
Source them from HuggingFace or GitHub.
Output as JSON list of dictionaries with "name", "platform", and "url".
"""
        return self.safe_invoke(prompt)

    def find_papers(self, use_case: str) -> List[Dict]:
        """Find research papers related to the use case."""
        prompt = f"""
You are an AI assistant tasked with finding research papers.
Find at least 3 research papers relevant to: {use_case}.
Output as JSON list of dictionaries with "title", "authors" (list), and "url".
"""
        return self.safe_invoke(prompt)

    def process_resources(self, input_data: Dict) -> Dict:
        """
        Master function: Takes the whole input dict and generates:
        - Implementation plan
        - Relevant datasets
        - Pretrained models
        - Research papers
        Returns a combined dictionary.
        """
        use_case = input_data["use_case"]
        market_trend = input_data["market_trend"]

        plan = self.generate_plan(use_case, market_trend)
        datasets = self.find_datasets(use_case)
        models = self.find_models(use_case)
        papers = self.find_papers(use_case)

        output = {
            "implementation_plan": plan,
            "datasets": datasets,
            "models": models,
            "research_papers": papers
        }
        return output
