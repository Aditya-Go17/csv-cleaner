# modules/cleaning.py

import pandas as pd
import numpy as np
import dateparser
import streamlit as st

def clean_data(df, options):
    """
    Apply all cleaning operations
    based on user selected options
    """
    
    clean_df = df.copy()
    report = []
    
    # ─────────────────────────────
    # 1. Remove Duplicates
    # ─────────────────────────────
    if options["remove_duplicates"]:
        before = len(clean_df)
        clean_df = clean_df.drop_duplicates()
        removed = before - len(clean_df)
        report.append(f"🗑️ Removed {removed} duplicate rows")
    
    # ─────────────────────────────
    # 2. Missing Value Resolution
    # ─────────────────────────────
    if options["missing_strategy"] == "Impute Median (Numerical)":
        numeric_cols = clean_df.select_dtypes(
            include='number'
        ).columns
        for col in numeric_cols:
            median_val = clean_df[col].median()
            filled = clean_df[col].isnull().sum()
            clean_df[col] = clean_df[col].fillna(median_val)
            if filled > 0:
                report.append(
                    f"📊 Column '{col}': filled {filled} "
                    f"missing with median ({median_val:.2f})"
                )
    
    elif options["missing_strategy"] == "Impute Mode (Categorical)":
        cat_cols = clean_df.select_dtypes(
            include='object'
        ).columns
        for col in cat_cols:
            mode_val = clean_df[col].mode()[0]
            filled = clean_df[col].isnull().sum()
            clean_df[col] = clean_df[col].fillna(mode_val)
            if filled > 0:
                report.append(
                    f"📝 Column '{col}': filled {filled} "
                    f"missing with mode ('{mode_val}')"
                )
    
    elif options["missing_strategy"] == "Drop Missing Rows":
        before = len(clean_df)
        clean_df = clean_df.dropna()
        removed = before - len(clean_df)
        report.append(f"🗑️ Dropped {removed} rows with missing values")
    
    # ─────────────────────────────
    # 3. Outlier Clipping (IQR)
    # ─────────────────────────────
    if options["clip_outliers"]:
        numeric_cols = clean_df.select_dtypes(
            include='number'
        ).columns
        for col in numeric_cols:
            Q1 = clean_df[col].quantile(0.25)
            Q3 = clean_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = len(clean_df[col][
                (clean_df[col] < lower) |
                (clean_df[col] > upper)
            ])
            
            clean_df[col] = clean_df[col].clip(lower, upper)
            
            if outliers > 0:
                report.append(
                    f"✂️ Column '{col}': clipped {outliers} outliers"
                )
    
    # ─────────────────────────────
    # 4. Text Sanitation
    # ─────────────────────────────
    if options["text_clean"]:
        str_cols = clean_df.select_dtypes(include='object').columns
        for col in str_cols:
            # Remove extra spaces
            clean_df[col] = clean_df[col].str.strip()
            # Remove special characters
            clean_df[col] = clean_df[col].str.replace(
                r'[^\w\s]', '', regex=True
            )
        report.append("✅ Text columns sanitized")
    
    if options["text_case"] == "lowercase":
        str_cols = clean_df.select_dtypes(include='object').columns
        clean_df[str_cols] = clean_df[str_cols].apply(
            lambda x: x.str.lower()
        )
        report.append("✅ Text converted to lowercase")
        
    elif options["text_case"] == "UPPERCASE":
        str_cols = clean_df.select_dtypes(include='object').columns
        clean_df[str_cols] = clean_df[str_cols].apply(
            lambda x: x.str.upper()
        )
        report.append("✅ Text converted to UPPERCASE")
    
    # ─────────────────────────────
    # 5. Date Standardizer
    # ─────────────────────────────
    if options["standardize_dates"]:
        for col in clean_df.columns:
            if "date" in col.lower() or \
               "time" in col.lower():
                try:
                    clean_df[col] = pd.to_datetime(
                        clean_df[col],
                        infer_datetime_format=True,
                        errors='coerce'
                    ).dt.strftime('%Y-%m-%d')
                    report.append(
                        f"📅 Column '{col}': dates standardized "
                        f"to ISO format (YYYY-MM-DD)"
                    )
                except:
                    pass
    
    return clean_df, report
