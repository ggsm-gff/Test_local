# Enfoque con params, no seguro frente a inyecciones sql

SQLExecuteQueryOperator(
    sql="SELECT * FROM orders WHERE product = '{{ params.product }}'",
    params={"product": user_input},
)

# Enfoque con parameters, seguro frente a inyecciones sql, se procesa en la DB
SQLExecuteQueryOperator(
    sql="SELECT * FROM orders WHERE product = $product",
    parameters={"product": user_input},
)

