from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
from pyBuildReleaseTest.DataModel.Person import Person
from sqlalchemy import select
from pandas import DataFrame, read_sql_query
from typing import Optional

class PersonService:
    # TODO: add logging
    # TODO: add schema validator
    def __init__(self, database_context: ApplicationDbContext) -> None:
        self._context: ApplicationDbContext = database_context

    def get_people_count(self) -> int:
        people_count: int = self._context.session.query(Person).count()
        return people_count
    
    def get_people(self) -> DataFrame:
        query = select(Person)
        people: DataFrame = read_sql_query(sql = query, con = self._context.database_connection)
        return people

    def get_person_by_id(self, id: int) -> DataFrame:
        query = select(Person).where(Person.BusinessEntityID == id)
        person: DataFrame = read_sql_query(sql = query, con = self._context.database_connection)

        # TODO: add unit tests for these two branches
        # TODO: is there a more specific Exception to use here
        number_of_records = len(person)
        if (number_of_records == 0):
            raise Exception(f"No records found for BusinessEntityID {id}")
        if (number_of_records > 1):
            raise Exception(f"Expected single record for BusinessEntityID {id} but found {number_of_records}")

        return person
    
    def get_people_by_name(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> DataFrame:
        no_names_provided: bool = ((first_name is None) & (last_name is None))
        if no_names_provided:
            raise Exception("Either first_name or last_name must be provided")
        
        if (last_name is None):
            query = select(Person).where(Person.FirstName == first_name)
        elif (first_name is None):
            query = select(Person).where(Person.LastName == last_name)
        else:
            query = select(Person).where((Person.FirstName == first_name) & (Person.LastName == last_name))

        people: DataFrame = read_sql_query(sql = query, con = self._context.database_connection)
        return people

    def create_person(self, new_person: Person) -> int:
        # TODO: add validation using SchemaValidator
        new_business_entity = BusinessEntity()
        self._context.session.add(new_business_entity)
        self._context.session.commit()
        
        new_business_entity_id = new_business_entity.BusinessEntityID
        new_person.BusinessEntityID = new_business_entity_id

        self._context.session.add(new_person)
        self._context.session.commit()

        return new_business_entity_id
