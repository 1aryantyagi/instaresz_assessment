## Company Analysis App (instaresz_assessment)

An interactive Streamlit application that lets you research any company, generate AI/GenAI use cases for its market, and compile implementation resources. It uses a modular **agent** architecture orchestrated by a `MasterAgent` to run three steps in sequence:

> 🔗 **Live Demo**: [Click here](https://1aryantyagi-instaresz-assessment-app-4diyhb.streamlit.app/)

## How It Works

1. **Research Agent**  
   Scrapes the web and Wikipedia for raw company information using DuckDuckGo search and BeautifulSoup parsing.

2. **Market Analysis Agent**  
   Uses GPT-4 (via LangChain) to suggest customized AI/GenAI use cases based on the company's industry.

3. **Resource Agent**  
   Collects practical resources including implementation plans, public datasets, pre-trained models, and research papers.

---

## Features

- **Streamlit UI**
  - Health-check endpoint
  - Company name input field
  - Interactive, expandable display of results

- **Modular Agents**
  - `agents/research_agent.py` — Research scraping agent
  - `agents/market_analysis_agent.py` — AI use case generator
  - `agents/resource_agent.py` — Resource compilation agent
  - `agents/tools/research.py` — DuckDuckGo + BeautifulSoup scraper

- **Orchestration**
  - `main.py` defines the `MasterAgent` to coordinate the full workflow

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
