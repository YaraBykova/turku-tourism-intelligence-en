FROM apache/airflow:slim-3.4.0-python3.14

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "matplotlib==3.11.2" \
    "psycopg[binary]==3.3.9" \
    "python-dotenv==1.2.4"

RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/pip install --no-cache-dir \
       "dbt-core==1.12.7" \
       "dbt-postgres==1.11.0"