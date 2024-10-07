import pyodbc

class ApplicationDbContext:
    def __init__(self, connection_driver = "ODBC Driver 17 for SQL Server", connection_server = "localhost", connection_database = "master"):
        # TODO: add validations
        # TODO: add logging
        self._connection_driver = connection_driver
        self._connection_server = connection_server
        self._connection_database = connection_database

        self._connection_string = self._get_connection_string()

        self.database_connection = self._create_database_connection()
    
    def _get_connection_string(self):
        # TODO: add logging
        connection_string = f'DRIVER={self._connection_driver};SERVER={self._connection_server};DATABASE={self._connection_database};Trusted_Connection=yes;'
        print(connection_string)

        return(connection_string)
    
    def _create_database_connection(self):
        # TODO: add logging
        # TODO: add error handling
        database_connection = pyodbc.connect(self._connection_string)
        
        return(database_connection)

    def close_database_connection(self):
        # TODO: add logging
        self.database_connection.close()
