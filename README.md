## Company Analysis App (instaresz_assessment)

An interactive Streamlit application that lets you research any company, generate AI/GenAI use cases for its market, and compile implementation resources. It uses a modular **agent** architecture orchestrated by a `MasterAgent` to run three steps in sequence:

1. **Research Agent**  
   Scrapes the web and Wikipedia for raw company data using DuckDuckGo queries and BeautifulSoup.

2. **Market Analysis Agent**  
   Uses GPT-4 (via LangChain) to propose AI/GenAI use cases tailored to the company’s market.

3. **Resource Agent**  
   Gathers implementation plans, public datasets, pre-trained models, and related research papers.

---

## Features

- **Streamlit UI**  
  - Health-check endpoint  
  - Company-name input  
  - Interactive, expandable display of findings  

- **Modular Agents**  
  - `agents/research_agent.py`  
  - `agents/market_analysis_agent.py`  
  - `agents/resource_agent.py`  
  - `agents/tools/research.py` (DuckDuckGo + BeautifulSoup scraper)  

- **Orchestration**  
  - `main.py` defines `MasterAgent` to coordinate the workflow  

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/1aryantyagi/instaresz_assessment.git
   cd instaresz_assessment
   ```
   
2. **Set up a virtual environment**
   ```bash
     python3 -m venv venv
    source venv/bin/activate
   ```
   
3. **Install dependencies**
   ```bash
     pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create Open AI API key and enter in .env file
   ```bash
     OPENAI_API_KEY=your_api_key_here
   ```

## Usage
Run the Streamlit app
```bash
  streamlit run app.py
```

## Project Structure
```bash
  instaresz_assessment/
  ├── .devcontainer/               # Dev container settings
  ├── agents/
  │   ├── market_analysis_agent.py # Generates AI use cases
  │   ├── research_agent.py        # Research scraping agent
  │   ├── resource_agent.py        # Resource-gathering agent
  │   └── tools/
  │       └── research.py          # DuckDuckGo + BeautifulSoup scraper
  ├── app.py                       # Streamlit front-end
  ├── main.py                      # MasterAgent orchestrator
  ├── requirements.txt             # Python dependencies
  └── .gitignore                   # Ignored files
```
