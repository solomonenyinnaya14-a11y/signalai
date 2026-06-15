import streamlit as st
import urllib.parse

st.set_page_config(page_title="SignalAI V2 - Customer Radar", page_icon="📡", layout="wide")
st.title("📡 SignalAI V2")
st.caption("Auto-track where your customers are talking: X + Facebook")

# Session state for saved searches
if 'searches' not in st.session_state:
    st.session_state.searches = ["phone cases", "hair oil"]

col1, col2 = st.columns(2)
with col1:
    product = st.text_input("What do you sell?", placeholder="clothes, cakes, gadgets")
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
        
        # X Search Link
        x_query = urllib.parse.quote(query)
        x_url = f"https://twitter.com/search?q={x_query}&src=typed_query&f=live"
        
        # Facebook Marketplace + Groups Search Link
        fb_query = urllib.parse.quote(f'{product} {city}')
        fb_marketplace = f"https://www.facebook.com/marketplace/search/?query={fb_query}"
        fb_groups = f"https://www.facebook.com/search/top/?q={fb_query}&epa=FILTERS"
        
        st.success(f"Scanning X + Facebook for '{product}' in {city}...")
        
        st.markdown("### 🎯 Open Customer Conversations:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[🐦 X/Twitter - Latest posts →]({x_url})")
        with col2:
            st.markdown(f"[📘 Facebook Marketplace →]({fb_marketplace})")
        
        st.markdown(f"[👥 Facebook Groups/Posts →]({fb_groups})")
        
        st.markdown("---")
        st.subheader("How to convert to sales:")
        st.markdown(f"""
        1. **Click X link** → Filter "Latest" → Reply: "I sell {product} in {city}. DM me"
        2. **Click Facebook Marketplace** → See people listing/asking for {product}
        3. **Click Facebook Groups** → Join PH buy/sell groups → Post your offer
        4. **Convert**: First 5 replies = your customers today
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
        wa_link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        st.markdown(f"[Click to send alert →]({wa_link})")
    else:
        st.warning("Enter WhatsApp number")

st.caption("V2.1: X + Facebook scanning. V3: Auto-scrape posts + Map pins")
