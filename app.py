import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="SignalAI - Customer Radar", page_icon="📡", layout="wide", initial_sidebar_state="collapsed")

def success_box(text):
    components.html(f"""
    <div style="
        background-color: #1E90FF;
        border-left: 4px solid #0d6efd;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        color: white;
        font-weight: 700;
        font-size: 16px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    ">
        {text}
    </div>
    """, height=60)

st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #87CEEB 0%, #E0F6FF 100%);}
    .block-container {padding-top: 1rem !important; padding-bottom: 1rem !important;}
    .stMarkdown, .stText, label, h1, h2, h3 {color: #1a1a1a !important;}
    
    .stButton>button {background: linear-gradient(90deg, #1E90FF 0%, #87CEEB 100%); 
                      color: #fff; border-radius: 12px; border: 2px solid #1E90FF; 
                      font-weight: 700; padding: 0.7rem 1.5rem; font-size: 16px;}
    .stButton>button:hover {background: linear-gradient(90deg, #87CEEB 0%, #1E90FF 100%); 
                            transform: translateY(-2px); box-shadow: 0 6px 20px rgba(30,144,255,0.4);}
    
    .stTextInput>div>div>input {background-color: #ffffff; color: #1a1a1a; 
                                border-radius: 10px; border: 2px solid #87CEEB;}
    
    .stInfo {background-color: #E0F6FF; border-left: 4px solid #87CEEB; color: #1a1a1a; border-radius: 10px;}
    .stWarning {background-color: #FF8C00; border-left: 4px solid #FF6B00; color: #ffffff; border-radius: 10px;}
    .stWarning * {color: #ffffff !important;}
    
    .footer {text-align: center; color: #666; margin-top: 1rem; font-weight: 600; font-size: 14px;}
    .footer span {color: #1E90FF; font-weight: 800;}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("logo.png", width=200)
    except:
        st.markdown("<h2 style='text-align:center;margin-bottom:0;'>📡 Signal<span style='color:#1E90FF'>AI</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;margin-top:0;'>Customer Radar</p>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:-20px;'></div>", unsafe_allow_html=True)

st.markdown("### **Find customers talking about your product**")
st.markdown("<p style='color:#1E90FF;font-weight:600;margin-top:-8px;font-size:15px;'>Stop scrolling. Start selling. Real buyers, real time.</p>", unsafe_allow_html=True)

if 'searches' not in st.session_state:
    st.session_state.searches = ["phone cases", "hair oil"]

col1, col2 = st.columns(2)
with col1:
    product = st.text_input("🎯 What do you sell?", placeholder="clothes, cakes, gadgets")
with col2:
    city = st.text_input("📍 Your city", value="Port Harcourt")

if st.button("💾 Save this search"):
    if product and product not in st.session_state.searches:
        st.session_state.searches.append(product)
        success_box(f"✅ Saved: {product}")

if st.button("🔍 Scan for Customers"):
    if product and city:
        query = f'"{product}" ("buy" OR "price" OR "need" OR "recommend") {city}'
        
        x_query = urllib.parse.quote(query)
        x_url = f"https://twitter.com/search?q={x_query}&src=typed_query&f=live"
        
        fb_query = urllib.parse.quote(f'{product} {city}')
        fb_marketplace = f"https://www.facebook.com/marketplace/search/?query={fb_query}"
        fb_groups = f"https://www.facebook.com/search/top/?q={fb_query}"
        
        success_box(f"🚀 Scanning for '{product}' in {city}...")
        
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
phone = st.text_input("Your WhatsApp number", placeholder="2347067149516")

if st.button("📲 Send test alert to WhatsApp"):
    if phone:
        phone = phone.strip().replace(" ", "")
        if phone.startswith("0"):  # FIXED: was "starts with"
            phone = "234" + phone[1:]
        elif not phone.startswith("234"):
            phone = "234" + phone
            
        msg = f"SignalAI Alert: New customer posted about '{product}' in {city} just now!"
        wa_link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        st.markdown(f"[👉 Click to send alert →]({wa_link})")
        success_box(f"📤 Sending to +{phone}")
    else:
        st.warning("Enter WhatsApp number")

year = datetime.now().year
st.markdown(f'<div class="footer">© {year} <span>@signalai</span>. All rights reserved. Made for Nigerian vendors 🇳🇬</div>', unsafe_allow_html=True)
