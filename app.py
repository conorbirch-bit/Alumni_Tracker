import os
import tempfile

import pandas as pd
import streamlit as st

from main_fixed import run_alumni_agent


st.set_page_config(
    page_title="AI Survey Project Assistant",
    page_icon="📋",
    layout="wide",
)

st.title("AI Survey Project Assistant")

st.write(
    "Upload a survey tracker, validate the data and generate "
    "an AI-assisted daily project report."
)

uploaded_file = st.file_uploader(
    "Choose a survey tracker",
    type=["xlsx"],
)

if uploaded_file is not None:
    try:
        preview_df = pd.read_excel(uploaded_file)

        st.subheader("Spreadsheet preview")
        st.dataframe(
            preview_df,
            width="stretch",
            hide_index=True,
        )

        if st.button(
            "Run survey analysis",
            type="primary",
        ):
            with st.spinner("Validating data and generating report..."):
                temporary_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".xlsx",
                    ) as temporary_file:
                        temporary_file.write(uploaded_file.getbuffer())
                        temporary_path = temporary_file.name

                    result = run_alumni_agent(temporary_path)

                finally:
                    if (
                        temporary_path
                        and os.path.exists(temporary_path)
                    ):
                        os.remove(temporary_path)

            st.subheader("Analysis result")

            if result.get("has_critical_errors"):
                st.error("Critical data-quality issues detected.")
            else:
                st.success("Analysis completed successfully.")

                metric_columns = st.columns(4)

                metric_columns[0].metric(
                    "Total alumni",
                    result.get("total_alumni", result.get("total_surveys", 0)),
                )

                metric_columns[1].metric(
                    "Contacted",
                    result.get("contacted", 0),
                )

                metric_columns[2].metric(
                    "Uploaded",
                    result.get("uploaded", 0),
                )

                metric_columns[3].metric(
                    "AI completion",
                    f"{result.get('ai_completion', 0)}%",
                )

            st.subheader("Daily report")
            st.markdown(result["final_report"])

            st.download_button(
                label="Download report",
                data=result["final_report"],
                file_name="alumni_report.txt",
                mime="text/plain",
            )

    except Exception as error:
        st.error(f"Unable to process the spreadsheet: {error}")

else:
    st.info("Upload an Excel survey tracker to begin.")