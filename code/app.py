import streamlit as st
from db import get_sql_engine, add_diary_record
from st_items import get_items


DB_CONFIG = {
    "uri": "postgresql://postgres:postgres@docker_db:5432/moodfit_db",
}

sql_engine = get_sql_engine(DB_CONFIG)
items = get_items()

if st.button("Abschicken", type="primary"):
    st.write(items)
    add_diary_record(items, sql_engine)
