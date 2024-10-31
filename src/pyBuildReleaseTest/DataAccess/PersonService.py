from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
from pyBuildReleaseTest.DataModel.Person import Person
from sqlalchemy import select, delete, CursorResult, Delete
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

    def check_person_exists(self, id: int) -> None:
        person_count: int = self._context.session.query(Person).where(Person.BusinessEntityID == id).count()
        if person_count == 0:
            raise Exception(f"No records found for Person with BusinessEntityID {id}")

    def get_person(self, id: int) -> Person:        
        query = select(Person).where(Person.BusinessEntityID == id)
        person: Person | None = self._context.session.scalars(query).first()

        if person is None:
            raise Exception(f"No records found for Person with BusinessEntityID {id}")
        
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
        new_business_entity = BusinessEntity()
        self._context.session.add(new_business_entity)
        self._context.session.commit()
        
        new_business_entity_id: int = new_business_entity.BusinessEntityID
        new_person.BusinessEntityID = new_business_entity_id

        self._context.session.add(new_person)
        self._context.session.commit()

        return new_business_entity_id

    def edit_person(self, id: int, edited_person: Person) -> None:
        self.check_person_exists(id = id)

        # TODO: use Mapper for this
        old_person: Person = self.get_person(id = id)
        old_person.Title = edited_person.Title
        old_person.FirstName = edited_person.FirstName
        old_person.MiddleName = edited_person.MiddleName
        old_person.Suffix = edited_person.Suffix
        old_person.ModifiedDate = edited_person.ModifiedDate

        self._context.session.commit()

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
