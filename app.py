import streamlit as st
from data_loader import load_data
from issue_search import search_similar_issues, generate_ai_response
from logging_setup import logger

def main():
    """Main Streamlit application."""
    st.title("AI-Driven Technical Support")
    logger.info("Application started.")

    # File Upload
    uploaded_file = st.file_uploader("Upload an Excel file with 'Issue' and 'Resolution' columns", type=["xls", "xlsx"])

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.write("Data Loaded Successfully!")
            st.dataframe(df.head())

        # User input
        issue_description = st.text_area("Describe the issue:")

        if st.button("Submit"):
            if issue_description:
                logger.info(f"User submitted issue: {issue_description}")
                results = search_similar_issues(df, issue_description)

                if results:
                    st.write("Existing Issues and Resolutions:")
                    for record in results:
                        st.write(f"**Issue:** {record['Issue']}")
                        st.write(f"**Resolution:** {record['Resolution']}")
                        st.write("---")
                else:
                    ai_response = generate_ai_response(issue_description)
                    st.write("Generated Resolution:")
                    st.write(ai_response)
            else:
                logger.warning("User submitted an empty issue description.")
                st.write("Please enter a description of the issue.")

if __name__ == "__main__":
    main()
