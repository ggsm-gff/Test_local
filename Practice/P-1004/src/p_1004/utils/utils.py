import sqlite3
import csv
from pathlib import Path
from datetime import datetime
import logging


BASE_DIR = Path(__file__).resolve().parents[3] # Project Directory
SRC_BASE_DIR = Path(__file__).resolve().parents[1] # src/project/ directory
PIPELINES_DIR = SRC_BASE_DIR / "pipelines"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = PIPELINES_DIR / "logs"

# Functions
def get_session() -> sqlite3.Connection| sqlite3.Cursor:
    '''
    Opens a connection to a predefined database and return the Connection and Cursor Objects
    '''
    con = sqlite3.connect(f'{DATA_DIR}/local.db')
    cur = con.cursor()
    return con, cur
    

def close_session(con:sqlite3.Connection , cur:sqlite3.Cursor):
    '''
    Takes the connection and cursor arguments and close the connection to the DB.  
    ''' 
    cur.close()
    con.close()



def get_logger(pipeline_name:str) -> logging.Logger:
    '''
    Prepare a logger object to handle the logging function during the ETL processes.
    '''

    logger = logging.getLogger(pipeline_name)

    if logger.handlers:
        return logger

    # logs/pipeline_name/
    log_dir = LOGS_DIR / pipeline_name
    log_dir.mkdir(parents=True, exist_ok=True)

    # logs/pipeline_name/2026-10-16.log
    log_file = log_dir / f"{pipeline_name}_{datetime.now():%Y-%m-%d}.log"

    handler = logging.FileHandler(
        filename=log_file,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger