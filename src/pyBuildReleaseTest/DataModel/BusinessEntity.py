from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

# TODO: check if Person can inherit directly from DeclarativeBase without defining Base
class Base(DeclarativeBase):
    pass

class BusinessEntity(Base):
    __tablename__ = "BusinessEntity"
    __table_args__ = {
        "schema": "Person", 
        # The below is needed because returning a newly inserted Id in a table with triggers can cause errors
        # https://stackoverflow.com/questions/36109206/should-i-always-use-implicit-returningfalse-in-sqlalchemy
        'implicit_returning': False
    }

    BusinessEntityID: Mapped[int] = mapped_column(Integer, primary_key = True, nullable = False)
    rowguid: Mapped[str] = mapped_column(String, nullable = False, server_default = "newid()")
    ModifiedDate: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.now())

    def __repr__(self) -> str:
        text = f"[Id: {self.BusinessEntityID}] [guid: {self.rowguid}]"
        return text
