import streamlit as st
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="SignalAI - Customer Radar", page_icon="📡", layout="wide", initial_sidebar_state="collapsed")

# GOLD + BLACK + WHITE BALANCED THEME
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);}
    .main {background: #ffffff; padding: 2.5rem; border-radius: 20px; margin: 1rem; 
           border: 2px solid #FFD700; box-shadow: 0 8px 32px rgba(0,0,0,0.1);}
    .stMarkdown, .stText, label {color: #333 !important;}
    .stButton>button {background: linear-gradient(90deg, #1a1a1a 0%, #000 100%); 
                      color: #FFD700; border-radius: 12px; border: 2px solid #FFD700; 
                      font-weight: 700; padding: 0.7rem 1.5rem; font-size: 16px;
                      transition: 0.3s;}
    .stButton>button:hover {background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%); 
                            color: #000; transform: translateY(-2px); 
                            box-shadow: 0 6px 20px rgba(255,215,0,0.4);}
    .stTextInput>div>div>input {background-color: #fafafa; color: #1a1a1a; 
                                border-radius: 10px; border: 2px solid #ddd;}
    .stTextInput>div>div>input:focus {border: 2px solid #FFD700;}
    .stInfo {background-color: #fff9e6; border-left: 4px solid #FFD700; color: #333;}
    .stSuccess {background-color: #e8f5e9; border-left: 4px solid #4caf50; color: #1a1a1a;}
    .footer {text-align: center; color: #666; margin-top: 2rem; font-weight: 600; font-size: 14px;}
    .footer span {color: #FFD700; font-weight: 800;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

# LOGO AT TOP - CENTER IT
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=250)

st.markdown("---")

# NO MORE st.title() WITH HTML - FIXED
st.markdown("### **Find customers talking about your product**")
st.caption("*Customer radar for Nigerian vendors*")

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
st.markdown(f'<div class="footer">© {year} <span>@signalai</span>. All rights reserved. Made for Nigerian vendors 🇳🇬</div>', unsafe_allow_html=True)
