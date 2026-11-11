## Spark and Databricks

RDD (Resilient Distributed Dataset) its a collection data type in spark  
    - The data is distributed across many "locations"  
    - Its the low level core of spark

DataFrame, its a distributed collection of data organized into named columns, similar to a table in sql  
    - They are "immutable and lazy evaluation"

Lazy Evaluation: Computations are optimized and executed only when an *Action* is triggered.  
    - Schema Awareness: The schema of a dataframe is known at runtime
    API cross languages.  
    - Built in optimization: Catalyst Optimizer


DataSet, strongly typed JVM based API available in Java and Scala
DataSets are a extension of DataFrames, provide a typesafe object oriented programming interface.
Every feature aplicable to DF are also aplicable to DSt
Additional features:
    TypeSafety: strong data type definition at compiled time
    Interoperability: Convert a DF to a DS by defining a class
    Performace: Benefits of Spark SQL engine (Catalyst Optimizer)

Use case scenarios:
    Python, R, high level abstraction, schema inferation -> DataFrame
    Java, Scala, Defined schema (TypeSafety), Complex Data Transformations-> DataSet

----

RDD need to use spark context  
            Spark Session -> hive or spark metastore session.  
            Spark Context include in hadoop and spark on premise  

As soon as a notebook is accesed, it allows to use 
"Spark" object that is a Spark Session and 
sc that is a Spark Context (Used when you want to work with RDD)

Functions over RDD are either:  
- Transformations:  
    - Filter
    - Map
    - groupByKey
    - reduceByKey
    - reduce
- Actions:   
    - Count
    - Collect
    - First
    - Take
    - SaveAsTextFile

### Narrow Transformation:  
This transformations are executed inside a single node, an input partition is processed and prodeced at most one output  
- Map  
- Filter  
- FlatMap  


### Nested Column  
In spark, a nested column is a column whose data type is a complex type, such a *StructType, ArrayType or MapType*  
```python
from pyspark.sql import Row

data = [Row(person=Row(name="Alice", age=30))]
df = spark.createDataFrame(data)
df.printSchema()
# root
#  |-- person: struct (nullable = true)
#  |    |-- name: string (nullable = true)
#  |    |-- age: long (nullable = true)
```
The way to rename it is the following:  
```python
from pyspark.sql.functions import col

df2 = df.withColumn(
    "person",
    col("person").withFieldRenamed("name", "full_name")
)
```

Add a new column to a DataFrame via PySpark:

```python
from pyspark.sql.functions import col

# Add a new column
df2 = df.withColumn('new_col',col('existing_col'))

#Update the values of an existing column
df2 = df.withColumn('existing_col',col('existing_col'))

# Add a constant value
from pyspark.sql.functions import lit
df2 = df.withColumn('constant_col', lit(10))

```

Add a new column to a DataFrame vía SparkSQL

```python
#Register a view to work with
df.createOrReplaceTempView('online_retail')

df2 = spark.sql('''
    select 
            t.*, existing_col + 1 as new_col
    from online_retail
''')

df2 = spark.sql('''
    select 
        t.*, existing_col * 1 as existing_col
    from online_retail
''')

```

To drop a column vía PySpark just use the df2 = df.drop(['col_name']) instruction

To drop a column vía SparkSQL list all the column except the one to drop.


**CASE WHEN** equivalent statement:
```python
from pyspark.sql.functions import when, col

df2 = df.withColumn(
    "new_col",
    when(col("score") >= 60, "pass").otherwise("fail")
)  

```  

**Common Spark Data Types:**

