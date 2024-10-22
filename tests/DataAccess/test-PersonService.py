import unittest
from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataAccess.PersonService import PersonService
from pyBuildReleaseTest.DataModel.Person import Person
from sqlalchemy import text, TextClause
from typing import List
from datetime import datetime
from pandas import DataFrame, Series

class TestPersonService(unittest.TestCase):
    in_memory_database_connection_string: str = "sqlite+pysqlite:///:memory:"

    def setUp(self):
        self._context: ApplicationDbContext = ApplicationDbContext(connection_string = self.in_memory_database_connection_string)

        # Create Person database
        create_person_database_statement: TextClause = text("ATTACH DATABASE \':memory:\' AS Person;")
        delete_person_table_statement: TextClause = text("DROP TABLE IF EXISTS Person")
        with self._context.connection_engine.connect() as connection:
            connection.execute(create_person_database_statement)
            connection.execute(delete_person_table_statement)

        # Create Person table
        Person.metadata.create_all(self._context.connection_engine)

    def tearDown(self):
        self._context.disconnect()

    def test_create_new_person_service_should_return_correct_class(self):
        # Arrange / Act
        test_person_service: PersonService = PersonService(database_context = self._context)

        # Assert
        self.assertIsInstance(test_person_service, PersonService)

    def test_get_people_count_should_return_correct_count(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        test_people: List[Person] = [
            Person(
                PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = len(test_people)

        # Act
        result: int = test_person_service.get_people_count()

        # Assert
        self.assertEqual(expected_count, result)

    def test_get_people_should_return_correct_records(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 1
        another_id: int = 2
        test_person_bob: Person = Person(
            BusinessEntityID = expected_id, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = another_id, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_people: List[Person] = [test_person_bob, test_person_alice]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = len(test_people)

        # Act
        result: DataFrame = test_person_service.get_people()

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        self.assertIn(expected_id, result["BusinessEntityID"].values)
        actual_person_bob: Series = result[result["BusinessEntityID"] == expected_id].squeeze()
        self.assertEqual(expected_count, actual_count)
        self.assertEqual(test_person_bob.FirstName, actual_person_bob["FirstName"])
        self.assertEqual(test_person_bob.ModifiedDate, actual_person_bob["ModifiedDate"])

    def test_get_person_by_id_should_return_correct_person(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 1
        another_id: int = 2
        test_person_bob: Person = Person(
            BusinessEntityID = another_id, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = expected_id, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_people: List[Person] = [test_person_bob, test_person_alice]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = sum(person.BusinessEntityID == expected_id for person in test_people)

        # Act
        result: DataFrame = test_person_service.get_person_by_id(id = expected_id)

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        self.assertEqual(expected_count, actual_count)
        self.assertIn(expected_id, result["BusinessEntityID"].values)
        actual_person_alice: Series = result[result["BusinessEntityID"] == expected_id].squeeze()
        self.assertEqual(test_person_alice.BusinessEntityID, actual_person_alice["BusinessEntityID"])
        self.assertEqual(test_person_alice.FirstName, actual_person_alice["FirstName"])

    def test_get_people_by_name_should_return_correct_people_using_first_name(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_first_name: str = "Bob"
        test_people: List[Person] = [
            Person(
                PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = expected_first_name, LastName = "Chapman",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "CD", NameStyle = 0, Title = "Mr", FirstName = expected_first_name, LastName = "Carson",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = sum(person.FirstName == expected_first_name for person in test_people)

        # Act
        result: DataFrame = test_person_service.get_people_by_name(first_name = expected_first_name)

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        self.assertEqual(expected_count, actual_count)
        self.assertIn(expected_first_name, result["FirstName"].values)
        actual_unique_first_names: List[str] = result["FirstName"].unique()
        self.assertEqual(expected_first_name, actual_unique_first_names)

    def test_get_people_by_name_should_return_correct_people_using_last_name(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_last_name: str = "Chapman"
        test_people: List[Person] = [
            Person(
                PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = expected_last_name,
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "CD", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = sum(person.LastName == expected_last_name for person in test_people)

        # Act
        result: DataFrame = test_person_service.get_people_by_name(last_name = expected_last_name)

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        self.assertEqual(expected_count, actual_count)
        self.assertIn(expected_last_name, result["LastName"].values)
        actual_unique_last_names: List[str] = result["LastName"].unique()
        self.assertEqual(expected_last_name, actual_unique_last_names)

    def test_get_people_by_name_should_return_correct_people_using_both_names(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_first_name: str = "Bob"
        expected_last_name: str = "Carson"
        test_people: List[Person] = [
            Person(
                PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = expected_first_name, LastName = "Chapman",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "CD", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                PersonType = "DE", NameStyle = 0, Title = "Mr", FirstName = expected_first_name, LastName = expected_last_name,
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        self._context.session.bulk_save_objects(test_people)
        expected_count: int = sum(
            ((person.FirstName == expected_first_name) & (person.LastName == expected_last_name)) for person in test_people
        )

        # Act
        result: DataFrame = test_person_service.get_people_by_name(first_name = expected_first_name, last_name = expected_last_name)

        # Assert
        self.assertIsInstance(result, DataFrame)
        actual_count: int = len(result)
        self.assertEqual(expected_count, actual_count)
        self.assertIn(expected_first_name, result["FirstName"].values)
        self.assertIn(expected_last_name, result["LastName"].values)
        actual_unique_first_names: List[str] = result["FirstName"].unique()
        self.assertEqual(expected_first_name, actual_unique_first_names)
        actual_unique_last_names: List[str] = result["LastName"].unique()
        self.assertEqual(expected_last_name, actual_unique_last_names)

if __name__ == '__main__':
    unittest.main()
