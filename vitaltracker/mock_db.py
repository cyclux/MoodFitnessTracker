from typing import Any
from datetime import datetime, timedelta
import random
import numpy as np


def get_datelist_from_amount_of_days(days: int = 0):
    """Gets a list of date strings for given number of past days.

    Args:
        days (int): The number of past days to get dates for.

    Returns:
        list: A list of date strings in ISO format for the given number
            of past days.

    Examples:
        >>> get_datelist_from_amount_of_days(3)
        ['2023-03-03', '2023-03-02', '2023-03-01']

    """
    return [
        (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
        for day in range(days)
    ]


def get_random_entry(day: str) -> dict[str, Any]:
    random_entry: dict[str, Any] = {}

    # Pick random tasks [from 0 to 3 tasks, each level 1 to 3]
    random_entry["date"] = day
    random_entry["tasks"] = random.choices([1, 2, 3], k=random.randint(0, 3))

    # Pick plausible random values for all other items
    # random_entry["sleep"] = random.randint(4, 12)
    random_entry["sleep"] = int(np.random.normal(8, 1, 1)[0])
    random_entry["bodybattery_min"] = int(np.random.normal(20, 7, 1)[0])
    random_entry["bodybattery_max"] = int(np.random.normal(75, 7, 1)[0])
    # random_entry["bodybattery_min"] = random.uniform(5, 40)
    # random_entry["bodybattery_max"] = random.uniform(50, 100)
    random_entry["steps"] = random.randint(400, 8000)
    random_entry["body"] = random.randint(0, 6)
    random_entry["psyche"] = random.randint(0, 6)
    random_entry["dizzy"] = random.choice([True, False])
    # Keep comment empty for now
    random_entry["comment"] = ""

    return random_entry


def get_random_entries(amount: int = 1) -> list[dict[str, Any]]:
    """Gets a list of random entries for given number of past days.

    Args:
        amount (int): The number of random entries to generate.

    Returns:
        list[dict[str, Any]]: A list containing the generated random entries.

    Raises:
        ValueError: If amount is less than 1.

    Examples:
        >>> get_random_entries(3)
        [
            {'tasks': [2], 'sleep': 7, ...},
            {'tasks': [1, 3], 'sleep': 5, ...},
            {'tasks': [], 'sleep': 8, ...}
        ]

    Note:
        The entries contain random plausible values for tasks, sleep etc.
    """
    if amount < 1:
        raise ValueError("amount must be greater than or equal to 1")

    return [
        get_random_entry(day) for day in get_datelist_from_amount_of_days(days=amount)
    ]
