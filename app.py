import streamlit as st

st.set_page_config(page_title="SignalAI - Customer Radar", page_icon="📡")
st.title("📡 SignalAI")
st.caption("Track where your customers are talking")

product = st.text_input("What do you sell?", placeholder="phone cases, hair oil")
city = st.text_input("Your city", value="Port Harcourt")

if st.button("Scan for Customers"):
    if product and city:
        search = f'"{product}" ("buy" OR "price" OR "recommend") {city}'
        x_url = f"https://twitter.com/search?q={search.replace(' ', '%20')}&src=typed_query"
        st.success("Found customer conversations!")
        st.markdown(f"[🎯 View buyers on X →]({x_url})")
    else:
        st.warning("Enter product + city first")

st.caption("V1: X search. V2: Auto alerts")
