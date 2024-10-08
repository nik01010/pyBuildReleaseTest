import pyodbc
from dataclasses import dataclass

@dataclass(frozen = True)
class ConnectionDetails:
    connection_driver: str
    connection_server: str
    connection_database: str

    def get_connection_string(self):
        connection_string: str = f'DRIVER={self.connection_driver};SERVER={self.connection_server};DATABASE={self.connection_database};Trusted_Connection=yes;'

        return(connection_string)

class ApplicationDbContext:
    def __init__(self, connection_details: ConnectionDetails) -> None:
        # TODO: add validations

        # TODO: add logging
        self._connection_string: str = connection_details.get_connection_string()

        self.database_connection: pyodbc.Connection = self._create_database_connection()
    
    def _create_database_connection(self) -> pyodbc.Connection:
        # TODO: add logging
        # TODO: add error handling
        # TODO: refactor using SQLAlchemy ORM
        # https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
        database_connection: pyodbc.Connection = pyodbc.connect(self._connection_string)
        
        return(database_connection)

    def close_database_connection(self) -> None:
        # TODO: add logging
        self.database_connection.close()
