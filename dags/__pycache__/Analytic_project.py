#1.Import airflow modules
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

#2. Import python libraries
from datetime import datetime, date
import pandas as pd

#3. Define functions
def generate_data(**kwargs):
    data = pd.DataFrame({"student": ["Maria Cruz", "Daniel Crema",
    "Elon Musk", "Karol Castrejon", "Freddy Vega"],
    "timestamp": [kwargs['logical_date'],
    kwargs['logical_date'], kwargs['logical_date'], kwargs['logical_date'],
    kwargs['logical_date']]})
    data.to_csv(f"/tmp/platzi_data_{kwargs['ds_nodash']}.csv",
    header=True)

#4. Default args
default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 2, 9),
    'depends_on_past': False, 
    'email_on_failure': False, 
    'email_on_retry': False, 
    'retries': 1}


with DAG(dag_id="space_exploration",
    schedule_interval="@daily",
	default_args=default_args
) as dag:

    task_1= BashOperator(task_id = "nasa_confirmation_response",
                      bash_command='sleep 20 && echo "Confirmed NASA response" > /tmp/response_{{ds_nodash}}.txt')
    
    task_2 = BashOperator(task_id = "read_nada_response_data",
                        bash_command='ls /tmp && head /tmp/response_{{ds_nodash}}.txt')
    
    task_3 = BashOperator(task_id="obtain_spacex_data",
                    bash_command="curl https://api.spacexdata.com/v4/launches/past > /tmp/spacex_{{ds_nodash}}.json")

    task_4 = PythonOperator(task_id="satellite_response",
                    python_callable=generate_data)
    
    task_5 = BashOperator(task_id = "read_satellite_response_data",
                    bash_command='ls /tmp && head /tmp/platzi_data_{{ds_nodash}}.csv')

    email = EmailOperator(task_id='notify_analysts',
                    to = ['email@domain.com', 'email@domain.com'],
                    subject = "Notification Satellite Data",
                    html_content = "The data is available")                 

    task_1 >> task_2 >> task_3 >> task_4 >> task_5 >> email