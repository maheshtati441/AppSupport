import pandas as pd
import streamlit as st
from logging_setup import logger

def load_data(file):
    """Load data from an uploaded Excel file."""
    try:
        df = pd.read_excel(file)
        logger.info("Excel file loaded successfully.")
        return df
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        st.error("Failed to load the Excel file.")
        return None
