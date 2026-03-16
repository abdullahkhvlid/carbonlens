from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
parser = StrOutputParser()

prompt_template = PromptTemplate(
    template="""You are a senior environmental forensic analyst.
Analyze the provided context and generate a complete lifecycle carbon footprint report.

REPORT MUST COVER THESE STAGES WITH kg CO2e VALUES:
- Raw material mining and extraction
- Material processing and refining
- Component manufacturing
- Final assembly
- Transportation and logistics
- Consumer use phase
- End of life disposal

For each stage extract exact kg CO2e values from context.
If data unavailable for any stage, clearly state: Data Not Available.
Be precise and data-driven.

Context: {retriever_docs}
Product: {query}""",
    input_variables=["retriever_docs", "query"]
)



def audit_agent(query:str) -> str:
    # embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vector_db = FAISS.load_local(
        "my_faiss_index", 
        embeddings_model,
        allow_dangerous_deserialization=True 
    )

    print("Data Loaded from Local Folder!")


    retriever_docs = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    # results = retriever_docs.invoke("what environmental policy of iphones?")


    parallel_chain = RunnableParallel({
    "retriever_docs": retriever_docs, 
    "query": RunnablePassthrough()
    })

    chain = parallel_chain | prompt_template | model | parser
    rs = chain.invoke(query)
    # print(rs)

    with open("audit_report.txt", "w") as f:
        f.write(rs)
    return rs 