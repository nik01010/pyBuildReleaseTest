from dataclasses import dataclass
from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session

@dataclass(frozen = True)
class ConnectionDetails:
    server: str
    database: str
    driver: str

    def get_connection_string(self) -> str:
        connection_string: str = f"mssql+pyodbc://{self.server}/{self.database}?trusted_connection=yes&driver={self.driver}"
        return connection_string

class ApplicationDbContext:
    def __init__(self, connection_string: str) -> None:
        # TODO: add validations
        # TODO: add logging and error handling
        self.connection_string: str = connection_string
        self.connection_engine: Engine = self._create_connection_engine()
        self.database_connection: Connection = self._create_database_connection()
        self.session: Session = self._create_session()

    def _create_connection_engine(self) -> Engine:
        # TODO: add logging and error handling
        connection_engine: Engine = create_engine(self.connection_string)
        return connection_engine

    def _create_database_connection(self) -> Connection:
        # TODO: add logging and error handling
        database_connection: Connection = self.connection_engine.connect()
        return database_connection
    
    def _create_session(self) -> Session:
        session: Session = Session(bind = self.connection_engine)
        return session

    def disconnect(self) -> None:
        # TODO: add logging and error handling
        self.session.close()
        self.database_connection.close()
        self.connection_engine.dispose()
