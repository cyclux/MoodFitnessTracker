import sqlalchemy as sql

DB_CONFIG = {
    "uri": "postgresql://postgres:postgres@docker_db:5433/moodfit_db",
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


sql_engine = get_sql_engine(DB_CONFIG)
