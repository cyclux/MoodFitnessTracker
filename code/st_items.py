from datetime import date
import streamlit as st

from typing import Any


def get_items(current_date: date, records: dict) -> dict:
    """Gets user input items for mood fitness tracking.

    Returns:
        dict: Dictionary containing the following user input items:
            - "tasks": List of selected task difficulty levels
            - "sleep": Number of hours slept
            - "bodybattery_min": Minimum body battery level
            - "bodybattery_max": Maximum body battery level
            - "steps": Number of steps taken
            - "body": Body condition grade
            - "psyche": Mental condition grade
            - "dizzy": Boolean indicating dizziness
            - "comment": Free-form text comment

    """
    items: dict[Any, Any] = records

    items["date"] = current_date

    items["tasks"] = st.multiselect(
        "Tätigkeiten",
        options=[1, 1, 1, 2, 2, 2, 3, 3, 3],
        default=items.get("tasks", []),
        help="1: Etwas anstrengend, 2: Mittel anstrengend, 3: Sehr anstrengend",
    )

    items["sleep"] = st.slider(
        "Schlaf",
        min_value=0,
        max_value=12,
        value=items.get("sleep", 6),
        step=1,
        help="Schlaf in Stunden",
    )

    items["bodybattery_min"] = st.slider(
        "Body Battery Min",
        min_value=0,
        max_value=100,
        value=items.get("bodybattery_min", 50),
        step=1,
    )

    items["bodybattery_max"] = st.slider(
        "Body Battery Max",
        min_value=0,
        max_value=100,
        value=items.get("bodybattery_max", 50),
        step=1,
    )

    items["steps"] = st.number_input(
        "Schritte", value=items.get("steps", 0), step=1, help="Anzahl Schritte"
    )

    items["body"] = st.slider(
        "Körper",
        min_value=0,
        max_value=6,
        value=items.get("body", 3),
        step=1,
        help="Schulnoten | 0 bedeutet besonders gut",
    )

    items["psyche"] = st.slider(
        "Psyche",
        min_value=0,
        max_value=6,
        value=items.get("psyche", 3),
        step=1,
        help="Schulnoten | 0 bedeutet besonders gut",
    )

    items["dizzy"] = st.toggle(
        "Schwindel", value=items.get("dizzy", False), help="Ja / Nein"
    )

    items["comment"] = st.text_area("Kommentar", value=items.get("comment", ""))

    return items
