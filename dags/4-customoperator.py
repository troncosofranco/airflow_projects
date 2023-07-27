from airflow import DAG
from datetime import datetime
from hellooperator import HelloOperator

with DAG(dag_id="customoperator",
        description="Primer custom_operator",
        start_date=datetime(2023,7,26)) as dag:
    
    t1= HelloOperator(task_id="hello",
                    name = "John")
    
    t1