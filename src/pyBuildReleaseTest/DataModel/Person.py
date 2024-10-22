from sqlalchemy import ForeignKey, Integer, NCHAR, NVARCHAR, String, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
from datetime import datetime

# TODO: check if Person can inherit directly from DeclarativeBase without defining Base
class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "Person"
    __table_args__ = {
        "schema": "Person", 
        # The below is needed because returning a newly inserted Id in a table with triggers can cause errors
        # https://stackoverflow.com/questions/36109206/should-i-always-use-implicit-returningfalse-in-sqlalchemy
        'implicit_returning': False
    }

    BusinessEntityID: Mapped[int] = mapped_column(ForeignKey(BusinessEntity.BusinessEntityID), primary_key = True, nullable = False)
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
    rowguid: Mapped[str] = mapped_column(String, nullable = False, server_default = "newid()")
    ModifiedDate: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.now())

    def __repr__(self) -> str:
        text = f"[Id: {self.BusinessEntityID}] [{self.FirstName} {self.LastName}] [guid: {self.rowguid}]"
        return text
