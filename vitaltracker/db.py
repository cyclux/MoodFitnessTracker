import os
from dotenv import load_dotenv
from datetime import date

from pathlib import Path

import pandas as pd

import sqlalchemy as sql
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Date, Integer, Float, Boolean, Text, ARRAY

from typing import List

import streamlit as st

# TODO: find solutions for type ignore, sqlalchemy 2.* introduced new way of declaring Table classes

# metadata_obj = MetaData()

# Diary = Table(
#     "diary",
#     metadata_obj,
#     Column("date", Date, primary_key=True),
#     Column("tasks", Column(ARRAY(Integer))),
#     Column("sleep", Column(Float)),
#     Column("bodybattery_min", Column(Integer)),
#     Column("bodybattery_max", Column(Integer)),
#     Column("steps", Column(Integer)),
#     Column("body", Column(Integer)),
#     Column("psyche", Column(Integer)),
#     Column("dizzy", Column(Boolean)),
#     Column("comment", Column(Text)),
# )


def check_success(result: sql.Result) -> str:
    """Checks if a SQL statement was successful.

    Args:
        result (sql.CursorResult): Result of executing the SQL statement.

    Returns:
        str: A message indicating whether the SQL statement was successful.

    Raises:
        SQLAlchemyError: If there was an error executing the SQL statement.
    """
    if not isinstance(result, sql.CursorResult):
        raise TypeError(
            f"Der Parameter `result` muss ein Objekt vom Typ `CursorResult` sein. "
            f"Der Typ `{type(result)}` wurde an die Funktion übergeben."
        )
    if result.rowcount == 1:
        return ":green[Gespeichert]"
    else:
        return ":red[Fehler bei der Speicherung. Versuche es erneut.]"


def get_postgres_pw() -> str:
    """Gets the PostgreSQL database password from the .env file.

    Returns:
        str: The PostgreSQL database password read from the
            PG_PASSWORD environment variable.

    Raises:
        SystemExit: If the PG_PASSWORD environment variable is not set,
            the program will stop execution and print an error message.

    Note:
        Relies on the python-dotenv package to load environment variables
        from the .env file.
    """
    load_dotenv(Path(".env"))
    pg_pw = os.environ.get("PG_PASSWORD")

    if pg_pw is None:
        st.write("Kein DB Passwort gefunden. Bitte ein Passwort in der .env anlegen.")
        st.stop()

    return pg_pw


def get_postgres_uri() -> dict:
    """Get PostgreSQL database URI.

    Constructs the PostgreSQL database URI from environment variables.

    Returns:
        dict: Dictionary containing the PostgreSQL database URI
            under the "uri" key.
    """
    return {
        "uri": f"postgresql://postgres:{get_postgres_pw()}@docker_db:5432/moodfit_db",
    }


def get_sql_engine(db_config: dict) -> sql.Engine:
    """Get SQLAlchemy engine instance

    Creates and initializes a SQLAlchemy engine based on the provided
    database configuration.

    Args:
        db_config (dict): Database configuration dictionary containing the
                        database URI and credentials

    Returns:
        sql.Engine: SQLAlchemy engine instance for the database
    """
    engine = sql.create_engine(db_config["uri"])
    engine.connect()
    return engine


Base = declarative_base()


class Diary(Base):  # type: ignore
    __tablename__ = "diary"

    date = Column(Date, primary_key=True)
    tasks = Column(ARRAY(Integer))  # type: ignore
    sleep = Column(Float)
    bodybattery_min = Column(Integer)
    bodybattery_max = Column(Integer)
    steps = Column(Integer)
    body = Column(Integer)
    psyche = Column(Integer)
    dizzy = Column(Boolean)
    comment = Column(Text)

    def __repr__(self):
        return (
            f"<Diary(date={self.date}, tasks={self.tasks}, sleep={self.sleep}, "
            f"bodybattery_min={self.bodybattery_min}, bodybattery_max={self.bodybattery_max}, "
            f"steps={self.steps}, body={self.body}, psyche={self.psyche}, "
            f"dizzy={self.dizzy}, comment={self.comment})>"
        )


