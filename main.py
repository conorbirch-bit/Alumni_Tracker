from typing_extensions import TypedDict

import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


# This defines all the information passed between the workflow steps.
class AlumniState(TypedDict, total=False):
    tracker_path: str
    total_alumni: int
    company_counts: pd.Series
    studied_counts: pd.Series
    final_report: str


def analyse_tracker(state: AlumniState) -> dict:
    """Read Excel and calculate reliable project metrics using Python."""

    df = pd.read_excel(state["tracker_path"])

    total_alumni = len(df)
    company_counts = df["Company"].value_counts()
    studied_counts = df["Studied"].value_counts()

    return {
        "total_alumni": total_alumni,
        "company_counts": company_counts,
        "studied_counts": studied_counts,
    }



# def route_after_validation(state: SurveyState) -> str:
#     """Choose the next node based on validation results."""

#     if state["has_critical_errors"]:
#         return "write_data_warning"

#     return "analyse_tracker"

def write_report(state: AlumniState) -> dict:
    """Use the LLM to interpret the Python-calculated metrics."""

    project_data = f"""
PROJECT KPIs

Total alumni: {state["total_alumni"]}
Company counts: {state["company_counts"].to_string()}
Studied counts: {state["studied_counts"].to_string()}
"""

    prompt = f"""
You are an assistant supporting a graduate from Newcastle University who studied Mechanical Engineering.

He has identified a database of alumni to reach out to for advice and help in job applicaions.
asset-recognition implementation.

The graduate wants has a year experience as an engineering consultant and wants to transition into mangement consulting.

Advise the graduate who is best to contact next and how to approach them.

Base this off of seniority, study area similarity, and try to keep variety in companies looking at of who has already been contacted.


Include:

1. Executive summary
2. Key KPIs
3. Advice on who to contact next and how to approach them
4. Advice on who to be targetting to improve the alumni database for future outreach

Do not invent facts.
Do not include placeholders.

Project data:

{project_data}
"""

    response = llm.invoke(prompt)

    return {"final_report": response.content}


# Build the graph.
builder = StateGraph(AlumniState)

builder.add_node("analyse_tracker", analyse_tracker)
builder.add_node("write_report", write_report)

builder.add_edge(START, "analyse_tracker")
builder.add_edge("analyse_tracker", "write_report")
builder.add_edge("write_report", END)

alumni_agent = builder.compile()


# Run the graph.
def run_alumni_agent(tracker_path: str) -> dict:
    """Run the LangGraph workflow and return the complete result."""

    return alumni_agent.invoke(
        {"tracker_path": tracker_path}
    )


if __name__ == "__main__":
    result = run_alumni_agent("data/Alumni_Tracker.xlsx")

    print("\n----- AI DAILY REPORT -----\n")
    print(result["final_report"])