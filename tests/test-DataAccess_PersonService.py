import unittest
from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataAccess_PersonService import PersonService
from pyBuildReleaseTest.DataModel_Person import Person
from sqlalchemy import text, TextClause
from typing import List
from datetime import datetime
from pandas import DataFrame, Series

class TestDataAccessPersonService(unittest.TestCase):
    in_memory_database_connection_string: str = "sqlite+pysqlite:///:memory:"

    def setUp(self):
        self.test_connection_string: str = self.in_memory_database_connection_string
        self.test_database_context: ApplicationDbContext = ApplicationDbContext(connection_string = self.in_memory_database_connection_string)

        # Create Person database
        create_person_database_statement: TextClause = text("ATTACH DATABASE \':memory:\' AS Person;")
        delete_person_table_statement: TextClause = text("DROP TABLE IF EXISTS Person")
        with self.test_database_context.connection_engine.connect() as connection:
            connection.execute(create_person_database_statement)
            connection.execute(delete_person_table_statement)

        # Create Person table
        Person.metadata.create_all(self.test_database_context.connection_engine)

    def tearDown(self):
        self.test_database_context.disconnect()

    def test_create_new_person_service_should_return_correct_class(self):
        # Arrange / Act
        test_person_service: PersonService = PersonService(database_context = self.test_database_context)

        # Assert
        self.assertIsInstance(test_person_service, PersonService)

    def test_get_people_count_should_return_correct_count(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self.test_database_context)
        test_people: List[Person] = [
            Person(
                BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
                EmailPromotion = 1, rowguid = "abc", ModifiedDate = datetime.now()
            ),
            Person(
                BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, rowguid = "bcd", ModifiedDate = datetime.now()
            ),
            Person(
                BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry",
                EmailPromotion = 1, rowguid = "bcd", ModifiedDate = datetime.now()
            )
        ]
        self.test_database_context.session.bulk_save_objects(test_people)
        expected_count: int = len(test_people)

        # Act
        result: int = test_person_service.get_people_count()

        # Assert
        self.assertEqual(expected_count, result)

    def test_get_people_should_return_correct_records(self):
                # Arrange
        test_person_service: PersonService = PersonService(database_context = self.test_database_context)
        test_person_bob: Person = Person(
            BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, rowguid = "abc", ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, rowguid = "bcd", ModifiedDate = datetime.now()
        )
        test_people: List[Person] = [test_person_bob, test_person_alice]
        
        self.test_database_context.session.bulk_save_objects(test_people)
        expected_count: int = len(test_people)

        # Act
        result: DataFrame = test_person_service.get_people()

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        actual_person_bob: Series = result[result["BusinessEntityID"] == 1].squeeze()
        self.assertEqual(expected_count, actual_count)
        self.assertEqual(test_person_bob.FirstName, actual_person_bob["FirstName"])
        self.assertEqual(test_person_bob.ModifiedDate, actual_person_bob["ModifiedDate"])

if __name__ == '__main__':
    unittest.main()
