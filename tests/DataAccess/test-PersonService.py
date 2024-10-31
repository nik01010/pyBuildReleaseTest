import unittest
from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataAccess.PersonService import PersonService
from pyBuildReleaseTest.DataModel.Person import Person
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
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

        # Delete BusinessEntity and Person tables
        delete_person_table_statement: TextClause = text("DROP TABLE IF EXISTS Person")
        delete_business_entity_table_statement: TextClause = text("DROP TABLE IF EXISTS BusinessEntity")
        with self._context.connection_engine.connect() as connection:
            connection.execute(create_person_database_statement)
            connection.execute(delete_person_table_statement)
            connection.execute(delete_business_entity_table_statement)

        # Re-create BusinessEntity and Person tables
        BusinessEntity.metadata.create_all(self._context.connection_engine)
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
        test_person_bob: Person = Person(
            BusinessEntityID = expected_id, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
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

    def test_check_person_exists_should_throw_error_if_record_does_not_exist(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 3
        test_people: List[Person] = [
            Person(
                BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        expected_error_message: str = f"No records found for Person with BusinessEntityID {expected_id}"
        self._context.session.bulk_save_objects(test_people)
        
        # Act
        with self.assertRaises(Exception) as result:
            test_person_service.check_person_exists(id = expected_id)

        # Assert
        actual_error_message: str = str(result.exception)
        self.assertEqual(expected_error_message, actual_error_message)

    def test_get_person_should_return_correct_person(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 2
        test_person_bob: Person = Person(
            BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = expected_id, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_people: List[Person] = [test_person_bob, test_person_alice]
        self._context.session.bulk_save_objects(test_people)

        # Act
        result: Person = test_person_service.get_person(id = expected_id)

        # Assert
        self.assertIsInstance(result, Person)
        self.assertEqual(test_person_alice.BusinessEntityID, result.BusinessEntityID)
        self.assertEqual(test_person_alice.FirstName, result.FirstName)
        self.assertEqual(test_person_alice.LastName, result.LastName)
        self.assertEqual(test_person_alice.ModifiedDate, result.ModifiedDate)

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

    def test_create_person_should_create_record(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        test_existing_business_entities: List[BusinessEntity] = [
            BusinessEntity(BusinessEntityID = 1, ModifiedDate = datetime.now()),
            BusinessEntity(BusinessEntityID = 2, ModifiedDate = datetime.now())
        ]
        test_existing_people: List[Person] = [
            Person(
                BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            ),
            Person(
                BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
                EmailPromotion = 1, ModifiedDate = datetime.now()
            )
        ]
        test_new_person: Person = Person(
            PersonType = "CD", NameStyle = 0, Title = "Mr", FirstName = "Tom", 
            LastName = "Jerry", EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        self._context.session.bulk_save_objects(test_existing_business_entities)
        self._context.session.bulk_save_objects(test_existing_people)
        expected_count: int = (len(test_existing_people) + 1)
        expected_new_id: int = (len(test_existing_people) + 1)

        # Act
        result: int = test_person_service.create_person(new_person = test_new_person)
        
        # Assert
        self.assertIsInstance(result, int)
        self.assertEqual(expected_new_id, result)
        actual_new_person: Person = test_person_service.get_person(id = result)
        self.assertEqual(test_new_person.BusinessEntityID, actual_new_person.BusinessEntityID)
        self.assertEqual(test_new_person.FirstName, actual_new_person.FirstName)
        self.assertEqual(test_new_person.LastName, actual_new_person.LastName)
        self.assertEqual(test_new_person.ModifiedDate, actual_new_person.ModifiedDate)
        actual_people: DataFrame = test_person_service.get_people()
        actual_count: int = len(actual_people)
        self.assertEqual(expected_count, actual_count)

    def test_edit_person_should_edit_record(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 1
        test_person_bob: Person = Person(
            BusinessEntityID = expected_id, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime(2024, 10, 1, 9, 0)
        )
        test_person_alice: Person = Person(
            BusinessEntityID = 2, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, ModifiedDate = datetime(2024, 10, 1, 9, 0)
        )
        test_existing_people: List[Person] = [test_person_bob, test_person_alice]
        self._context.session.bulk_save_objects(test_existing_people)
        test_edited_person_bob: Person = Person(
            BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Robert", 
            MiddleName = "Anderson", LastName = "Chapman", EmailPromotion = 1, ModifiedDate = datetime(2024, 12, 1, 12, 0)
        )

        # Act
        result: None = test_person_service.edit_person(id = expected_id, edited_person = test_edited_person_bob)

        # Assert
        self.assertIsNone(result)
        actual_new_person = test_person_service.get_person(id = expected_id)
        self.assertEqual(test_edited_person_bob.BusinessEntityID, actual_new_person.BusinessEntityID)
        self.assertEqual(test_edited_person_bob.FirstName, actual_new_person.FirstName)
        self.assertEqual(test_edited_person_bob.MiddleName, actual_new_person.MiddleName)
        self.assertEqual(test_edited_person_bob.LastName, actual_new_person.LastName)
        self.assertEqual(test_edited_person_bob.ModifiedDate, actual_new_person.ModifiedDate)

    def test_delete_person_should_delete_record(self):
        # Arrange
        test_person_service: PersonService = PersonService(database_context = self._context)
        expected_id: int = 2
        test_person_bob: Person = Person(
            BusinessEntityID = 1, PersonType = "AB", NameStyle = 0, Title = "Mr", FirstName = "Bob", LastName = "Chapman",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_person_alice: Person = Person(
            BusinessEntityID = expected_id, PersonType = "BC", NameStyle = 0, Title = "Ms", FirstName = "Alice", LastName = "Cooper",
            EmailPromotion = 1, ModifiedDate = datetime.now()
        )
        test_existing_people: List[Person] = [test_person_bob, test_person_alice]
        self._context.session.bulk_save_objects(test_existing_people)
        expected_rows_to_delete: int = 1
        expected_count: int = (len(test_existing_people) - expected_rows_to_delete)

        # Act
        result: int = test_person_service.delete_person(id = expected_id)

        # Assert
        self.assertEqual(expected_rows_to_delete, result)
        actual_new_people: DataFrame = test_person_service.get_people()
        actual_count: int = len(actual_new_people)
        self.assertEqual(expected_count, actual_count)
        expected_id_exists: bool = (expected_id in actual_new_people["BusinessEntityID"].values)
        self.assertFalse(expected_id_exists)

if __name__ == '__main__':
    unittest.main()
