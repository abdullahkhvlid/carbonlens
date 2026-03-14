from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", streaming=False)


from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#first make the tool 
@tool 
def carbon_search_tool(query: str) -> str:
    """this tool gets the environment data from internet of this product"""
    
    response = tavily_client.search(query, max_results=5)
    raw_text = []
    for result in response['results']:
        content = result.get('content', 'No content found')
        raw_text.append(content)
    
    return "\n\n".join(raw_text)

prompt = PromptTemplate.from_template("""You are a world-class environmental forensic analyst 
and carbon accounting expert with deep knowledge of global supply chains, 
manufacturing processes, and 2026 IPCC/GHG Protocol standards.

OBJECTIVE:
Conduct a complete lifecycle carbon footprint analysis of the given product.
First identify what type of product it is, then dynamically determine all relevant 
stages of its lifecycle. Search the internet thoroughly for real data.
For missing or incomplete data, apply your expert knowledge to provide the most 
statistically probable estimate.

CRITICAL SEARCH RULES — FOLLOW STRICTLY:
- Every search query must be under 10 words
- Never copy prompt instructions into search query
- Never search multiple stages at once
- Good: "Samsung S26 Ultra manufacturing emissions"
- Bad: "Conduct complete lifecycle carbon footprint analysis for Samsung Galaxy S26 Ultra"

MANDATORY SEARCH SEQUENCE — ONE SEARCH PER STAGE:
Step 1: "[product name] carbon footprint total kg CO2e"
Step 2: "[product name] raw materials mining emissions"
Step 3: "[product name] manufacturing assembly emissions"
Step 4: "[product name] transportation logistics carbon"
Step 5: "[product name] consumer use phase energy emissions"
Step 6: "[product name] end of life recycling carbon"

Each step = ONE separate search call.
Never combine multiple stages in one search query.

ANALYSIS APPROACH:
- First identify: What is this product? What industry? What materials?
- Then determine: What are ALL the lifecycle stages specific to THIS product?
- Cover everything from raw material extraction to end of life
- Every product is different — a cotton t-shirt has different stages than a smartphone

STAGES TO CONSIDER (adapt based on product):
- Raw material extraction/farming/mining
- Material processing and refining
- Component or part manufacturing  
- Final assembly or production
- Packaging
- Transportation and logistics at every stage
- Consumer use phase (if applicable)
- End of life and disposal

CRITICAL RULES:
- All emissions in kg CO2 equivalent (kg CO2e)
- Use 2026 GHG Protocol and IPCC AR6 standards
- If official data unavailable → use industry average from trained knowledge, label as [ESTIMATED]
- If reported data seems underreported → flag as [SUSPICIOUS] and provide realistic range
- Be mathematically precise — show calculations where possible
- Adapt your analysis to the specific product — do not force irrelevant categories

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

Question: Conduct complete carbon footprint lifecycle analysis for: {input}
Thought:{agent_scratchpad}""")


def validator_agent(query: str) -> str:
    agent = create_react_agent(model, [carbon_search_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[carbon_search_tool], verbose=True, handle_parsing_errors=True, max_iterations=10)

    answer = agent_executor.invoke({"input": query})
    validator_report = answer["output"]  

    with open("validator_report.txt", "w") as f:
        f.write(validator_report)

    return validator_report



