from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", streaming=False)


from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool 
def validate_action(action: str) -> str:
    """this tool validates the action agent's output for accuracy
      and completeness validates the company's action data using real time internet data"""
    response = tavily_client.search(action, max_results=5)
    raw_text = []
    for result in response['results']:
        content = result.get('content', 'No content found')
        raw_text.append(content)
    
    return "\n\n".join(raw_text)

prompt = PromptTemplate.from_template("""You are a world-class environmental forensic analyst 
and carbon accounting expert with deep knowledge of global supply chains, 
manufacturing processes, and 2026 IPCC/GHG Protocol standards.

HERE ARE THE COMPANY CLAIMS TO VALIDATE:
{action_agent_output_txt}

OBJECTIVE:
Validate each company claim about carbon footprint reduction actions.
Cross-check using real-time internet data where available.
For future targets, use progress analysis and statistical estimation.

CRITICAL SEARCH RULE:
- Extract 4-6 key terms from each claim
- Never pass full claim text as search query
- Keep every search query under 300 characters
- Example: "Apple 2030 renewable energy progress"

VALIDATION APPROACH:

Step 1 - FOR VERIFIABLE CLAIMS (past/present actions):
- Search internet for third party confirmation
- Search for actual progress reports and numbers
- Search for any contradicting evidence or greenwashing reports

Step 2 - FOR FUTURE TARGETS (2030/2040 goals):
- Search current progress data (how much achieved so far)
- Calculate required annual reduction rate to meet target
- Compare with historical reduction rate of this company
- Estimate: is target mathematically achievable?

Step 3 - PATTERN ANALYSIS:
- Are these standard boilerplate ESG claims?
- Is progress consistent with claims?
- Any red flags or greenwashing patterns?

OUTPUT FORMAT FOR EACH CLAIM:
---
CLAIM: [exact claim]
SEARCHED FOR: [what you searched]
REAL DATA FOUND: [what internet said]
PROGRESS SO FAR: [numbers if available]
MATHEMATICAL ESTIMATE: [if future target — is it achievable?]
VERDICT: [VERIFIED / PARTIALLY TRUE / BEHIND TARGET / GREENWASHING / UNVERIFIABLE]
CONFIDENCE: [HIGH / MEDIUM / LOW]
---

FINAL SUMMARY:
- Overall assessment of company's carbon actions
- Most credible actions
- Most suspicious claims
- Probability of meeting stated targets

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}""")


def action_validator_agent(action_agent_output_txt: str) -> str:
  
    agent = create_react_agent(model, [validate_action], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[validate_action], 
                               verbose=True, handle_parsing_errors=True, 
                               max_iterations=25)

    answer = agent_executor.invoke({
        "input": "Validate all company claims listed above",
        "action_agent_output_txt": action_agent_output_txt
    })

    with open("action_validator_report.txt", "w") as f:
        f.write(answer["output"])

    return answer["output"]