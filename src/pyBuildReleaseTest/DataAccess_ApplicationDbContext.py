from dataclasses import dataclass
from sqlalchemy import create_engine, Engine, Connection, MetaData, Integer, NCHAR, NVARCHAR, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

@dataclass(frozen = True)
class ConnectionDetails:
    server: str
    database: str
    driver: str

    def get_connection_string(self) -> str:
        connection_string: str = f"mssql+pyodbc://{self.server}/{self.database}?trusted_connection=yes&driver={self.driver}"
        return connection_string

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "Person"
    __table_args__ = {"schema": "Person"}

    BusinessEntityID: Mapped[int] = mapped_column(Integer, primary_key = True, nullable = False)
    PersonType: Mapped[str] = mapped_column(NCHAR(2), nullable = False)
    NameStyle: Mapped[bool] = mapped_column(Boolean, nullable = False)
    Title: Mapped[str] = mapped_column(NVARCHAR(8), nullable = True)
    FirstName: Mapped[str] = mapped_column(NVARCHAR(50), nullable = False)
    MiddleName: Mapped[str] = mapped_column(NVARCHAR(50), nullable = True)
    LastName: Mapped[str] = mapped_column(NVARCHAR(50), nullable = False)
    Suffix: Mapped[str] = mapped_column(NVARCHAR(10), nullable = True)
    EmailPromotion: Mapped[int] = mapped_column(Integer, nullable = False)
    AdditionalContactInfo: Mapped[str] = mapped_column(String, nullable = True)
    Demographics: Mapped[str] = mapped_column(String, nullable = True)
    rowguid: Mapped[str] = mapped_column(String, nullable = False)
    ModifiedDate: Mapped[datetime] = mapped_column(DateTime, nullable = False)

    def __repr__(self) -> str:
        text = f"[Id {self.BusinessEntityID}] [{self.FirstName} {self.LastName}] [guid: {self.rowguid}]"
        return text

class ApplicationDbContext:
    def __init__(self, connection_details: ConnectionDetails) -> None:
        # TODO: add validations
        # TODO: add logging and error handling
        self._connection_string: str = connection_details.get_connection_string()
        self.connection_engine: Engine = self._create_connection_engine()
        self.database_connection: Connection = self._create_database_connection()
        self.database_metadata: MetaData = self._get_database_metadata()
    
    def _create_connection_engine(self) -> Engine:
        # TODO: add logging and error handling
        connection_engine: Engine = create_engine(self._connection_string)
        return connection_engine

    def _create_database_connection(self) -> Connection:
        # TODO: add logging and error handling
        database_connection: Connection = self.connection_engine.connect()
        return database_connection     
    
    def _get_database_metadata(self) -> MetaData:
        # TODO: add logging and error handling
        database_metadata: MetaData = MetaData()
        return database_metadata

    def disconnect(self) -> None:
        # TODO: add logging and error handling
        # TODO: check if sessions need to be closed
        self.database_connection.close()
        self.connection_engine.dispose()