- StringType: Text data.
- IntegerType: 32-bit integer numbers.
- LongType: 64-bit integer numbers.
- FloatType: 32-bit floating point numbers.
- DoubleType: 64-bit floating point numbers.
- BooleanType: True/False values.
- DateType: Date (year, month, day).
- TimestampType: Date and time.
- DecimalType: Fixed precision decimal numbers.
- ArrayType: List/array of elements.
- MapType: Key-value pairs (dictionary).
- StructType: Complex/nested structure (like a JSON object).  
  
  
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
```


Basic Topics
-Spark DataFrame – Rename nested column
-How to add or update a column on DataFrame
-How to drop a column on DataFrame
-Spark when otherwise usage
-How to add literal constant to DataFrame
-Spark Data Types explained
How to change column data type
How to Pivot and Unpivot a DataFrame
Create a DataFrame using StructType & StructField schema
How to select the first row of each group
-How to sort DataFrame
How to union DataFrame
How to drop Rows with null values from DataFrame
How to split single to multiple columns
How to concatenate multiple columns
How to replace null values in DataFrame
How to remove duplicate rows on DataFrame
How to remove distinct on multiple selected columns
Spark map() vs mapPartitions()

Spark DataFrame Advanced concepts
Spark Partitioning, Repartitioning and Coalesce
How does Spark shuffle work?
Spark Cache and Persistence
Spark Persistance Storage levels
Spark Broadcast shared variable
Spark Accumulator shared variable
Spark UDF

Spark Array and Map operations
How to create an Array (ArrayType) column on DataFrame
How to create a Map (MapType) column on DataFrame
How to convert an Array to columns
How to create an Array of struct column
How to explode an Array and map columns
How to explode an Array of structs
How to explode an Array of map columns to rows
How to create a DataFrame with nested Array
How to explode nested Arrays to rows
How to flatten nested Array to single Array
Spark – Convert array of String to a String column

Spark Aggregate
How to group rows in DataFrame
How to get Count distinct on DataFrame
How to add row number to DataFrame
How to select the first row of each group

Spark SQL Joins
Spark SQL Join

Spark Performance
Spark Performance Improvement

Other Helpful topics on DataFrame
How to stop DEBUG & INFO log messages
Print DataFrame full column contents
Unstructured vs semi-structured vs structured files
Spark SQL Schema & StructType
How to convert case class to a schema

Spark Schema explained with examples
How to create array of struct column

Spark StructType & StructField
How to flatten nested column

Spark SQL Functions
Spark Date and Time Functions
Spark String Functions
Spark Array Functions
Spark Map Functions
Spark Aggregate Functions
Spark Window Functions
Spark Sort Functions

Spark Data Source with Examples

- Text  
Spark process Text file
How to process JSON from a Text file

- CSV  
How to process CSV file
How to convert Parquet file to CSV file
How to process JSON from a CSV file
How to Convert Avro file to CSV file
How to convert CSV file to Avro, Parquet & JSON

- JSON  
    - JSON Example (Read & Write)
    - How to Read JSON from multi-line
    - How to read JSON file with custom schema
    - How to process JSON from a CSV file
    - How to process JSON from a Text file
    - How to convert Parquet file to JSON file
    - How to convert Avro file to JSON file
    - How to convert JSON to Avro, Parquet, CSV file
- Parquet
    - Parquet Example (Read and Write)
    - How to convert Parquet file to CSV file
    - How to convert Parquet file to Avro file
    - How to convert Avro file to Parquet file
- Avro
    - Avro Example (Read and Write)
    - Spark 2.3 – Apache Avro Example
    - How to Convert Avro file to CSV file
    - How to convert Parquet file to Avro file
    - How to convert Avro file to JSON file
    - How to convert Avro file to Parquet file
- ORC
    - Spark Read & Write ORC
- XML
    - Processing Nested XML structured files
    - How to validate XML with XSD
- Hive & Tables
    - Spark Save DataFrame to Hive Table
    - Spark JDBC Parallel Read
    - Read JDBC Table to Spark DataFrame
    - Spark saveAsTable() with Examples
    - Spark Query Table using JDBC
    - Spark Read and Write MySQL Database Table
    - Spark with SQL Server – Read and Write Table
    - Spark spark.table() vs spark.read.table()