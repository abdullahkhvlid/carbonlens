# CarbonLens — Forensic Carbon Audit System

> *Every product has a carbon story. We reveal it.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-carbonlens--1.onrender.com-2997ff?style=for-the-badge)](https://carbonlens-1.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-1.2-1C3C3C?style=for-the-badge)](https://langchain.com)

---

## What is CarbonLens?

CarbonLens is a **production-grade multi-agent AI system** that forensically audits corporate carbon footprint claims — cross-referencing official environmental reports against real-world validated data, and delivering a verdict.

**HONEST. UNDERSTATED. SIGNIFICANTLY MISREPORTED. FRAUDULENT.**

Type any product name. Six specialized AI agents activate. In minutes, you receive a complete forensic carbon audit — including mathematical analysis of whether the company's sustainability targets are even achievable.

---

## The Problem

Corporate greenwashing is rarely lying. It is **architecture**.

Companies publish a single total carbon figure — clean, credible, responsible-looking. Then they mark 97% of the lifecycle breakdown as `Data Not Available`. The one stage they do disclose? Strategically overstated — just enough to signal accountability without actually demonstrating it.

CarbonLens was built to dismantle that architecture.

---

## System Architecture

```
User Query (e.g. "iPhone 15 Pro Max")
         │
         ▼
┌─────────────────────┐
│   Research Agent    │ ──── Tavily Search ──► FAISS Vector Store
└─────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────────┐  ┌───────────────┐
│  Audit   │  │   Validator   │ ──── Tavily Real-Time Search
│  Agent   │  │   Agent       │
│ (FAISS)  │  │ (ReAct Loop)  │
└──────────┘  └───────────────┘
    │               │
    └───────┬────────┘
            ▼
   ┌──────────────────┐
   │ Comparison Agent │ ──── Forensic Stage-by-Stage Analysis
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐
   │   Action Agent   │ ──── Company Sustainability Claims
   └──────────────────┘
            │
            ▼
   ┌──────────────────────┐
   │ Action Validator     │ ──── Tavily + Math Verification
   │ Agent (ReAct Loop)   │
   └──────────────────────┘
            │
            ▼
      Final Verdict
```

---

## The Six Agents

| Agent | Type | Role |
|-------|------|------|
| **Research Agent** | Tool + Chain | Scrapes real-time web data, builds FAISS vector knowledge base |
| **Audit Agent** | Chain | Retrieves and structures company's official carbon claims from FAISS |
| **Validator Agent** | ReAct Agent | Independently calculates true carbon footprint from live internet data |
| **Comparison Agent** | Chain | Forensic stage-by-stage comparison with discrepancy flagging |
| **Action Agent** | Tool + Chain | Extracts every sustainability promise and future target |
| **Action Validator** | ReAct Agent | Stress-tests each claim with mathematical probability models |

---

## Agent Design Philosophy

```
Chain          →  LLM already has the data. Just think.
ReAct Agent    →  LLM needs to go outside. Search. Decide. Loop.
Tool + Chain   →  Fixed fetch, then LLM structures the result.
```

ReAct agents are used where the system needs **dynamic multi-step decision making** — not a fixed pipeline.

---

## Tech Stack

```
Backend         FastAPI
AI Framework    LangChain + LangChain Classic
LLM             Google Gemini (gemini-3.1-flash-lite-preview)
Embeddings      Google Generative AI Embeddings
Vector Store    FAISS (Facebook AI Similarity Search)
Search          Tavily Real-Time Search API
Deployment      Render
Frontend        Vanilla HTML / CSS / JS
```

---

## Output Example

```
FORENSIC COMPARISON REPORT
===========================

Stage                    | Company Claimed | Real Validated | Status
-------------------------|-----------------|----------------|---------------------------
Raw Material Extraction  | Data N/A        | 37.4 kg CO2e   | [NOT DISCLOSED BY COMPANY]
Component Manufacturing  | Data N/A        | 13.4 kg CO2e   | [NOT DISCLOSED BY COMPANY]
Final Assembly           | Data N/A        | 2.7 kg CO2e    | [NOT DISCLOSED BY COMPANY]
Transportation           | 2.32 kg CO2e   | 1.64 kg CO2e   | [SERIOUS MISREPORTING]
Consumer Use Phase       | Data N/A        | 9.9 kg CO2e    | [NOT DISCLOSED BY COMPANY]
End of Life              | Data N/A        | 0.66 kg CO2e   | [NOT DISCLOSED BY COMPANY]

FINAL VERDICT: [ UNDERSTATED ]

97% of lifecycle stages hidden. The one disclosed stage: overstated by 41%.
```

---

## Project Structure

```
carbonlens/
│
├── main.py                    # Orchestration — connects all agents
├── api.py                     # FastAPI server + HTML serving
├── index.html                 # Frontend UI
│
├── research_agent.py          # Tavily search → FAISS index
├── audit_agent.py             # FAISS retrieval → company report
├── validator_agent.py         # ReAct agent → real carbon data
├── comparison_agent.py        # Forensic comparison chain
├── action_agent.py            # Company sustainability claims
├── action_validator_agent.py  # ReAct agent → claim verification
│
└── requirements.txt
```

---

## Local Setup

```bash
# Clone the repository
git clone https://github.com/abdullahkhvlid/carbonlens.git
cd carbonlens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your GOOGLE_API_KEY and TAVILY_API_KEY

# Run the server
uvicorn api:app --reload
```

Then open `index.html` in your browser or visit `http://localhost:8000`.

---

## Environment Variables

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Key Design Decisions

**Why FAISS over a cloud vector DB?**
For this use case, each query builds a fresh index from real-time scraped data. Persistence across sessions is intentionally not the goal — we want live, unbiased retrieval every time.

**Why ReAct for Validator and Action Validator?**
These agents need to make autonomous decisions — what to search next, when enough data has been gathered, how to handle missing information. A fixed chain cannot do this. ReAct agents can.

**Why Google Embeddings over HuggingFace?**
Deployment constraint. HuggingFace models require downloading 90MB+ at runtime, causing timeout failures on Render's free tier. Google Embeddings are API calls — no download, no timeout.

---

## Limitations

- Free tier Gemini API: ~30 RPM. One full audit consumes approximately 20-25 LLM calls.
- FAISS index is rebuilt per request — not persisted between sessions.
- Company PDF data requires manual ingestion into the vector store for highest accuracy.

---

## License

MIT

---

<div align="center">

**CarbonLens** — Infrastructure for accountability.

*Greenwashing just became significantly more expensive.*

</div>
