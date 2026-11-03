import logging
from pathlib import Path
from datetime import datetime
import duckdb
import time
from functools import wraps

DATA_PLATFORM_PATH = Path(__file__).resolve().parents[3]
LOGS_PATH = DATA_PLATFORM_PATH / "logs"
DATA_PATH = DATA_PLATFORM_PATH / "data"
DBT_PATH = DATA_PLATFORM_PATH / "dbt"
WAREHOUSE_PATH = DATA_PATH / "warehouse"
#logger = get_logger("")

def get_logger(name:str) ->logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_dir = LOGS_PATH / name
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{name}_{datetime.now():%Y-%m-%d}.log"

    handler = logging.FileHandler(
        filename=log_file,
        encoding='utf-8'
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

def get_db_session():
    #logger.info("get_db_session: Starting a db Connection")
    db = duckdb.connect(WAREHOUSE_PATH/"warehouse.db")
    return db

def close_db_session(db:duckdb.DuckDBPyConnection):
    #logger.info("close_db_session: Clossing a db Connection")
    db.close()

def log_execution(pipeline_name):
    
    logger = get_logger(pipeline_name)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            phase = func.__name__
            start_time = time.perf_counter()
            logger.info(f'Starting phase: {phase}')
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time

                logger.info(f'Completed phase: {phase}| Duration: {elapsed}')
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start_time
                logger.exception(f'Failed in phase: {phase}| Duration: {elapsed}')
                raise
        return wrapper
    return decorator