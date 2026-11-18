from data_platform.utils import utils
from data_platform.utils.utils import log_execution
import pandas as pd
import datetime
import duckdb
PIPELINE_NAME = 'dim_restaurants'

logger=utils.get_logger(PIPELINE_NAME)

def read_logger():
    return utils.get_logger(PIPELINE_NAME)

# Read Data
def read_raw_dim_restaurants_data(path:str,chunk_size:int=10000)->pd.DataFrame:
    '''
    Read the restaurants data from the csv file especified by the path parameter.
    '''
    # This function involve a chunksize parameter for a bigger filesize and support iterative reading
    logger.info(f"read_raw_dim_restaurants_data: {path}")
    ppn_dt = datetime.datetime.today().date()
    rows_read=0

    for df in pd.read_csv(path, chunksize=chunk_size):
        df['PPN_DT'] = pd.to_datetime(ppn_dt) 
        shape = df.shape
        rows_read = rows_read + shape[0]
        logger.info(f"read_raw_dim_restaurants_data: DataFrame read with: {shape} shape | total rows read: {rows_read}")
        yield df

# DML
def insert_raw_dim_restaurants_data(df:pd.DataFrame, db:duckdb.DuckDBPyConnection, chunk_size:int=10000):
    '''
    Takes the restaurants_data values and loads them into the db
    '''
    # Registering the df as a table to read it via duckdb is the easiest way to generate the merge behavior desired for idempotency.
    db.register("restaurants_df", df)

    db.execute("""
        MERGE INTO raw.tbl_dim_restaurants AS tgt
        USING restaurants_df AS src
        ON tgt.restaurant_id = src.restaurant_id
        AND tgt.ppn_dt = src.ppn_dt

        WHEN MATCHED THEN
            UPDATE SET
                restaurant_name = src.restaurant_name,
                zone = src.zone

        WHEN NOT MATCHED THEN
            INSERT (
                restaurant_id,
                restaurant_name,
                zone,
                ppn_dt
            )
            VALUES (
                src.restaurant_id,
                src.restaurant_name,
                src.zone,
                src.ppn_dt
            );
    """)


# DDL
def create_raw_dim_restaurants_table(db:duckdb.DuckDBPyConnection):
    '''
    Takes the cursor argument to execute a ddl sentence.
    Creates a predefined sql table.
    '''
    logger.info("create_raw_restaurants_table: Creating table RAW.TBL_DIM_RESTAURANTS")
    
    ddl_sentence = """
        CREATE TABLE IF NOT EXISTS RAW.TBL_DIM_RESTAURANTS(
            RESTAURANT_ID VARCHAR(10),
            RESTAURANT_NAME VARCHAR(100),
            ZONE VARCHAR(50),
            PPN_DT DATE
        );
        """
    db.execute(ddl_sentence)

# Orchestrator
@log_execution(PIPELINE_NAME)
def load_raw_restaurants_data():
    logger.info("load_raw_restaurants_data: Starting process")
    try:
        db = utils.get_db_session()
        path = utils.DATA_PATH/"restaurants/dim_restaurants.csv"
        path = str(path)

        logger.info(f"reading path: {path}")

        # DDL preparing the table
        create_raw_dim_restaurants_table(db)

        rows=0
        # Extract
        for df in read_raw_dim_restaurants_data(path, 5):
            rows=rows + df.shape[0]
            # Load
            insert_raw_dim_restaurants_data(df=df,db=db)
            logger.info(f"Total rows loaded into db : {rows}")
        
        utils.close_db_session(db)
        logger.info("load_raw_restaurants_data: Completed")
        
    except Exception as e:
        logger.exception("Error during ingest process")
        raise

if __name__=='__main__':
    pass
    #load_raw_restaurants_data()
    