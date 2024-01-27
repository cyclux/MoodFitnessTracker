from datetime import date, timedelta
import streamlit as st
from db import (  # type: ignore
    get_sql_engine,
    get_postgres_uri,
    add_diary_record,
    get_diary_record_by_date,
)
from st_items import get_items  # type: ignore


def main():
    postgres_uri = get_postgres_uri()
    sql_engine = get_sql_engine(postgres_uri)

    # Default date is "yesterday"
    date_yesterday = date.today() - timedelta(days=1)

    # Set placeholder for the title
    title = st.empty()

    current_date = st.date_input(
        "Datum",
        date_yesterday,
    )

    if isinstance(current_date, date):
        records = get_diary_record_by_date(current_date, sql_engine)
        items = get_items(current_date, records)
        # Update the title with the current date
        title.write(f"## Vital Tracker: {current_date}")

    else:
        st.write("Bitte ein Datum angeben")
        items = {}

    if st.button("Abschicken", type="primary"):
        response = add_diary_record(items, sql_engine)
        st.write(response)


if __name__ == "__main__":
    main()