def add_diary_record(items: dict, sql_engine: sql.Engine) -> str:
    """Adds a record to the diary table in the moodfit_db database.

    Args:
        items (dict): A dictionary containing the diary record data.
        sql_engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance for the database.

    Returns:
        str: A message indicating whether the insert was successful.

    Raises:
        SQLAlchemyError: If there was an error executing the SQL statement.

    Note:
        Uses an UPSERT statement to insert/update the record.
    """
    upsert_stmt = sql.text(
        """
        INSERT INTO diary (date, tasks, sleep, bodybattery_min, bodybattery_max, steps, body, psyche, dizzy, comment)
        VALUES (:date, :tasks, :sleep, :bodybattery_min, :bodybattery_max, :steps, :body, :psyche, :dizzy, :comment)
        ON CONFLICT (date) DO UPDATE SET
            tasks = EXCLUDED.tasks,
            sleep = EXCLUDED.sleep,
            bodybattery_min = EXCLUDED.bodybattery_min,
            bodybattery_max = EXCLUDED.bodybattery_max,
            steps = EXCLUDED.steps,
            body = EXCLUDED.body,
            psyche = EXCLUDED.psyche,
            dizzy = EXCLUDED.dizzy,
            comment = EXCLUDED.comment
        """
    )
    # Use a Session to execute the SQL statement
    try:
        with Session(sql_engine) as session:
            result = session.execute(upsert_stmt, items)
            session.commit()
            response_txt = check_success(result)

    except SQLAlchemyError as e:
        session.rollback()
        response_txt = f":red[Datenbankfehler:] {e}"

    return response_txt


def add_diary_records_bulk(items: list[dict], sql_engine: sql.Engine) -> str:
    """
    Adds multiple records to the diary table in the moodfit_db database using bulk operation.

    Args:
        items (list[dict]): A list of dictionaries, each containing the diary record data.
        sql_engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance for the database.

    Returns:
        str: A message indicating whether the insert was successful.
    """
    try:
        with Session(sql_engine) as session:
            session.bulk_insert_mappings(
                mapper=Diary,  # type: ignore
                mappings=items,
                render_nulls=True,
            )
            session.commit()
            return "Records successfully added in bulk."

    except SQLAlchemyError as e:
        # Handle the exception and return an error message
        return f"Database error: {e}"


def get_diary_record_by_date(date: date, sql_engine: sql.Engine) -> dict:
    """Query the diary table for a specific date and return the record as a dict.

    Args:
        date (str): The date to query in the diary table.
        sql_engine (sql.Engine): SQLAlchemy engine instance for the database.

    Returns:
        dict: The diary record of the specified date, or None if no record is found.
    """
    # Define the SQL SELECT statement
    columns: List[sql.ColumnElement] = [
        sql.column("date"),
        sql.column("tasks"),
        sql.column("sleep"),
        sql.column("bodybattery_min"),
        sql.column("bodybattery_max"),
        sql.column("steps"),
        sql.column("body"),
        sql.column("psyche"),
        sql.column("dizzy"),
        sql.column("comment"),
    ]
    select_stmt = (
        sql.select(*columns)
        .select_from(sql.table("diary"))
        .where(sql.column("date") == date)
    )

    # Execute the query and fetch the result
    with sql_engine.connect() as conn:
        result = conn.execute(select_stmt).fetchone()

    # If a record is found, return as a dictionary
    if result:
        return {
            "date": result[0],
            "tasks": result[1],
            "sleep": result[2],
            "bodybattery_min": result[3],
            "bodybattery_max": result[4],
            "steps": result[5],
            "body": result[6],
            "psyche": result[7],
            "dizzy": result[8],
            "comment": result[9],
        }
    else:
        return {"date": date}


def _get_oldest_diary_record_date(sql_engine: sql.Engine) -> date | None:
    """Query the diary table for the oldest record and return the date."""
    # Define the SQL SELECT statement
    columns: List[sql.ColumnElement] = [sql.column("date")]
    select_stmt = (
        sql.select(*columns)
        .select_from(sql.table("diary"))
        .order_by(sql.column("date").asc())
        .limit(1)
    )

    # Execute the query and fetch the result
    with sql_engine.connect() as conn:
        result = conn.execute(select_stmt).fetchone()
        if result:
            return result[0]
        return None


