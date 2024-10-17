import unittest
from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext
from pyBuildReleaseTest.DataAccess_PersonService import PersonService
from pyBuildReleaseTest.DataModel_Person import Person

class TestDataAccessPersonService(unittest.TestCase):
    in_memory_database_connection_string: str = "sqlite+pysqlite:///:memory:/"


    def setUp(self):
        self.test_connection_string: str = self.in_memory_database_connection_string
        self.test_database_context: ApplicationDbContext = ApplicationDbContext(connection_string = self.in_memory_database_connection_string)
        # Person.metadata.create_all(self.test_database_context.connection_engine)

    def tearDown(self):
        self.test_database_context.disconnect()

    def test_create_new_person_service_should_return_correct_class(self):
        # Arrange / Act
        test_person_service: PersonService = PersonService(database_context = self.test_database_context)

        # Assert
        self.assertIsInstance(test_person_service, PersonService)

    def test_get_people_count_should_return_correct_count(self):
         pass
        # Arrange
        # Act
        # Assert
    