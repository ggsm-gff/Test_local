from data_platform.utils import utils
from data_platform.utils.utils import log_execution
import pandas as pd
import duckdb

PIPELINE_NAME = 'dim_sale_status'

logger = utils.get_logger(PIPELINE_NAME)

def read_raw_dim_sale_status(path:str)->pd.DataFrame:
    '''
    Reads the information from the csv file located in the path
    '''
    df = pd.read_csv(path)
    shape = df.shape()
    logger.info(f"read_raw_dim_sale_status read dataframe with {shape} shape")

    return df

def create_table_raw_dim_sale_status(db:duckdb.DuckDBPyConnection):
    
    logger.info("create_table_raw_dim_sale_status: Creating table RAW.TBL_DIM_SALE_STATUS")

    ddl = """
    CREATE TABLE IF NOT EXISTS RAW.TBL_DIM_SALE_STATUS(
        SALE_STATUS_ID INT,
        SALE_STATUS VARCHAR,
        IS_VALID_SALE INT,
        PPN_DT
    );
    """
    db.execute(ddl)




# Orchestrator
@log_execution(PIPELINE_NAME)
def load_raw_dim_sale_status():
    logger.info("load_raw_restaurants_data: Starting process")
    try:
        path = utils.DATA_PATH/"restaurants/dim_sale_status.csv"
        path = str(path)
        logger.info(f"reading path: {path}")

        df = read_raw_dim_sale_status()
        db = utils.get_db_session()

    except Exception as e:
        logger.exception("Error during ingest process")
        raise





if __name__ == '__main__':
    pass
