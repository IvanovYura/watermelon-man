from typing import List

from psycopg2 import extras
from psycopg2.extensions import connection

SQL_INSERT_METRICS = '''
    INSERT INTO os_metrics(timestamp, metrics)
    VALUES (%(timestamp)s, %(metrics)s);        
'''

SQL_CREATE_TABLE = '''
    CREATE TABLE IF NOT EXISTS os_metrics (
        id serial,
        timestamp timestamp NOT NULL,
        metrics jsonb NOT NULL,
        PRIMARY KEY (id)
    );
'''


def insert_metrics(conn: connection, metrics: List[dict]):
    if not metrics:
        return

    with conn.cursor() as cursor:
        extras.execute_batch(cursor, SQL_INSERT_METRICS, metrics)
        conn.commit()


def create_table(conn: connection):
    with conn.cursor() as cursor:
        cursor.execute( SQL_CREATE_TABLE)
