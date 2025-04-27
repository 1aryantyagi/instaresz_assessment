import json
import re
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
load_dotenv()

class UseCaseGenerationTool:
    """
    Generate AI/GenAI use cases for a given industry and focus areas.
    """
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.3):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        system_msg = SystemMessage(content=(
            "You are an AI strategist. Generate innovative AI/GenAI use cases for an industry with given focus areas. "
            "Respond as a JSON list of dictionaries with 'use_case', 'market_trend', and 'implementation_steps'. "
            "Provide the JSON directly without markdown formatting."
        ))
        user_template = (
            "Industry: {industry}\n"
            "Key Offerings: {key_offerings}\n"
            "Strategic Focus: {strategic_focus}\n"
            "Market Position: {market_position}"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            system_msg,
            HumanMessagePromptTemplate.from_template(user_template)
        ])
        self.output_parser = StrOutputParser()

    def generate_use_cases(
        self, 
        industry: str, 
        key_offerings: List[str], 
        strategic_focus: List[str], 
        market_position: str
    ) -> List[Dict[str, Any]]:
        """
        Generate use cases based on inputs.
        """
        messages = self.prompt.format_messages(
            industry=industry,
            key_offerings=", ".join(key_offerings),
            strategic_focus=", ".join(strategic_focus),
            market_position=market_position
        )
        response = self.llm.invoke(messages)
        content = response.content if hasattr(response, "content") else str(response)
        content = self.output_parser.parse(content)
        
        # Preprocess to remove markdown code blocks
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'\s*```', '', content)
        
        # Debugging: Print raw content to inspect
        print("Raw Response Content:", content)
        
        try:
            use_cases = json.loads(content)
            if not isinstance(use_cases, list):  # Ensure it's a list
                use_cases = []
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            use_cases = []
        return use_cases


class MarketAnalysisAgent:
    """
    Agent that handles generating use cases with provided market data.
    """
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.3):
        self.market_agent = UseCaseGenerationTool(model_name=model_name, temperature=temperature)

    def generate_use_cases(
        self, 
        industry: str, 
        key_offerings: List[str], 
        strategic_focus: List[str], 
        market_position: str
    ) -> List[Dict[str, Any]]:
        """
        Interface to directly generate use cases given market inputs.
        """
        return self.market_agent.generate_use_cases(
            industry, key_offerings, strategic_focus, market_position
        )

    def execute_workflow(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow when market data (not company name) is already provided.
        """
        use_cases = self.generate_use_cases(
            market_data.get("industry", ""),
            market_data.get("key_offerings", []),
            market_data.get("strategic_focus", []),
            market_data.get("market_position", "")
        )
        return {
            "generated_use_cases": use_cases
        }