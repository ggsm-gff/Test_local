import p_1004.utils.utils as utils
import p_1004.pipelines.restaurants.extract as extract
import p_1004.pipelines.restaurants.load as load

filename='restaurants_L2_dirty.csv'

logger = utils.get_logger('restaurants')
logger.info("Pipeline restaurants iniciado")
try:
    logger.info('Iniciado Extracción')
    restaurants_data = extract.extract_restaurants_data(filename=filename)
    logger.info(f'Extracción completada. Registros: {len(restaurants_data)}')

    logger.info('Iniciando Carga')
    load.load_restaurants(restaurants_data=restaurants_data)
    logger.info('Carga Completada')

    logger.info("Pipeline restaurants finalizado exitosamente")
except Exception as e:
    logger.exception(
        "Error durante la extracción"
    )
    raise

'''
INFO → Inicio/fin de procesos y métricas.
WARNING → Datos inesperados pero recuperables.
ERROR → Falla de una operación.
EXCEPTION → Dentro de un except.
'''