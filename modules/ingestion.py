# modules/ingestion.py

import pandas as pd
import pyarrow as pa
import json
import streamlit as st

def load_file(uploaded_file):
    """
    Detects file format automatically
    and loads into pandas DataFrame
    """
    
    file_name = uploaded_file.name
    
    try:
        # Detect format automatically
        if file_name.endswith(".csv"):
            df = pd.read_csv(
                uploaded_file,
                engine="pyarrow"    # High performance
            )
            file_type = "CSV"
            
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(
                uploaded_file,
                engine="openpyxl"
            )
            file_type = "Excel"
            
        elif file_name.endswith(".json"):
            data = json.load(uploaded_file)
            df = pd.json_normalize(data)  # Flatten JSON
            file_type = "JSON"
            
        else:
            st.error("❌ Unsupported file format!")
            return None, None
            
        return df, file_type
        
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None, None
