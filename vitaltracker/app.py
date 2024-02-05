from datetime import date, timedelta
import streamlit as st

from st_pages import Page, show_pages, add_page_title
from db import (  # type: ignore
    get_sql_engine,
    get_postgres_uri,
    add_diary_record,
    get_diary_record_by_date,
)
from st_items import get_items  # type: ignore


def main():
    show_pages(
        [
            Page("app.py", "Fragebogen", "📋"),
            Page("analysis.py", "Analyse", "📊"),
        ]
    )

    add_page_title()

    postgres_uri = get_postgres_uri()
    sql_engine = get_sql_engine(postgres_uri)

    # Default date is "yesterday"
    date_yesterday = date.today() - timedelta(days=1)

    # Set placeholder for the title
    title = st.empty()

    date_current = st.date_input(
        "Datum",
        date_yesterday,
        format="DD.MM.YYYY",
    )

    if isinstance(date_current, date):
        records = get_diary_record_by_date(date_current, sql_engine)
        items = get_items(date_current, records)
        # Update the title with the current date
        title.write(f"## Datum: {date_current.strftime('%d.%m.%Y')}")

    else:
        st.write("Bitte ein Datum angeben")
        items = {}

    if st.button("Abschicken", type="primary"):
        response = add_diary_record(items, sql_engine)
        st.write(response)


if __name__ == "__main__":
    main()
