"""Streamlit interface for the Alumni Tracker analysis workflow."""

import os
import tempfile

import pandas as pd
import streamlit as st

from main import run_alumni_agent

st.set_page_config(page_title="Alumni Tracker Assistant", page_icon="🎓", layout="wide")
st.title("Alumni Tracker Assistant")
st.write(
    "Upload your alumni networking tracker to review your contacts and "
    "generate an AI-assisted outreach report."
)

uploaded_file = st.file_uploader("Choose an alumni tracker", type=["xlsx"])

if uploaded_file is None:
    st.info("Upload an Excel alumni tracker to begin.")
else:
    try:
        preview_df = pd.read_excel(uploaded_file)
        required_columns = {"Company", "Studied"}
        missing = required_columns - set(preview_df.columns)
        if missing:
            st.error("Missing required columns: " + ", ".join(sorted(missing)))
        else:
            st.subheader("Alumni tracker preview")
            st.dataframe(preview_df, use_container_width=True, hide_index=True)

            if st.button("Generate alumni analysis", type="primary"):
                with st.spinner("Analysing your alumni tracker..."):
                    temporary_path = None
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                            temp_file.write(uploaded_file.getbuffer())
                            temporary_path = temp_file.name
                        result = run_alumni_agent(temporary_path)
                    finally:
                        if temporary_path and os.path.exists(temporary_path):
                            os.remove(temporary_path)

                st.success("Analysis completed successfully.")
                metric_columns = st.columns(3)
                metric_columns[0].metric("Total alumni", result["total_alumni"])
                metric_columns[1].metric("Companies represented", len(result["company_counts"]))
                metric_columns[2].metric("Subjects represented", len(result["studied_counts"]))

                st.subheader("AI-assisted networking report")
                st.markdown(result["final_report"])
                st.download_button(
                    "Download report",
                    data=result["final_report"],
                    file_name="alumni_report.txt",
                    mime="text/plain",
                )
    except Exception as error:
        st.error(f"Unable to process the spreadsheet: {error}")
