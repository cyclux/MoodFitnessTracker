from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from plots import create_plots  # type: ignore

import streamlit as st
from db import (  # type: ignore
    get_postgres_uri,
    get_sql_engine,
    _get_oldest_diary_record_date,
    get_diary_records_by_date_range,
    get_df_with_interval_col,
)
from st_pages import add_page_title

add_page_title()

plt.style.use("ggplot")

postgres_uri = get_postgres_uri()
sql_engine = get_sql_engine(postgres_uri)

col1, col2, col3, col4 = st.columns([1, 1, 2, 1])


def _get_date_timeframe(date_start_default=None) -> tuple[date, date, str] | None:
    date_today = date.today()

    if not date_start_default:
        date_start_default = date_today - timedelta(days=7)

    # col1, col2, col3 = st.columns(3)
    with col1:
        date_start = st.date_input(
            "Datum Start",
            date_start_default,
            format="DD.MM.YYYY",
        )
    with col2:
        date_end = st.date_input(
            "Datum Ende",
            date_today,
            format="DD.MM.YYYY",
        )

    with col3:
        delta_time = st.select_slider(
            "Zeitspanne / Intervall", options=["1day", "3days", "7days"], value="3days"
        )

    if not isinstance(date_start, date) or not isinstance(date_end, date):
        return None

    if date_start > date_end:
        st.error("Das Startdatum muss vor dem Enddatum liegen.")
        return None

    return date_start, date_end, str(delta_time)


def get_df_diary_records() -> tuple[pd.DataFrame, str]:
    oldest_diary_record_date = _get_oldest_diary_record_date(sql_engine)

    date_timeframe = _get_date_timeframe(date_start_default=oldest_diary_record_date)

    if not date_timeframe:
        st.stop()

    date_start, date_end, delta_time = date_timeframe

    df_diary = get_diary_records_by_date_range(
        start_date=date_start, end_date=date_end, sql_engine=sql_engine
    )

    df_diary = get_df_with_interval_col(
        df_diary, interval=delta_time, interval_col_name="date_interval"
    )
    return df_diary, delta_time


def run_analysis():
    df_diary_records, interval_delta_time = get_df_diary_records()

    if col4.button("Plot", type="primary", use_container_width=True):
        create_plots(df_diary_records, interval_delta_time)


run_analysis()
