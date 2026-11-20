from airflow.sdk import dag, task
# Import SQLExecuteQueryOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(schedule="@daily")
def sales_pipeline():

    # Aggregate raw orders into the daily summary table
    aggregate = SQLExecuteQueryOperator(
        task_id="aggregate_daily_sales",
        conn_id="duckdb_analytics",
        sql="""
            INSERT INTO daily_summary (order_date, total_orders, total_revenue)
            SELECT order_date, COUNT(*), SUM(revenue)
            FROM raw_orders
            GROUP BY order_date
        """,
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


pipeline = sales_pipeline()

if __name__ == "__main__":
    pipeline.test()
