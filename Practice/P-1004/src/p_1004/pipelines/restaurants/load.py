import sqlite3
import p_1004.utils.utils as utils

logger = utils.get_logger('restaurants')

# DDL
def create_raw_restaurants_table(cur:sqlite3.Cursor):
    '''
    Takes the cursor argument to execute a ddl sentence.
    Creates a predefined sql table.
    '''
    logger.info('Creando tabla RAW_TBL_RESTAURANTS si no existe')
    # In sqlite the varchar type is considered TEXT which is legacy behavior
    ddl_sentence = """
        CREATE TABLE IF NOT EXISTS RAW_TBL_RESTAURANTS(
            ID INT,
            NAME TEXT,
            ADDR TEXT,
            CITY TEXT,
            PHONE TEXT,
            TYPE TEXT
        );
        """
    cur.execute(ddl_sentence)
    logger.info('Tabla RAW_TBL_RESTAURANTS validada exitosamente')
    

# DML
def insert_restaurants_data(restaurants_data:list, cur:sqlite3.Cursor, con:sqlite3.Connection):
    '''
    Takes the restaurants_data values and loads them into the db
    '''
    rows = len(restaurants_data)
    logger.info(f'Iniciando carga de {rows} registros')
    cur.executemany("insert into raw_tbl_restaurants values(?,?,?,?,?,?)",restaurants_data[1:])
    con.commit()
    logger.info('Carga de información completada con éxito.')
    
# Orchestrator
def load_restaurants(restaurants_data:list):
    logger.info('Iniciando sesion en DB')
    try:
        con, cur = utils.get_session()

        create_raw_restaurants_table(cur=cur)
        insert_restaurants_data(restaurants_data=restaurants_data, cur=cur, con=con)

        utils.close_session(con=con, cur=cur)
    except Exception as e:
        logger.exception('Error en Carga de Información hacia DB')
        raise
