import sqlalchemy as sql


def get_sql_engine(db_config: dict) -> sql.Engine:
    engine = sql.create_engine(db_config["uri"])
    engine.connect()
    return engine


db_config = {
    "uri": "postgresql://postgres:postgres@docker_db:5433/moodfit_db",
}

sql_engine = get_sql_engine(db_config)

