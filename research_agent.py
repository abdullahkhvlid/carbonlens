import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools import tool


from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS




@tool 
def search_tool(query: str ) -> str:
    """this tool gets the environment data from internet of this 
    product"""

    response = tavily_client.search(f"{query}", max_results=5)
    return response
    

def research_agent(query: str) -> str:
    # embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    research_data = search_tool.invoke({"query": query})


    raw_text =[]
    for i in range(5):
        content = research_data['results'][i].get('content', 'No content found')
        raw_text.append(content)


    vector_db = FAISS.from_texts(raw_text, embeddings_model)
    vector_db.save_local("my_faiss_index")
    return "FAISS index saved successfully"



