import psycopg2

class PostgresDB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='pipelines',
                user='postgres',
                password='Ng1w6foxgr',
                host='db',
                port='5432'
            )
            print("Connected to database")
        except Exception as e:
            print(f"Unable to connect to the database: {e}")

    def query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
        except Exception as e:
            print(f"Query execution failed: {e}")

    def load_data(self, table_name, data):
        try:
            cursor = self.conn.cursor()
            cursor.copy_expert(f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER", open(data, "r"))
            print("Data loaded successfully")
        except Exception as e:
            print(f"Unable to load data into the table: {e}")

    def copy_to_file(self, table_name, file_path):
        try:
            cursor = self.conn.cursor()
            with open(file_path, 'w') as file:
                cursor.copy_to(file, table_name)
            print(f"Data from table {table_name} copied to file {file_path} successfully")
        except Exception as e:
            print(f"Unable to copy data to file: {e}")

    def close(self):
        try:
            self.conn.close()
            print("Connection closed")
        except Exception as e:
            print(f"Unable to close connection: {e}")