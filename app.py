import streamlit as st
import pandas as pd

st.title("CSV File Cleaner")
st.write("Upload your CSV file and get a clean version!")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    
    # Read file
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Original Data Preview")
    st.dataframe(df.head())
    
    # Show problems
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Duplicate Rows", df.duplicated().sum())
    col3.metric("Missing Values", df.isnull().sum().sum())
    
    # Cleaning options
    st.subheader("Cleaning Options")
    remove_duplicates = st.checkbox("Remove Duplicate Rows", value=True)
    remove_missing = st.checkbox("Remove Missing Values", value=True)
    
    if st.button("Clean CSV"):
        
        clean_df = df.copy()
        
        if remove_duplicates:
            clean_df = clean_df.drop_duplicates()
            
        if remove_missing:
            clean_df = clean_df.dropna()
        
        # Show results
        st.subheader("Cleaned Data Preview")
        st.dataframe(clean_df.head())
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", len(clean_df))
        col2.metric("Duplicate Rows", clean_df.duplicated().sum())
        col3.metric("Missing Values", clean_df.isnull().sum().sum())
        
        # Download button
        st.download_button(
            label="⬇️ Download Clean CSV",
            data=clean_df.to_csv(index=False),
            file_name="clean_output.csv",
            mime="text/csv"
        )