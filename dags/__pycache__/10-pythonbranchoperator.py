from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, date

default_args = {
'start_date': datetime(2022, 7, 1),
'end_date': datetime(2022, 8, 1)
}

#Logical node
#**context: access to task variables
def _choose(**context):

    #logical_data: execution date
    if context["logical_date"].date() < date(2022, 7, 15):
        return "finish_22_june" #task ID to execute
    return "start_23_june" #task ID to execute

with DAG(dag_id="10-branching",
    schedule_interval="@daily",
	default_args=default_args
) as dag:

    branching = BranchPythonOperator(task_id="branch",
	                                 python_callable=_choose)

    finish_22 = BashOperator(task_id="finish_22_june",
	                         bash_command="echo 'Running {{ds}}'")

    start_23 = BashOperator(task_id="start_23_june",
	                        bash_command="echo 'Running {{ds}}'")

    branching >> [finish_22, start_23]