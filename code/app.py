import streamlit as st
from st_items import get_items

items = get_items()

if st.button("Abschicken", type="primary"):
    st.write(items)
