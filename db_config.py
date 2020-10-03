postgres_url = '192.168.0.105:5432'
postgres_user = "postgres"
postgres_db = 'Task_Manager'
postgres_pw = '1'


db_url = f'postgresql+psycopg2://{postgres_user}:{postgres_pw}@{postgres_url}/{postgres_db}'
