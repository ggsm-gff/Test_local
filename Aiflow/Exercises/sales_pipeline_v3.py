# Import CronPartitionTimetable and Asset
from airflow.sdk import dag, task, Asset, CronPartitionTimetable
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Define the daily_sales asset
daily_sales = Asset("daily_sales")


# Schedule with CronPartitionTimetable
@dag(schedule=CronPartitionTimetable("0 0 * * *", timezone="UTC"), template_searchpath="/home/repl/workspace/include/sql")
def sales_pipeline_v3():

    load = SQLExecuteQueryOperator(
        task_id="load_daily_sales",
        conn_id="duckdb_analytics",
        # Emit a partitioned asset event
        outlets=[daily_sales],
        sql="aggregate_sales.sql",
    )

    read_results = SQLExecuteQueryOperator(
        task_id="read_results",
        conn_id="duckdb_analytics",
        sql="SELECT * FROM daily_summary ORDER BY order_date",
    )

    @task
    def send_report(results):
        for row in results:
            print(f"Date: {row[0]} | Orders: {row[1]} | Revenue: ${row[2]:.2f}")

    load >> read_results >> send_report(read_results.output)


pipeline = sales_pipeline_v3()

if __name__ == "__main__":
    # Workaround: dag.test() does not set a partition_key.
    # We inject one so the CronPartitionTimetable Dag can run.
    from unittest.mock import patch
    from airflow.serialization.definitions.dag import SerializedDAG

    _orig_create_dagrun = SerializedDAG.create_dagrun

    def _create_dagrun_with_partition_key(self, *args, **kwargs):
        kwargs["partition_key"] = "2026-04-23T00:00:00"
        return _orig_create_dagrun(self, *args, **kwargs)

    with patch.object(SerializedDAG, "create_dagrun", _create_dagrun_with_partition_key):
        pipeline.test()
