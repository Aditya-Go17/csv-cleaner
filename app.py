# app.py

import streamlit as st
from modules.ingestion import load_file
from modules.profiling import show_profile, schema_check
from modules.cleaning import clean_data
from modules.export import show_export_options

st.set_page_config(
    page_title="SmartClean",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 SmartClean")
st.write("Professional Data Cleaning Tool")
st.write("---")

# ─────────────────────────────
# STEP 1: Upload
# ─────────────────────────────
st.subheader("Step 1: Upload Your File")
st.write("Supports: CSV, Excel, JSON")

uploaded_file = st.file_uploader(
    "📂 Drag and drop file here",
    type=["csv", "xlsx", "json"]
)

if uploaded_file is not None:

    df, file_type = load_file(uploaded_file)
    
    if df is not None:
        st.success(
            f"✅ {file_type} file loaded! "
            f"({len(df)} rows, {len(df.columns)} columns)"
        )
        st.write("---")
        
        # ─────────────────────────────
        # STEP 2: Auto Profiling
        # ─────────────────────────────
        st.subheader("Step 2: Data Health Check")
        health_score = show_profile(df)
        df = schema_check(df)
        st.write("---")
        
        # ─────────────────────────────
        # STEP 3: Clean Options
        # ─────────────────────────────
        st.subheader("Step 3: Choose Cleaning Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            remove_duplicates = st.toggle(
                "🗑️ Remove Duplicate Rows",
                value=True
            )
            
            missing_strategy = st.radio(
                "Handle Missing Values:",
                ["Impute Median (Numerical)",
                 "Impute Mode (Categorical)",
                 "Drop Missing Rows",
                 "Keep As Is"]
            )
            
            clip_outliers = st.toggle(
                "✂️ Clip Outliers (IQR Method)",
                value=True
            )
        
        with col2:
            text_clean = st.toggle(
                "✅ Text Sanitation",
                value=True
            )
            
            text_case = st.radio(
                "Text Case:",
                ["Keep Original",
                 "lowercase",
                 "UPPERCASE"]
            )
            
            standardize_dates = st.toggle(
                "📅 Standardize Date Format",
                value=True
            )
        
        st.write("---")
        
        # Clean button
        if st.button(
            "🚀 Start Cleaning",
            use_container_width=True
        ):
            with st.spinner("Cleaning your data..."):
                
                options = {
                    "remove_duplicates": remove_duplicates,
                    "missing_strategy": missing_strategy,
                    "clip_outliers": clip_outliers,
                    "text_clean": text_clean,
                    "text_case": text_case,
                    "standardize_dates": standardize_dates
                }
                
                clean_df, report = clean_data(df, options)
            
            st.success("✅ Cleaning Complete!")
            
            # Show report
            st.subheader("📋 Cleaning Report:")
            for item in report:
                st.write(item)
            
            st.write("---")
            
            # After metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Rows", len(clean_df))
            col2.metric("Total Columns", len(clean_df.columns))
            col3.metric("🟢 Missing Values",
                       clean_df.isnull().sum().sum())
            col4.metric("🟢 Duplicates",
                       clean_df.duplicated().sum())
            
            st.write("---")
            
            # ─────────────────────────────
            # STEP 4: Export
            # ─────────────────────────────
            st.subheader("Step 4: Download Clean Data")
            show_export_options(
            original_df=df,          # original data
            clean_df=clean_df,       # cleaned data
            health_score=health_score,
            cleaning_report=report,
            file_name=uploaded_file.name
            )
            
            st.balloons()
