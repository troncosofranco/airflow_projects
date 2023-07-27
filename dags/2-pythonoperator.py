from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_python():
    print("Hola Gente de Python")

with DAG(dag_id="pythonperator",
        description="Primer DAG con Python operator",
        schedule_interval='@once',
        start_date=datetime(2023,7,27)) as dag:
    
    t1 = PythonOperator(task_id="hello_with_python" ,
                    python_callable=hello_python)
    t1