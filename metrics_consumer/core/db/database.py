from psycopg2 import connect
from psycopg2.extensions import connection


class DB:
    """
    Represents DB connections handling
    """
    _conn: connection = None

    def connect_with(self, host: str, port: str, dbname: str, user: str, password: str) -> connection:
        """
        Connect to DB and returns connection object
        """

        if not self._conn:
            params = {
                'host': host,
                'port': port,
                'user': user,
                'password': password,
            }
            if dbname:
                params['dbname'] = dbname

            self._conn = connect(**params)

        return self._conn

    def close_connection(self):
        if self._conn is not None:
            self._conn.close()


db = DB()
