from dataclasses import dataclass
from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session
from logging import getLogger, Logger


logger: Logger = getLogger(__name__)

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
        logger.debug(f"Database context using connection string: {connection_string}")

        self.connection_string: str = connection_string
        self.connection_engine: Engine = self._create_connection_engine()
        self.database_connection: Connection = self._create_database_connection()
        self.session: Session = self._create_session()

        logger.debug("Created database connection")

    def _create_connection_engine(self) -> Engine:
        try:
            connection_engine: Engine = create_engine(self.connection_string)
        except Exception as error:
            logger.error(f"Error creating connection engine with message: {repr(error)}")
            raise
        return connection_engine

    def _create_database_connection(self) -> Connection:
        try:
            database_connection: Connection = self.connection_engine.connect()
        except Exception as error:
            logger.error(f"Error creating database connection with message: {repr(error)}")
            raise
        return database_connection
    
    def _create_session(self) -> Session:
        try:
            session: Session = Session(bind = self.connection_engine)
        except Exception as error:
            logger.error(f"Error creating database session with message: {repr(error)}")
            raise
        return session

    def disconnect(self) -> None:
        try:
            self.session.close()
            self.database_connection.close()
            self.connection_engine.dispose()
        except Exception as error:
            logger.error(f"Error disconnecting from database with message: {repr(error)}")
            raise
