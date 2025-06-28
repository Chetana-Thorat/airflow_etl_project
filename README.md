# 🧩 Airflow ETL Pipeline

---

## 🚀 Overview

- **Goal:** Read raw sales data from a CSV, calculate total sales per region, and store the summary in a PostgreSQL table.
- **Tech Stack:** Apache Airflow · PostgreSQL · Docker · Python (Pandas)

---

## 🛠 Technologies Used

- **Apache Airflow** (DAGs, PythonOperator, PostgresOperator)
- **PostgreSQL** (as ETL target)
- **Docker & Docker Compose** (container orchestration)
- **Pandas** (data transformation)

---

### 📁 Project Structure

airflow-etl-project/
├── dags/
│ └── sales_etl.py # Airflow DAG definition
├── data/
│ └── sales_raw.csv # Raw sales input file
├── docker-compose.yaml # Docker setup for Airflow & Postgres
├── .gitignore
└── README.md

---

## 🙌 Author

Chetana Thorat  
📧 thoratchetana8@gmail.com  
📌 [LinkedIn](https://www.linkedin.com/in/chetana-thorat/) | [GitHub](https://github.com/Chetana-Thorat)


### 📌 How It Works
1. Reads `sales_raw.csv`
2. Aggregates total sales per region
3. Stores the results in a Postgres table `sales_summary`

---

## 📸 Screenshots

### ✅ DAG Success in Airflow
![DAG Success](./screenshots/airflow_dag_success.png)

### 🔍 Task Logs
![Task Logs](./screenshots/task_logs.png)

### 📊 PGAdmin Table Output
![Table View](./screenshots/pgadmin_table_view.png)

### 🧱 Etl_detail
![Docker Terminal](./screenshots/airflow_etl_detail.png)

---

## 🧠 Learnings

✅ How to define DAGs using Airflow  
✅ How to use PythonOperator and PostgresOperator  
✅ Writing idempotent ETL logic  
✅ Triggering and monitoring tasks via the Airflow UI  
✅ Interacting with PostgreSQL using PGAdmin

---
