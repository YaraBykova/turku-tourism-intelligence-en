import subprocess
import sys
from datetime import timedelta

import pendulum
from airflow.sdk import Param, dag, get_current_context, task


@task(
    retries=2,
    retry_delay=timedelta(minutes=1),
    execution_timeout=timedelta(minutes=5),
)
def run_script(script):
    context = get_current_context()

    if (
        script == "ingestion/statfin.py"
        and context["params"]["simulate_source_failure"]
    ):
        raise RuntimeError("TEST: simulated failure before StatFin request.")

    subprocess.run(
        [sys.executable, script],
        cwd="/opt/turku",
        check=True,
    )


@dag(
    dag_id="turku_tourism",
    schedule="20 1 * * *",
    start_date=pendulum.datetime(2026, 11, 18, tz="Europe/Moscow"),
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
    tags=["turku", "tourism"],
    params={
        "simulate_source_failure": Param(
            False,
            type="boolean",
            title="Simulate failure of the extraction task",
        ),
    },
)
def tourism_pipeline():
    extract = run_script.override(task_id="extract_statfin")(
        "ingestion/statfin.py"
    )
    quality = run_script.override(
        task_id="check_data_quality",
        retries=0,
    )("ingestion/check_statfin_quality.py")

    load = run_script.override(task_id="load_postgres")(
        "ingestion/load_statfin_postgres.py"
    )

    marts = run_script.override(task_id="build_marts")(
        "ingestion/build_marts.py"
    )

    plot = run_script.override(task_id="plot_seasonality")(
        "analysis/plot_seasonality.py"
    )

    monthly_change = run_script.override(
        task_id="plot_monthly_change"
    )(
        "analysis/plot_monthly_change.py"
    )

    segment_seasonality = run_script.override(
        task_id="plot_segment_seasonality"
    )(
        "analysis/plot_segment_seasonality.py"
    )

    (
        extract
        >> quality
        >> load
        >> marts
        >> plot
        >> monthly_change
        >> segment_seasonality
    )


tourism_pipeline()
