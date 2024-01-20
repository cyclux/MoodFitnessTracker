from datetime import date, timedelta
import streamlit as st
from db import get_sql_engine, add_diary_record, get_diary_record_by_date
from st_items import get_items


DB_CONFIG = {
    "uri": "postgresql://postgres:postgres@docker_db:5432/moodfit_db",
}


def main():
    sql_engine = get_sql_engine(DB_CONFIG)

    st.title("Vitaltagebuch")

    # Default date is "yesterday"
    date_yesterday = date.today() - timedelta(days=1)
    current_date = st.date_input("Datum", date_yesterday)

    if isinstance(current_date, date):
        records = get_diary_record_by_date(current_date, sql_engine)
        items = get_items(current_date, records)

    else:
        st.write("Bitte ein Datum angeben")
        items = {}

    if st.button("Abschicken", type="primary"):
        response = add_diary_record(items, sql_engine)
        st.write(response)


if __name__ == "__main__":
    main()
