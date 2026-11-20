from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


# Set the template search path, so Airflow finds SQL files
@dag(schedule="@daily", template_searchpath="/home/repl/workspace/include/sql/")
def sales_pipeline_v2():

    # Reference the external SQL file instead of inline SQL
    aggregate = SQLExecuteQueryOperator(
        task_id="aggregate_daily_sales",
        conn_id="duckdb_analytics",
        sql="aggregate_sales.sql",
    )

    # Read back the results to verify
    read_results = SQLExecuteQueryOperator(
        task_id="read_results",
        conn_id="duckdb_analytics",
        sql="SELECT * FROM daily_summary ORDER BY order_date",
    )

    @task
    def send_report(results):
        for row in results:
            print(f"Date: {row[0]} | Orders: {row[1]} | Revenue: ${row[2]:.2f}")

    aggregate >> read_results >> send_report(read_results.output)


pipeline = sales_pipeline_v2()

if __name__ == "__main__":
    pipeline.test()
