import sqlalchemy as sql
from sqlalchemy.sql import text


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


def add_diary_record(items: dict, sql_engine: sql.Engine) -> None:
    """
    Adds a record to the diary table in the moodfit_db database.

    Args:
        items (dict): A dictionary containing the diary record data.
    """

    upsert_stmt = text(
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

    # Execute the SQL statement with the provided items
    with sql_engine.connect() as conn:
        conn.execute(upsert_stmt, items)
        conn.commit()
