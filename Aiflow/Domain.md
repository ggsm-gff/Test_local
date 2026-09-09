## Operadores
- Representan una sola tarea en un flujo de trabajo
- Se ejecutan de form independiente
- Generalmente no comparten información

```python
from airflow.sdk import dag, task

@dag(
    dag_id = 'Example_Dag'
)
def example_dag():
    # El siguiente es un PythonOperator
    @task
    def task1():
        return "The result from task1"

    task1()
example_dag()

# Bash operator ejecuta un comando o script de bash
@task.bash
def bash_example():
    return "echo 'Example!'"

bash_example()

@task.bash
def run_cleanup():
    return "runcleanup.sh"

run_cleanup()
```

### BashOperator
- Ejecuta el comando en un directorio temporal
- Permite definir variables de entorno para el comando

Definir las dependencias de tareas con >> o <<
denominado bitshift:
- Dependencia lineal
`task1() >> task2()`  
`task1() >> task2() >>task3()`
- Dependencia en paralelo:
`task1() >> task3()`
`task2() >> task3()`

Example:
```python
from airflow.sdk impot dag, task
@dag(
  dag_id='analytics_dag', 
  start_date=datetime(2026,1,1)
)
def analytics_dag():
  # Specify a Bash task
  @task.bash
  def cleanup_task():
    return 'cleanup.sh'
  
  # Run the task
  cleanup_task()

analytics_dag()
```

Example:
```python
@dag(
    dag_id="analytics_dag",
    start_date=datetime(2026, 3, 1),
)
def analytics_dag():
    # Run cleanup before consolidate
    cleanup() >> consolidate()
    # Run consolidate before push_data
    consolidate() >> push_data()

analytics_dag()
```

Exercise:
```python
@dag(dag_id='process_sales')
def process_sales():
    # Decorate parse_file as a task
    @task
    def parse_file(inputfile: str, outputfile: str):
        with open(inputfile) as infile:
            data = json.load(infile)
            with open(outputfile, 'w') as outfile:
                json.dump(data, outfile)

    pull_file('http://dataserver/sales.json', 'latestsales.json')
    # Call the parse_file task
    parse_file('latestsales.json', 'latestsales_parsed.json')

process_sales()
```

### Ejecuciones de DAG
- Una instancia de un flujo de trabajo en un momento dado
- Puede ejecutarse manualmente o via schedule
- Mantiene estado para cada flujo y sus tareas:
    - running
    - failed
    - success
    - queued
    - skipped

`start_date` -> Fecha y hora inicial para ejecutar un dag
es un objeto datetime de pendulum.
`end_date` -> Fecha u hora cuando dejar de crear nuevas instancias del DAG (es opcional) 

```python
from pendulum import datetime
start_date = datetime(2026,4,10, tz='UTC')
```
Schedule
- schedule indica con que frecuencia se programa el dag
- entre start_date y end_date
- se define con sintaxis *cron*

#### CRON
| minuto| hora| dia del mes| mes |dia de la semana|
|-------|-----|------------|-----|----------------| 
| *     |   * |        *   |  *  |        *       |

```bash
0 12 * * * # Ejecutar a diario al mediodia
* * 25 2 * # Ejecutar cada minuto el 25 de febrero
0,15,30,45 * * * * # Ejecutar cada 15 minutos
```
Presets:
```bash
@hourly == 0 * * * *
@daily  == 0 0 * * *
@weekly == 0 0 * * 0
@monthly == 0 0 1 * *
@yearly == 0 0 1 1 *

None == #No programar nunca
@once == #Programar solo una vez
@continuous == #Ejecutar en cuanto termine la ejecución previa.
```
Timedelta
```python
from pendulum import duration

@dag(
    dag_id = 'example_dag',
    schedule=duration(days=2)
    schedule='0 12 * * *',
    schedule='@daily'
) # Cualquiera de estas nomenclaturas es valida
```

**Nota**
Un DAG con start_date=datetime(2026, 2, 25, tz='UTC')
schedule='@daily'

la primera ejecución posible es el 26 de Febrero

## XCom
XCom es la abreviatura de comunicación cruzada.
Sirve para que las tareas pueden enviarse datos entre ellas, lo que indica que debe ser pequeño es que residen en la base de metadatos de airflow.
(nombre de archivos, URIs o recuentos de filas)

```python
@dag(dag_id='Example_XCom')
def example_xcom():  
    @task
    def get_data():
        return data  
    @task(multiple_outputs=True)
    def clean_data(sourcedata):
        return clean(sourcedata) 
        # Example, not implemented  
    clean_data(get_data())  
    
example_xcom()
```
Para definir realmente el XCom, debemos pasar los datos de una tarea (get_data) a otra (clean_data). Usamos la misma sintaxis que si llamáramos funciones de forma similar; en este caso, clean_data(get_data()).

