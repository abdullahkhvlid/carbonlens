from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
import os

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()
prompt = PromptTemplate(
    template="""You are a world-class environmental forensic analyst and carbon accounting 
expert with deep knowledge of global supply chains, manufacturing processes, 
and 2026 IPCC/GHG Protocol standards.

OBJECTIVE:
Conduct a rigorous forensic comparison of two carbon footprint reports for the same product.
Identify matches, discrepancies, and potential misreporting.

REPORT 1 - COMPANY CLAIMED DATA:
{company_report}

REPORT 2 - REAL TIME VALIDATED DATA:
{internet_report}

ANALYSIS INSTRUCTIONS:
Step 1 - NORMALIZE: First map both reports to the same lifecycle stages:
         (Mining, Processing, Manufacturing, Assembly, Shipping, Use, End of Life)
         Even if naming differs, match equivalent stages intelligently.

Step 2 - COMPARE: For each matched stage compare:
         - Company claimed kg CO2e vs Real validated kg CO2e
         - Calculate absolute difference and percentage difference
         - Flag if difference > 10% as [DISCREPANCY]
         - Flag if difference > 25% as [SERIOUS MISREPORTING]

Step 3 - PATTERN ANALYSIS:
         - Is underreporting consistent across all stages or specific stages only?
         - Are any stages conveniently missing from company report?
         - Does total claimed vs total real make sense?

OUTPUT FORMAT:

FORENSIC COMPARISON REPORT
===========================

STAGE BY STAGE ANALYSIS:
| Stage | Company Claimed | Real Validated | Difference | Status |
(fill table for each stage)

MISSING STAGES:
- List any stages present in real report but absent in company report

DISCREPANCY ANALYSIS:
- Accurate stages
- Suspicious stages
- Misreported stages

TOTAL CARBON FOOTPRINT:
- Company claimed total: X kg CO2e
- Real validated total: X kg CO2e
- Overall difference: X kg CO2e (X%)

FINAL VERDICT:
[ HONEST | UNDERSTATED | SIGNIFICANTLY MISREPORTED | FRAUDULENT ]
- Reasoning
- Which stages were most misreported
- Confidence level of this analysis

STRICT RULES:
- Only use provided reports, zero outside information
- If data is missing from either report, clearly state Data Not Available
- If company report lacks stage-wise breakdown, flag as [NOT DISCLOSED BY COMPANY]
- Treat non-disclosure of stage data as suspicious and mention it in final verdict
- Be mathematically precise in all calculations
- Confidence level must reflect data quality""",
    input_variables=["company_report", "internet_report"]
)

def comparison_agent(company_report: str, internet_report: str) -> str:
    chain = prompt | model | parser
    result = chain.invoke({
        "company_report": company_report,
        "internet_report": internet_report
    })

    with open("comparison_report.txt", "w") as f:
        f.write(result)

    return result