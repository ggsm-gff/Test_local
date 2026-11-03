from data_platform.utils import utils
from data_platform.utils.utils import log_execution
import pandas as pd
import duckdb
PIPELINE_NAME = 'restaurants'

logger=utils.get_logger(PIPELINE_NAME)

# Read Data
def read_raw_restaurants_data(path:str,chunk_size:int=10000)->pd.DataFrame:
    '''
    Read the restaurants data from the csv file especified by the path parameter.

    '''
    # This function involve a chunksize parameter for a bigger filesize and support iterative reading
    logger.info(f"read_raw_restaurants_data: {path}")
    #df = pd.read_csv(path, chunksize=chunk_size)
    # chunk size involve an iterator and 
    df = pd.read_csv(path)
    df.columns = ['ID','NAME','ADDR','CITY','PHONE','TYPE']
    shape = df.shape
    logger.info(f"read_raw_restaurants_data: DataFrame read with: {shape} shape")
    return df

# DML
def insert_raw_restaurants_data(df:pd.DataFrame, db:duckdb.DuckDBPyConnection, chunk_size:int=10000):
    '''
    Takes the restaurants_data values and loads them into the db
    '''
    logger.info(f"insert_raw_restaurants_data: Inserting ({df.shape}) DataFrame")
    #db.executemany("insert into raw.tbl_restaurants values(?,?,?,?,?,?)",df)

    db.register("restaurants_df", df)

    """db.execute(
        INSERT INTO raw.tbl_restaurants
        SELECT *
        FROM restaurants_df
    ) """

    db.execute("""
        MERGE INTO raw.tbl_restaurants AS tgt
        USING restaurants_df AS src
        ON tgt.id = src.id

        WHEN MATCHED THEN
            UPDATE SET
                name = src.name,
                ADDR = src.ADDR,
                city = src.city,
                PHONE = src.PHONE,
                TYPE = src.TYPE

        WHEN NOT MATCHED THEN
            INSERT (
                id,
                name,
                ADDR,
                city,
                PHONE,
                TYPE
            )
            VALUES (
                src.id,
                src.name,
                src.ADDR,
                src.city,
                src.PHONE,
                src.TYPE
            );
    """)

    #logger.info("insert_raw_restaurants_data: Completed")

# DDL
def create_raw_restaurants_table(db:duckdb.DuckDBPyConnection):
    '''
    Takes the cursor argument to execute a ddl sentence.
    Creates a predefined sql table.
    '''
    logger.info("create_raw_restaurants_table: Creating table RAW.TBL_RESTAURANTS")
    
    ddl_sentence = """
        CREATE TABLE IF NOT EXISTS RAW.TBL_RESTAURANTS(
            ID INT,
            NAME TEXT,
            ADDR TEXT,
            CITY TEXT,
            PHONE TEXT,
            TYPE TEXT
        );
        """
    db.execute(ddl_sentence)
    #logger.info("create_raw_restaurants_table: table RAW.TBL_RESTAURANTS is ready")

# Orchestrator
@log_execution(PIPELINE_NAME)
def load_raw_restaurants_data():
    logger.info("load_raw_restaurants_data: Starting process")
    try:
        db = utils.get_db_session()
        path = utils.DATA_PATH/"restaurants/restaurants_L2_dirty.csv"
        path = str(path)
        print(path)

        # Extract
        df = read_raw_restaurants_data(path)
        # Load
        create_raw_restaurants_table(db)
        insert_raw_restaurants_data(df=df,db=db)

        utils.close_db_session(db)
        logger.info("load_raw_restaurants_data: Completed")
        
    except Exception as e:
        logger.exception("Error during ingest process")
        raise

if __name__=='__main__':
    load_raw_restaurants_data()
    