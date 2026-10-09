# Alumni Tracker — AI-Assisted Networking Analysis

A Python project that analyses an Excel-based alumni networking tracker and uses an OpenAI language model to produce a structured outreach strategy. Built to support a graduate exploring opportunities in management consulting and related roles.

The project combines **deterministic data analysis** with **AI-generated recommendations**: Pandas calculates summary statistics, while a LangGraph workflow passes those results to an LLM to interpret networking coverage and suggest where to focus next.

## Why I built it

Reaching out to university alumni can be a useful way to learn about industries, roles and recruitment processes. As a networking list grows, it becomes harder to see which companies and academic backgrounds are represented and where outreach could be more varied.

This project explores how a simple spreadsheet and an AI-assisted reporting workflow can make that process more structured.

## What it does

- Reads an alumni tracker from an Excel (`.xlsx`) file.
- Calculates the total number of alumni in the tracker.
- Summarises contacts by **company** and **subject studied**.
- Passes the calculated metrics to an OpenAI model for a written report.
- Requests an executive summary, key KPIs, outreach advice and suggestions for expanding the database.
- Provides a Streamlit interface for uploading and previewing a spreadsheet, viewing the report and downloading it as a text file.

**Current scope:** The AI receives aggregate counts, not the individual alumni rows. It can therefore comment on the overall composition of the tracker, but it cannot reliably identify or rank specific people to contact next. The source spreadsheet also contains a `Contacted` column, but the current analysis does not calculate contact-status metrics from it.

## Technology

| Tool | Purpose |
| --- | --- |
| Python | Application and analysis logic |
| Pandas | Excel ingestion and summary statistics |
| LangGraph | Orchestrating the analysis and reporting steps |
| LangChain OpenAI | Calling the language model (`gpt-4o-mini` in the supplied code) |
| Streamlit | Spreadsheet upload, preview and report interface |
| python-dotenv | Loading local environment variables |
| OpenPyXL | Excel file support for Pandas |

## How it works

```text
Excel alumni tracker
        |
        v
Pandas: read spreadsheet
        |
        v
Calculate total alumni,
company counts and degree counts
        |
        v
LangGraph: pass metrics to LLM
        |
        v
AI-generated networking report
        |
        v
Streamlit display / TXT download
```

The LangGraph workflow has two nodes:

1. **`analyse_tracker`** — loads the spreadsheet and calculates metrics using Pandas.
2. **`write_report`** — supplies those metrics to the OpenAI model and returns a written report.

This separation keeps numerical calculations in Python rather than relying on the LLM to count spreadsheet records.

## Input data

The supplied example workbook (`Alumni_Tracker.xlsx`) contains these columns:

| Column | Description |
| --- | --- |
| `Name` | Alumni contact name |
| `Company` | Organisation |
| `Role` | Job title or role |
| `Studied` | Subject studied |
| `Alumni` | University |
| `Linkedin` | LinkedIn reference |
| `Contacted` | Outreach date or contact status |

Only `Company` and `Studied` are explicitly accessed by the current analysis; the total is calculated from the number of rows. The remaining columns provide useful scope for future development.

**Privacy:** A real networking tracker may contain personal information. Use anonymised sample data in a public repository, and do not commit private contact lists or API keys.

## Running the project

### 1. Install dependencies

```bash
pip install pandas openpyxl python-dotenv langchain-openai langgraph streamlit
```

### 2. Configure the OpenAI API key

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Keep `.env` out of version control (add it to `.gitignore`). API usage may incur costs.

### 3. Run the analysis from the command line

The supplied `main.py` expects the workbook at `data/Alumni_Tracker.xlsx`:

```text
project/
├── main.py
├── app.py
├── data/
│   └── Alumni_Tracker.xlsx
└── .env
```

Then run:

```bash
python main.py
```

### 4. Run the Streamlit interface

```bash
streamlit run app.py
```

Upload an `.xlsx` file, review the spreadsheet preview, and run the analysis to generate a downloadable text report.

**Integration note:** The uploaded Streamlit script is named `app (2).py` and imports `run_alumni_agent` from `main_fixed`, while the supplied workflow is in `main.py`. Before launching the interface, rename the UI script to `app.py` and change its import to:

```python
from main import run_alumni_agent
```

The interface also retains some survey-project labels and placeholder metrics (`Contacted`, `Uploaded`, `AI completion`) that are not currently returned by the alumni workflow. Those labels and metrics should be updated or removed before presenting the app as a finished alumni dashboard.

## Limitations and next steps

- **Individual prioritisation:** Pass relevant alumni-level records into a structured ranking stage so the tool can suggest specific contacts based on role, company, academic background and previous outreach.
- **Outreach tracking:** Calculate contacted/not-contacted counts and follow-up activity from the `Contacted` field.
- **Data validation:** Check required columns, missing values and duplicate records before analysis.
- **Dashboard consistency:** Replace leftover survey-specific UI text and metrics with alumni-focused information.
- **Explainable recommendations:** Show why a particular contact or company has been prioritised, with references to the input data.
- **Privacy safeguards:** Use synthetic sample records and limit the personal data sent to an external model.

## Project status

**Prototype.** The core LangGraph analysis-and-reporting workflow is implemented. The Streamlit interface is present but needs the integration and labelling updates described above. This repository demonstrates an early approach to combining conventional data analysis with LLM-generated business recommendations.
