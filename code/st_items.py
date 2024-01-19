import streamlit as st

from typing import Any


def get_items() -> dict:
    items: dict[Any, Any] = {}

    items["tasks"] = st.multiselect(
        "Tätigkeiten",
        [1, 1, 1, 2, 2, 2, 3, 3, 3],
        help="1: Etwas anstrengend, 2: Mittel anstrengend, 3: Sehr anstrengend",
    )

    items["sleep"] = st.number_input("Schlaf", step=1, help="Schlaf in Stunden")

    items["bodybattery_min"] = st.slider(
        "Body Battery Min",
        min_value=0,
        max_value=100,
        value=None,
        step=1,
    )

    items["bodybattery_max"] = st.slider(
        "Body Battery Max",
        min_value=0,
        max_value=100,
        value=None,
        step=1,
    )

    items["steps"] = st.number_input("Schritte", step=1, help="Anzahl Schritte")

    items["body"] = st.slider(
        "Körper",
        min_value=0,
        max_value=6,
        value=None,
        step=1,
        help="Schulnoten | 0 bedeutet besonders gut",
    )

    items["psyche"] = st.slider(
        "Psyche",
        min_value=0,
        max_value=6,
        value=None,
        step=1,
        help="Schulnoten | 0 bedeutet besonders gut",
    )

    items["dizzy"] = st.toggle("Schwindel", value=False, help="Ja / Nein")

    items["comment"] = st.text_area("Kommentar")

    return items