Conceptualmente clean_data depende de get_data y posteriormente podemos definir

```python
result = clean_data(get_data()) 
result >> alert_when_complete()
```
Example:
```python
@dag(start_date=datetime(2026,4,1))
def etl_example():
    # Chain extract, transform, and load, assigning the result
    etl_result = load(transform(extract()))
    # Run send_report after the ETL tasks
    etl_result >> send_report()
    
etl_example()
```

## Sensors
Un sensor es un tipo de operador que espera a que se cumpla una condición.
- crear un archivo
- subir un registro a una bd
- respuesta de un web request

**Detalles de los sensores**
Derivan de la clase `airflow.sdk.BaseSensorOperator`
Argumentos:
- ``mode`` - Como se va a revisar la condicion
    - ``mode='poke'`` default, se ejecuta repetidamente
    - ``mode='reschedule'`` cede el turno e intenta después
- `poke_interval` cuanto esperar entre chequeo (si el modo es poke)
- `timeout` cuanto esperar antes de marcar la tarea como fallida

**FileSensor**
`airflow.providers.standard.sensor`
Comprueba la existencia de un archivo en cierta ubicación.
Puede revisar si existe algun archivo en el directorio.

```python
from airflow.providers.standard.sensors.filesystem import FileSensor

file_sensor_task = FileSensor(task_id='file_sense',
                                filepath='salesdata.csv',
                                poke_interval=300,
                                timeout=300)

init_sales_cleanup() >> file_sensor_task >> generate_report()                            
```

Otros sensores
- `airflow.providers.*.sensors`
- `ExternalTaskSensor` espera a una tarea en otro dag
- `HttpSensor` solicita una web url y revisa su contenido
- `SqlSensor` corre un query y revisa su contenido

Example
```python
# Import the FileSensor class
from airflow.providers.standard.sensors.filesystem import FileSensor

# Set the file sensor to an alias
precheck = FileSensor(
  task_id='check_for_datafile',
  # Wait for this file to exist before continuing
  filepath='salesdata_ready.csv',
  timeout=300,
  mode="reschedule"
)
```

### DAG Lifecycle 
![nota_1](img/Captura%20de%20pantalla%202026-09-04%20091358.png)

### Callbacks
Son funciones en un DAG o en una Task que Airflow llama automaticamente.
Callbacks para transiciones de estado especificas:
- on_failure_callback
- on_success_callback

Task specific callbacks:
- on_retry_callback
- on_skipped_callback
- on_execute_callback

### Callback Context
Airflow permite pasar un contexto automaticamente (diccionario)
`context` contiene metadata del dag/task
- `context['dag'].dag_id` Nombre del dag
- `context['task_instane'].task_id` Nombre de la task
- `context['logical_date']` fecha de ejecución del dag

Las funcionesdeben acceptar un parametro contexto
```python
def alert_on_failure(context):    
    dag_id = context["dag"].dag_id    
    task_id = context["task_instance"].task_id
    print(f"Task {task_id} in DAG {dag_id} has failed.")

@dag(on_failure_callback=alert_on_failure)
def sales_etl_dag():    
    @task()
    def data_import_task():
        raise ValueError("Simulated failure")

# Task data_import_task in Dag sales_etl_dag has failed.
```

### Notifiers
Functions that can be tied to callbacks
- Send alerts to external systems
- Several notifiers available:
- `SmtpNotifier` - Sends email alerts
- `SlackNotifier` - Posts messages to a Slack channel

**SmtpNotifier**
In the `airflow.providers.smtp.notifications.smtp` library 

```python
from airflow.providers.smtp.notifications.smtp import SmtpNotifier
@dag(dag_id=`sales_etl_dag`,
    on_failure_callback=SmtpNotifier( 
              to='me@datacamp.com',       
              from_email='airflow_server@datacamp.com',       
              subject='Dag sales_etl_dag has failed'
              )
    )
```

### Template Jinja
Airflow Jinja functions
- `logical_date`: When a Dag run occurs
- `ds`: The logical_date in YYYY-MM-DD format
- `logical_date.year`, `logical_date.month`, `logical_date.day`: Access the date components
- `params`: The runtime parameters of the Dag run

Calculations, loops, and moremacros.
- `ds_add`: Allows date calculations

```python
@dag(dag_id=`sales_etl`, 
    on_failure_callback=SmtpNotifier( 
                to='me@datacamp.com', 
                from_email='airflow_server@datacamp.com',
                subject='sales_etl on {{ logical_date }} has failed!'     
                )
    )
```




