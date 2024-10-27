from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
from pyBuildReleaseTest.DataModel.Person import Person
from sqlalchemy import select, update, delete, CursorResult, Delete
from pandas import DataFrame, read_sql_query
from typing import Optional, Any

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

    def person_exists(self, id: int) -> bool:
        person_count: int = self._context.session.query(Person).where(Person.BusinessEntityID == id).count()

        # TODO: add unit test for multiple records scenario
        if person_count > 1:
            raise Exception(f"Expected single record for BusinessEntityID {id} but found {person_count}")
        elif person_count == 1:
            return True
        else:
            return False

    def check_person_exists(self, id: int) -> None:
        person_exists: bool = self.person_exists(id = id)
        if not person_exists:
            raise Exception(f"No records found for Person with BusinessEntityID {id}")

    def get_person_by_id(self, id: int) -> DataFrame:
        self.check_person_exists(id = id)
        
        query = select(Person).where(Person.BusinessEntityID == id)
        person: DataFrame = read_sql_query(sql = query, con = self._context.database_connection)
        return person
    
    def get_people_by_name(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> DataFrame:
        no_names_provided: bool = ((first_name is None) & (last_name is None))
        if no_names_provided:
            raise Exception("Either first_name or last_name must be provided")
        
        if last_name is None:
            query = select(Person).where(Person.FirstName == first_name)
        elif first_name is None:
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
        
        new_business_entity_id: int = new_business_entity.BusinessEntityID
        new_person.BusinessEntityID = new_business_entity_id

        self._context.session.add(new_person)
        self._context.session.commit()

        return new_business_entity_id

    # def edit_person(self, id: int, new_person: Person) -> int:
    #     # TODO: add logging
    #     # TODO: add validation using SchemaValidator
    #     self.check_person_exists(id = id)

        # query = update(Person).where(Person.BusinessEntityID == id).values(new_person)

    def delete_person(self, id: int) -> int:
        self.check_person_exists(id = id)

        query_delete_person: Delete = delete(Person).where(Person.BusinessEntityID == id)
        delete_person_result: CursorResult[Any] = self._context.session.execute(query_delete_person)
        
        query_delete_business_entity: Delete = delete(BusinessEntity).where(BusinessEntity.BusinessEntityID == id)
        delete_business_entity_result: CursorResult[Any] = self._context.session.execute(query_delete_business_entity)

        people_deleted: int = delete_person_result.rowcount
        business_entities_deleted: int = delete_business_entity_result.rowcount

        self._context.session.commit()

        rows_affected: int = max(people_deleted, business_entities_deleted)

        return rows_affected
