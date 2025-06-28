from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd

# File path (inside Docker container)
RAW_FILE_PATH = '/opt/airflow/data/sales_raw.csv'

# DAG default settings
default_args = {
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    dag_id='sales_etl',
    schedule_interval=None,
    default_args=default_args,
    catchup=False
)

# Step 1: Create the destination table
create_table_query = """
CREATE TABLE IF NOT EXISTS sales_summary (
    region TEXT,
    total_sales INT
);
"""

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_conn',
    sql=create_table_query,
    dag=dag
)

# Step 2: Extract + Transform
def transform_data(**kwargs):
    df = pd.read_csv(RAW_FILE_PATH)
    summary = df.groupby('region')['sales'].sum().reset_index()
    summary.rename(columns={'sales': 'total_sales'}, inplace=True)
    
    # Convert to list of dicts for safe XCom transfer
    summary_list = summary.to_dict(orient='records')
    kwargs['ti'].xcom_push(key='summary_data', value=summary_list)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag
)

# Step 3: Load into PostgreSQL
def load_to_postgres(**kwargs):
    try:
        # Get data from XCom
        summary_list = kwargs['ti'].xcom_pull(task_ids='transform_data', key='summary_data')
        
        if not summary_list:
            raise ValueError("No data received from transform_data task.")

        # Log how many records we're about to insert
        print(f"Inserting {len(summary_list)} records into sales_summary...")

        hook = PostgresHook(postgres_conn_id='postgres_conn')
        conn = hook.get_conn()
        cursor = conn.cursor()

        for row in summary_list:
            print(f"Inserting row: {row}")
            cursor.execute(
                "INSERT INTO sales_summary (region, total_sales) VALUES (%s, %s);",
                (row['region'], row['total_sales'])
            )

        conn.commit()
        cursor.close()
        conn.close()
        print("Data loaded successfully into sales_summary.")

    except Exception as e:
        print(f"❌ Error in load_to_postgres: {str(e)}")
        raise


load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_to_postgres,
    provide_context=True,
    dag=dag
)

# Define task dependencies
create_table >> transform_task >> load_task
