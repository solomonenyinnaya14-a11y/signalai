import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="SignalAI - Customer Radar", page_icon="📡", layout="wide")

# GOLD + BLACK LUXURY THEME
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #000 0%, #1a1a1a 100%);}
    .main {background: linear-gradient(180deg, #0a0a0a 0%, #000 100%); 
           padding: 2rem; border-radius: 20px; margin: 1rem; 
           border: 2px solid #FFD700; box-shadow: 0 0 30px rgba(255,215,0,0.3);}
    h1 {color: #FFD700; font-weight: 900; text-shadow: 0 0 20px rgba(255,215,0,0.5);}
    .stMarkdown, .stText {color: #FFD700 !important;}
    .stButton>button {background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%); 
                      color: #000; border-radius: 12px; border: 2px solid #FFD700; 
                      font-weight: 800; padding: 0.7rem 1.5rem; font-size: 16px;
                      transition: 0.3s; box-shadow: 0 4px 15px rgba(255,215,0,0.4);}
    .stButton>button:hover {transform: scale(1.05); box-shadow: 0 0 25px rgba(255,215,0,0.8);}
    .stTextInput>div>div>input {background-color: #1a1a1a; color: #FFD700; 
                                border-radius: 10px; border: 2px solid #FFD700;}
    .stInfo {background-color: #1a1a1a; border-left: 4px solid #FFD700; color: #FFD700;}
    .stSuccess {background-color: #1a1a1a; border-left: 4px solid #00FF00; color: #FFD700;}
    .footer {text-align: center; color: #FFD700; margin-top: 2rem; font-weight: 700; font-size: 14px;}
    a {color: #FFD700 !important; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("📡 SignalAI")
st.markdown("**Find customers talking about your product** | *Customer radar for Nigerian vendors*")

# Session state for saved searches
if 'searches' not in st.session_state:
    st.session_state.searches = ["phone cases", "hair oil"]

col1, col2 = st.columns(2)
with col1:
    product = st.text_input("🎯 What do you sell?", placeholder="clothes, cakes, gadgets")
with col2:
    city = st.text_input("📍 Your city", value="Port Harcourt")

# Save search button
if st.button("💾 Save this search"):
    if product and product not in st.session_state.searches:
        st.session_state.searches.append(product)
        st.success(f"✅ Saved: {product}")

# Scan button
if st.button("🔍 Scan for Customers"):
    if product and city:
        query = f'"{product}" ("buy" OR "price" OR "need" OR "recommend") {city}'
        
        x_query = urllib.parse.quote(query)
        x_url = f"https://twitter.com/search?q={x_query}&src=typed_query&f=live"
        
        fb_query = urllib.parse.quote(f'{product} {city}')
        fb_marketplace = f"https://www.facebook.com/marketplace/search/?query={fb_query}"
        fb_groups = f"https://www.facebook.com/search/top/?q={fb_query}"
        
        st.success(f"🚀 Scanning for '{product}' in {city}...")
        
        st.markdown("### 📊 Open customer conversations:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[🐦 **X/Twitter**]({x_url})")
        with col2:
            st.markdown(f"[📘 **Facebook Marketplace**]({fb_marketplace})")
        
        st.markdown(f"[👥 **Facebook Groups**]({fb_groups})")
        
        st.markdown("---")
        st.subheader("🔥 Top customer posts found:")
        st.info("💡 X + Facebook block direct scraping. Click links above → Filter by 'Latest' → Reply: 'I sell {product} in {city}. DM me'")
        
    else:
        st.warning("⚠️ Enter product + city first")

st.markdown("---")
st.subheader("💾 Your Saved Searches")
for i, s in enumerate(st.session_state.searches):
    if st.button(f"⚡ Scan {s}", key=i):
        st.session_state.last_search = s
        st.rerun()

st.markdown("---")
st.subheader("📱 WhatsApp Alerts")
phone = st.text_input("Your WhatsApp number", placeholder="2347067149516", help="Use 234 + your number, no 0")

if st.button("📲 Send test alert to WhatsApp"):
    if phone:
        phone = phone.strip().replace(" ", "")
        if phone.startswith("0"):
            phone = "234" + phone[1:]
        elif not phone.startswith("234"):
            phone = "234" + phone
            
        msg = f"SignalAI Alert: New customer posted about '{product}' in {city} just now!"
        wa_link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        st.markdown(f"[👉 Click to send alert →]({wa_link})")
        st.success(f"📤 Sending to +{phone}")
    else:
        st.warning("Enter WhatsApp number")

st.markdown('</div>', unsafe_allow_html=True)

# COPYRIGHT FOOTER
year = datetime.now().year
st.markdown(f'<div class="footer">© {year} @signalai. All rights reserved. Made for Nigerian vendors 🇳🇬</div>', unsafe_allow_html=True)
