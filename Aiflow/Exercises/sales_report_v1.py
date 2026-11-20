# Import PartitionedAssetTimetable and StartOfDayMapper
from airflow.sdk import dag, task, Asset, CronPartitionTimetable, PartitionedAssetTimetable, StartOfDayMapper
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

daily_sales = Asset("daily_sales")


# --- Upstream: partitioned sales load (from previous exercise) ---
@dag(schedule=CronPartitionTimetable("0 0 * * *", timezone="UTC"), template_searchpath="/home/repl/workspace/include/sql")
def sales_pipeline_v3():
    SQLExecuteQueryOperator(
        task_id="load_daily_sales",
        conn_id="duckdb_analytics",
        outlets=[daily_sales],
        sql="aggregate_sales.sql",
    )

upstream = sales_pipeline_v3()


# --- Downstream: report triggered by partitioned asset event ---
# Schedule on partitioned daily_sales events with StartOfDayMapper
@dag(schedule=PartitionedAssetTimetable(
    assets=daily_sales,
    partition_mapper_config={daily_sales: StartOfDayMapper()}
))
def sales_report():

    @task
    def generate_report(dag_run=None):
        # Read the partition key from the Dag run
        partition_key = dag_run.partition_key
        print(f"Generating report for partition: {partition_key}")

    generate_report()

downstream = sales_report()


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
        upstream.test()
