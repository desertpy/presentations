from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 10, 14),
    'email': ['godber@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
}

dag = DAG('plot-phx-gsod', default_args=default_args)

t1 = BashOperator(
    task_id='get_data',
    bash_command='wget ftp://ftp.ncdc.noaa.gov/pub/data/gsod/2018/722780-23183-2018.op.gz -O /srv/airflow/data/plot-phx-gsod/722780-23183-2018.op.gz',
    dag=dag
)

t2 = BashOperator(
    task_id='extract_data',
    bash_command='gunzip -fk /srv/airflow/data/plot-phx-gsod/722780-23183-2018.op.gz',
    retries=3,
    dag=dag
)

t3 = BashOperator(
    task_id='clean_data',
    bash_command='sed "s/\*/ /g" /srv/airflow/data/plot-phx-gsod/722780-23183-2018.op | tail -n +2 > /srv/airflow/data/plot-phx-gsod/temps.fwf',
    retries=3,
    dag=dag
)

# /srv/airflow/scripts/plot-temps.py /srv/airflow/data/plot-phx-gsod/temps.fwf 2018-10-14
t4 = BashOperator(
    task_id='plot_data',
    bash_command="/srv/airflow/scripts/plot-temps.py /srv/airflow/data/plot-phx-gsod/temps.fwf {{ds}}",
    dag=dag
)

t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