def get_diary_records_as_df(sql_engine: sql.Engine) -> pd.DataFrame:
    """Query the diary table of the DB and return the records as a DataFrame.

    Args:
        sql_engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance
            for the database

    Returns:
        pd.DataFrame: Dataframe containing all records from the diary table

    Raises:
        SQLAlchemyError: If there is an error executing the SQL query

    Examples:
        ```python
        import pandas as pd
        from sqlalchemy import create_engine

        engine = create_engine('sqlite:///mydb.sqlite')

        df = get_diary_records_as_df(engine)
        print(df.head())
        ```

    Note:
        Converts the 'date' column to datetime64[s].
    """
    query = "SELECT * FROM diary"
    df_diary = pd.read_sql_query(query, sql_engine)
    # df_diary["date"] = df_diary["date"].astype("datetime64[s]")
    df_diary["date"] = pd.to_datetime(df_diary["date"])

    return df_diary.sort_values("date", ascending=False)


def get_diary_records_by_date_range(
    start_date: date, end_date: date, sql_engine: sql.Engine
) -> pd.DataFrame:
    """Query the diary table for a date range and return the records as a dataframe.

    Args:
        start_date (date): The start date of the range to query.
        end_date (date): The end date of the range to query.
        sql_engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance
            for the database

    Returns:
        pd.DataFrame: DataFrame containing the diary records within the
        specified date range.

    Raises:
        SQLAlchemyError: If there is an error executing the SQL query.
    """
    df_diary = get_diary_records_as_df(sql_engine)
    return df_diary[
        (df_diary["date"] >= pd.to_datetime(start_date))
        & (df_diary["date"] <= pd.to_datetime(end_date))
    ]


def _get_date_interval_column(df: pd.DataFrame, interval: str) -> pd.Series:
    """Gets date interval column segmented by specified time interval.

    Args:
        df (pd.DataFrame): Input dataframe, must have a 'date' column.
        interval (str): Interval duration over which to segment the 'date' values,
            e.g. '3days'.

    Returns:
        pd.Series: Series containing integer segment number for each row's 'date'
            value, segmented by the specified time interval.

    Raises:
        ValueError: If input dataframe does not have a 'date' column.

    Examples:
        >>> df = pd.DataFrame({'date': ['2023-01-01', '2023-01-04']})
        >>> _get_date_interval_col(df, '2days')
        0    0
        1    1
        Name: date_interval, dtype: int64

    Note:
        Date intervals are calculated relative to minimum 'date' value in the
        dataframe.
    """
    if "date" not in df.columns:
        raise ValueError("Input dataframe must have a 'date' column.")

    interval_length = pd.Timedelta(interval)
    reference_start_date = df["date"].min()

    return df["date"].apply(
        lambda x: (x - reference_start_date).days // interval_length.days
    )


def get_df_with_interval_col(
    df: pd.DataFrame, interval: str = "3days", interval_col_name: str = "date_interval"
) -> pd.DataFrame:
    """Gets a DataFrame with an added column segmented by a specified time interval.

    This function adds a new column to the input DataFrame that represents time
    intervals for each date entry. The intervals are calculated based on the
    minimum date in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame, which must have a 'date' column.
        interval (str): The time interval used to segment the 'date' values.
            Defaults to "3days".
        interval_col_name (str): The name of the new interval column to be added
            to the DataFrame. Defaults to "date_interval".

    Returns:
        pd.DataFrame: A copy of the input DataFrame with the added 'date_interval'
            column containing integer segment numbers for each row's 'date' value,
            segmented by the specified time interval.

    Raises:
        ValueError: If the input DataFrame does not have a 'date' column.

    Examples:
        >>> df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-04'])})
        >>> get_df_with_interval_col(df)
           date date_interval
        0 2023-01-01            0
        1 2023-01-04            1

    Note:
        The 'date' column is converted to datetime64 if not already in that format.
        The date intervals are calculated relative to the minimum 'date' value in
        the DataFrame. The name of the new interval column can be customized using
        the 'interval_col_name' argument.
    """
    if "date" not in df.columns:
        raise ValueError("Input dataframe must have a 'date' column.")

    df[interval_col_name] = _get_date_interval_column(df, interval)
    return df
