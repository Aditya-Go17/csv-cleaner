# modules/export.py

import pandas as pd
import streamlit as st
import io
from modules.report import (
    generate_pdf_report,
    generate_excel_report
)

def show_export_options(
    original_df,
    clean_df,
    health_score,
    cleaning_report,
    file_name
):
    
    st.subheader("📤 Export Your Clean Data:")
    
    # ─────────────────────────────
    # Data Downloads
    # ─────────────────────────────
    st.write("### 📊 Download Clean Data:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("📊 CSV File")
        st.write("Best for: Excel, Power BI")
        st.download_button(
            label="⬇️ Download CSV",
            data=clean_df.to_csv(index=False),
            file_name="clean_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.write("📗 Excel File")
        st.write("Best for: Reporting")
        buffer = io.BytesIO()
        with pd.ExcelWriter(
            buffer, engine='openpyxl'
        ) as writer:
            clean_df.to_excel(writer, index=False)
        st.download_button(
            label="⬇️ Download Excel",
            data=buffer.getvalue(),
            file_name="clean_data.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    
    with col3:
        st.write("⚡ Parquet File")
        st.write("Best for: ML Training")
        buffer = io.BytesIO()
        clean_df.to_parquet(buffer, index=False)
        st.download_button(
            label="⬇️ Download Parquet",
            data=buffer.getvalue(),
            file_name="clean_data.parquet",
            mime="application/octet-stream",
            use_container_width=True
        )
    
    st.write("---")
    
    # ─────────────────────────────
    # Report Downloads
    # ─────────────────────────────
    st.write("### 📋 Download Cleaning Report:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📄 PDF Report")
        st.write("Professional cleaning summary")
        
        pdf_data = generate_pdf_report(
            original_df,
            clean_df,
            health_score,
            cleaning_report,
            file_name
        )
        
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_data,
            file_name="cleaning_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    with col2:
        st.write("📗 Excel Report")
        st.write("Detailed cleaning report")
        
        excel_data = generate_excel_report(
            original_df,
            clean_df,
            health_score,
            cleaning_report,
            file_name
        )
        
        st.download_button(
            label="⬇️ Download Excel Report",
            data=excel_data,
            file_name="cleaning_report.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
