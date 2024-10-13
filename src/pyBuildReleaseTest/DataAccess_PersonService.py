from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataModel_Person import Person
from sqlalchemy import select
from pandas import DataFrame, read_sql_query

class PersonService:
    # TODO: add logging
    # TODO: add schema validator
    def __init__(self, database_context: ApplicationDbContext) -> None:
        self._context: ApplicationDbContext = database_context

    def get_people(self) -> DataFrame:
        people: DataFrame = read_sql_query(sql = select(Person), con = self._context.database_connection)
        return people
