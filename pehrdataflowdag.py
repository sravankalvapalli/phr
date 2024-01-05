import os
import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from fhirdataflow import FhirDataFlow

# default_args = {
#     "owner": "airflow",
#     "start_date": datetime(2023, 12, 7),
#     "schedule_interval": None,
#     "depends_on_past": False,
#     "email": ["airflow@example.com"],
#     "retries": 3,
#     "retry_delay": timedelta(minutes=5),
# }

# dag = DAG(
#     'tempus_pehr_dag',
#     default_args=default_args,
#     description='A simple Airflow DAG',
#     schedule_interval=timedelta(days=1),  # Run the DAG daily
# )

# # Define a Python function to be executed by a task
# def run_pipeline():
#     FhirDataFlow.run_pipeline()

# # Create a task using the PythonOperator and associate it with the DAG
# task_hello = PythonOperator(
#     task_id='run_pipeline',
#     python_callable=run_pipeline,
#     dag=dag,
# )

if __name__ == "__main__":
    print('Started processing fhir patient dag')
    FhirDataFlow.run_pipeline()
    print('Complted processing fhir patient dag')
