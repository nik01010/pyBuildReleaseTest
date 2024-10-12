from dataclasses import dataclass
from sqlalchemy import create_engine, Engine, Connection

@dataclass(frozen = True)
class ConnectionDetails:
    server: str
    database: str
    driver: str

    def get_connection_string(self) -> str:
        connection_string: str = f"mssql+pyodbc://{self.server}/{self.database}?trusted_connection=yes&driver={self.driver}"
        return(connection_string)

class ApplicationDbContext:
    def __init__(self, connection_details: ConnectionDetails) -> None:
        # TODO: add validations
        # TODO: add logging
        self._connection_string: str = connection_details.get_connection_string()
        self.connection_engine: Engine = self._create_connection_engine()
        self.database_connection: Connection = self._create_database_connection()
    
    def _create_connection_engine(self) -> Engine:
        connection_engine: Engine = create_engine(self._connection_string)
        return(connection_engine)

    def _create_database_connection(self) -> Connection:
        # TODO: add logging
        # TODO: add error handling
        database_connection: Connection = self.connection_engine.connect()
        return(database_connection)

    def close_database_connection(self) -> None:
        # TODO: add logging
        self.database_connection.close()
        self.connection_engine.dispose()
