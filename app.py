import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="SignalAI V2 - Customer Radar", page_icon="📡", layout="wide")
st.title("📡 SignalAI V2")
st.caption("Auto-track where your customers are talking")

# Session state for saved searches
if 'searches' not in st.session_state:
    st.session_state.searches = ["phone cases", "hair oil"]

col1, col2 = st.columns(2)
with col1:
    product = st.text_input("What do you sell?", placeholder="gadgets, cakes")
with col2:
    city = st.text_input("Your city", value="Port Harcourt")

# Save search button
if st.button("💾 Save this search"):
    if product and product not in st.session_state.searches:
        st.session_state.searches.append(product)
        st.success(f"Saved: {product}")

# Scan button
if st.button("🔍 Scan for Customers NOW"):
    if product and city:
        query = f'"{product}" ("buy" OR "price" OR "need" OR "recommend") {city}'
        x_url = f"https://nitter.net/search?q={query.replace(' ', '+')}"
        
        st.success(f"Scanning X for '{product}' in {city}...")
        
        # Show X link + embedded results
        st.markdown(f"[🎯 Open full results on X →](https://twitter.com/search?q={query.replace(' ', '%20')})")
        
        st.markdown("---")
        st.subheader("Top customer posts found:")
        
        # Note: X blocks scraping, so we show smart preview + link
        st.info("X blocks direct scraping. Click link above for live posts. V3 will use API.")
        
        st.markdown(f"""
        **How to use this:**
        1. Click link above 
        2. Filter by "Latest" 
        3. Reply: "I sell {product} in {city}. DM me" 
        4. Convert to sales
        """)
    else:
        st.warning("Enter product + city first")

st.markdown("---")
st.subheader("💾 Your Saved Searches")
for i, s in enumerate(st.session_state.searches):
    if st.button(f"Scan {s}", key=i):
        st.session_state.last_search = s
        st.rerun()

st.markdown("---")
st.subheader("📱 WhatsApp Alerts V1")
phone = st.text_input("Your WhatsApp number", placeholder="2348012345678")
if st.button("Send test alert to WhatsApp"):
    if phone:
        msg = f"SignalAI Alert: New customer posted about '{product}' in {city} just now!"
        wa_link = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
        st.markdown(f"[Click to send alert →]({wa_link})")
    else:
        st.warning("Enter WhatsApp number")

st.caption("V2: Auto-scan + Save searches. V3: Real API + Map pins + Auto alerts")
