import streamlit as st
import urllib.parse

st.set_page_config(page_title="SignalAI - Customer Radar", page_icon="📡", layout="wide")

st.title("📡 SignalAI")
st.caption("Find customers talking about your product")

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
if st.button("🔍 Scan for Customers"):
    if product and city:
        query = f'"{product}" ("buy" OR "price" OR "need" OR "recommend") {city}'
        
        x_query = urllib.parse.quote(query)
        x_url = f"https://twitter.com/search?q={x_query}&src=typed_query&f=live"
        
        fb_query = urllib.parse.quote(f'{product} {city}')
        fb_marketplace = f"https://www.facebook.com/marketplace/search/?query={fb_query}"
        fb_groups = f"https://www.facebook.com/search/top/?q={fb_query}"
        
        st.success(f"Scanning for '{product}' in {city}...")
        
        st.markdown("### Open customer conversations:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[🐦 X/Twitter]({x_url})")
        with col2:
            st.markdown(f"[📘 Facebook Marketplace]({fb_marketplace})")
        
        st.markdown(f"[👥 Facebook Groups]({fb_groups})")
        
        st.markdown("---")
        st.subheader("Top customer posts found:")
        st.info("X + Facebook block direct scraping. Click links above for live posts. Filter by 'Latest' and reply: I sell {product} in {city}. DM me")
        
    else:
        st.warning("Enter product + city first")

st.markdown("---")
st.subheader("💾 Your Saved Searches")
for i, s in enumerate(st.session_state.searches):
    if st.button(f"Scan {s}", key=i):
        st.session_state.last_search = s
        st.rerun()

st.markdown("---")
st.subheader("📱 WhatsApp Alerts")
phone = st.text_input("Your WhatsApp number", placeholder="2347067149516", help="Use 234 + your number, no 0. Example: 2347067149516")

if st.button("Send test alert to WhatsApp"):
    if phone:
        # Auto-convert 0706... to 234706...
        phone = phone.strip().replace(" ", "")
        if phone.startswith("0"):
            phone = "234" + phone[1:]
        elif not phone.startswith("234"):
            phone = "234" + phone
            
        msg = f"SignalAI Alert: New customer posted about '{product}' in {city} just now!"
        wa_link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        st.markdown(f"[Click to send alert →]({wa_link})")
        st.success(f"Sending to +{phone}")
    else:
        st.warning("Enter WhatsApp number")

st.caption("SignalAI - Customer radar for Nigerian vendors")
