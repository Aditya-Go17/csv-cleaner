# modules/profiling.py

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def calculate_health_score(df):
    """
    Calculate overall dataset health score
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    # Calculate score
    missing_penalty = (missing_cells / total_cells) * 100
    duplicate_penalty = (duplicate_rows / len(df)) * 100
    
    health_score = 100 - missing_penalty - duplicate_penalty
    health_score = round(max(0, health_score), 1)
    
    return health_score

def show_profile(df):
    """
    Show visual data health summary
    """
    
    health_score = calculate_health_score(df)
    
    # Health score color
    if health_score >= 80:
        color = "🟢"
    elif health_score >= 50:
        color = "🟡"
    else:
        color = "🔴"
    
    # Show health score
    st.subheader("📊 Dataset Health Report")
    
    st.markdown(f"""
    ### {color} Dataset is {health_score}% Healthy
    """)
    
    # Progress bar
    st.progress(health_score / 100)
    
    st.write("---")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📏 Total Rows", len(df))
    col2.metric("📋 Total Columns", len(df.columns))
    col3.metric("🔴 Missing Values", df.isnull().sum().sum())
    col4.metric("🔴 Duplicate Rows", df.duplicated().sum())
    
    st.write("---")
    
    # Column by column report
    st.subheader("📋 Column Health Report:")
    
    column_report = []
    
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = round((missing_count / len(df)) * 100, 1)
        
        # Detect outliers for numeric columns
        outliers = 0
        if df[col].dtype in ['int64', 'float64']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = len(df[col][
                (df[col] < Q1 - 1.5 * IQR) |
                (df[col] > Q3 + 1.5 * IQR)
            ])
        
        column_report.append({
            "Column": col,
            "Data Type": str(df[col].dtype),
            "Missing (%)": f"{missing_pct}%",
            "Outliers": outliers,
            "Unique Values": df[col].nunique()
        })
    
    report_df = pd.DataFrame(column_report)
    st.dataframe(report_df, use_container_width=True)
    
    st.write("---")
    
    # Missing values chart
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    
    if len(missing) > 0:
        st.subheader("🔴 Missing Values Chart:")
        fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={"x": "Columns", "y": "Missing Count"},
            color=missing.values,
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    return health_score

def schema_check(df):
    """
    Let user confirm/change data types
    """
    
    st.subheader("🔍 Confirm Data Types:")
    st.write("Check if data types are correct:")
    
    new_types = {}
    cols = st.columns(3)
    
    for i, col in enumerate(df.columns):
        with cols[i % 3]:
            current_type = str(df[col].dtype)
            
            new_type = st.selectbox(
                f"{col}",
                ["Auto", "Text", "Number",
                 "Datetime", "Boolean"],
                key=f"type_{col}"
            )
            new_types[col] = new_type
    
    # Apply type changes
    if st.button("✅ Confirm Data Types"):
        for col, dtype in new_types.items():
            try:
                if dtype == "Text":
                    df[col] = df[col].astype(str)
                elif dtype == "Number":
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif dtype == "Datetime":
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                elif dtype == "Boolean":
                    df[col] = df[col].astype(bool)
            except:
                pass
        st.success("✅ Data types updated!")
    
    return df
