import pandas as pd
import streamlit as st
from craigslist_scan import scan_craigslist
from reddit_scan import scan_reddit
from master_scan import scan_all
from extra_scan import scan_extra


st.set_page_config(page_title="DFW Tree Lead Radar", layout="wide")

st.title("🌳 DFW Arborist Lead Radar")

st.write("Scanning Reddit + Craigslist for tree work leads...")

if st.button("Scan Now"):
    leads = []
    leads += scan_all()       # reddit + google
    leads += scan_craigslist()
    leads += scan_extra()

    if not leads:
        st.warning("No leads found right now.")
    else:
        df = pd.DataFrame(leads)
        df = df.sort_values(by="score", ascending=False)

        st.success(f"Found {len(df)} possible leads")
        st.dataframe(df, use_container_width=True)
    
        
