import os
from pathlib import Path
from dotenv import load_dotenv
from .DB import PostgresDB

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.abspath(BASE_DIR / 'config' / '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
db = PostgresDB()


class BaseTask:
    """Base Pipeline Task"""

    def run(self):
        raise RuntimeError('Do not run BaseTask!')

    def short_description(self):
        pass

    def __str__(self):
        task_type = self.__class__.__name__
        return f'{task_type}: {self.short_description()}'


class CopyToFile(BaseTask):
    """Copy table data to CSV file"""

    def __init__(self, table, output_file):
        self.table = table
        self.output_file = output_file

    def short_description(self):
        return f'{self.table} -> {self.output_file}'

    def run(self):
        db.copy_to_file(self.table, self.output_file)
        print(f"Copy table `{self.table}` to file `{self.output_file}`")


class LoadFile(BaseTask):
    """Load file to table"""

    def __init__(self, table, input_file, cols):
        self.table = table
        self.input_file = input_file
        self.cols = cols

    def short_description(self):
        return f'{self.input_file} -> {self.table}'

    def run(self):
        columns = ', '.join([f'{col} varchar' for col in self.cols])
        db.query(f"CREATE TABLE IF NOT EXISTS {self.table} (id SERIAL PRIMARY KEY, {columns})")
        db.load_data(self.table, self.input_file)
        print(f"Load file `{self.input_file}` to table `{self.table}`")


class RunSQL(BaseTask):
    """Run custom SQL query"""

    def __init__(self, sql_query, title=None):
        self.title = title
        self.sql_query = sql_query

    def short_description(self):
        return f'{self.title}'

    def run(self):
        db.query(self.sql_query)
        print(f"Run SQL ({self.title}):\n{self.sql_query}")


class CTAS(BaseTask):
    """SQL Create Table As Task"""

    def __init__(self, table, sql_query, title=None):
        self.table = table
        self.sql_query = sql_query
        self.title = title or table

    def short_description(self):
        return f'{self.title}'

    def run(self):
        db.query(
            f'''CREATE TABLE IF NOT EXISTS {self.table} 
                        (id SERIAL PRIMARY KEY, name varchar, url varchar, domain_of_url varchar)''')

        db.query('drop function if exists domain_of_url(varchar)')

        db.query('''CREATE FUNCTION domain_of_url(url varchar) RETURNS varchar AS $$
                                DECLARE
                                    domain varchar;
                                BEGIN
                                    select substring(url from '.*://([^/]*)') into domain;
                                    return domain;
                                END;
                                $$ LANGUAGE plpgsql;
                            ''')

        db.query(f'insert into {self.table} ({self.sql_query})')
        print(f"Create table `{self.table}` as SELECT:\n{self.sql_query}")
