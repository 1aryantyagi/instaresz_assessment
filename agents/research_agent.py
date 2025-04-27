from dotenv import load_dotenv
import json

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.prebuilt import create_react_agent

# Your existing ResearchAgent import
from agents.tools.research import ResearchAgent

load_dotenv()


class ResearchLangGraphAgent:
    def __init__(self):
        # Initialize the LLM (ChatGPT GPT-4 here)
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.5)

        # Initialize your wrapped research agent (non-LangChain)
        self.research_agent = ResearchAgent()

        # Define the tool using @tool decorator from langchain_core.tools
        @tool
        def company_research_tool(query: str) -> str:
            """
            Perform deep web research about a company and return detailed findings.
            """
            info = self.research_agent.get_company_info(query)
            combined_info = ""
            if "wikipedia" in info:
                combined_info += f"Wikipedia Info:\n{info['wikipedia']}\n\n"
            if "website" in info:
                combined_info += f"Website Info:\n{info['website']}\n"
            return combined_info or "No information found."

        self.company_research_tool = company_research_tool

        # Create the LangGraph React agent with debug enabled for verbose logs
        self.agent = create_react_agent(
            model=self.llm,
            tools=[self.company_research_tool],
            debug=True  # Set to False to reduce verbosity
        )

    def analyze_company(self, company_info: str) -> dict:
        """Analyze scraped company info into structured JSON."""
        prompt = ChatPromptTemplate.from_template(
            """
            Analyze the following company information:
            {company_info}

            Extract and return the information in this JSON format:
            {{
                "industry": string,
                "key_offerings": [list of strings],
                "strategic_focus": [list of strings],
                "market_position": string
            }}
            Only output JSON. No explanation.
            """
        )

        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"company_info": company_info})

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {"error": "Failed to parse JSON", "raw_response": response}

        return parsed

    def research_and_analyze(self, company_name: str) -> dict:
        """
        Full workflow: search, gather, and analyze a company.

        This method calls the LangGraph agent with a user message and
        then analyzes the text response into structured JSON.
        """
        print(f"🔎 Researching: {company_name}")

        # Invoke the LangGraph agent with a message history (single human message)
        response = self.agent.invoke({"messages": [("human", f"Find detailed information about {company_name}")], "stream_mode": None})

        # The last message from the agent contains the final answer text
        research_result = response["messages"][-1].content

        print(f"📄 Research Result:\n{research_result}\n")

        analysis = self.analyze_company(research_result)

        print(f"📊 Analysis:\n{json.dumps(analysis, indent=2)}")

        return analysis