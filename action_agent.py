from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")

from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def fetch_company_actions(query:str) -> str:
    """this tool get what actions are the company doing 
    in order to reduce the carbon footprint of this product"""

    response = tavily_client.search(query, max_results=5)
    raw_text = []
    for result in response['results']:
        content = result.get('content', 'No content found')
        raw_text.append(content)
    
    return "\n\n".join(raw_text)


prompt = PromptTemplate(
    template="""You are a world-class environmental forensic analyst 
and carbon accounting expert.

OBJECTIVE:
Analyze the raw data below and extract ONLY what the company is doing 
to reduce or neutralize their carbon footprint.

OUTPUT FORMAT:
1. Program/Initiative Name
2. What exactly they are doing
3. Target year (if mentioned)
4. Verified or just a claim (if mentioned)

STRICT RULES:
- Use ONLY the provided raw data
- Zero outside information
- If data is missing, write [NOT MENTIONED IN DATA]
- Do not assume or hallucinate anything

Raw Data:
{raw_text}""",
    input_variables=["raw_text"]
)

parser = StrOutputParser()

def action_agent(query: str) -> str:
    search_query = f"{query} company carbon neutrality sustainability initiatives 2030"
    chain = RunnableLambda(fetch_company_actions) | prompt | model | parser 


    result = chain.invoke(search_query)


    with open ("action_agent_output.txt", "w") as f:
        f.write(result)

    return result

    

