import csv 
import p_1004.utils.utils as utils

logger=utils.get_logger('restaurants')

def extract_restaurants_data(filename:str)->list:
    '''
    Gets the data from a csv file, just csv module reader.
    filename: str containing the name and the extension of the file to be read.
    '''
    logger.info('Leyendo archivo .csv')
    try:
        line_content = []
        with open(f'{utils.DATA_DIR}/{filename}','r') as csv_file:
            content = csv.reader(csv_file, delimiter=',')
            for row in content:
                line_content.append(row)
        return line_content
    except Exception as e:
        logger.exception('Error leyendo el archivo de origen')
        raise
