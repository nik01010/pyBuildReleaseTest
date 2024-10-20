from sqlalchemy import Integer, NCHAR, NVARCHAR, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

# TODO: check if Person can inherit directly from DeclarativeBase without defining Base
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
