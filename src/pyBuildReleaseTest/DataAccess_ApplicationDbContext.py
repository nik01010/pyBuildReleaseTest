import pyodbc

class ApplicationDbContext:
    def __init__(
        self, 
        connection_driver: str = "ODBC Driver 17 for SQL Server", 
        connection_server: str = "localhost", 
        connection_database: str = "master"
    ):
        # TODO: add validations
        # TODO: add logging
        self._connection_driver: str = connection_driver
        self._connection_server: str = connection_server
        self._connection_database: str = connection_database

        self._connection_string: str = self._get_connection_string()

        self.database_connection: pyodbc.Connection = self._create_database_connection()
    
    def _get_connection_string(self):
        # TODO: add logging
        connection_string: str = f'DRIVER={self._connection_driver};SERVER={self._connection_server};DATABASE={self._connection_database};Trusted_Connection=yes;'
        print(connection_string)

        return(connection_string)
    
    def _create_database_connection(self) -> pyodbc.Connection:
        # TODO: add logging
        # TODO: add error handling
        database_connection: pyodbc.Connection = pyodbc.connect(self._connection_string)
        
        return(database_connection)

    def close_database_connection(self) -> None:
        # TODO: add logging
        self.database_connection.close()
