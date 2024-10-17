import unittest
from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext, ConnectionDetails
from sqlalchemy import Engine, Connection

class TestDataAccessApplicationDbContext(unittest.TestCase):
    in_memory_database_connection_string: str = "sqlite+pysqlite:///:memory:"

    def test_connection_details_should_construct_correct_connection_string(self):
        # Arrange
        test_server: str = "test_server"
        test_database: str  = "DatabaseName"
        test_driver: str  = "Driver Name 123"
        expected_connection_string: str = f"mssql+pyodbc://{test_server}/{test_database}?trusted_connection=yes&driver={test_driver}"

        # Act
        test_connection_details: ConnectionDetails = ConnectionDetails(
            server = test_server,
            database = test_database,
            driver = test_driver
        )

        # Assert
        actual_connection_string: str = test_connection_details.get_connection_string()
        self.assertEqual(expected_connection_string, actual_connection_string)

    def test_create_new_context_should_return_correct_class(self):
        # Arrange
        test_connection_string: str = self.in_memory_database_connection_string
        
        # Act
        test_database_context: ApplicationDbContext = ApplicationDbContext(connection_string = test_connection_string)

        # Assert
        self.assertIsInstance(test_database_context, ApplicationDbContext)
        test_database_context.disconnect()

    def test_create_new_context_should_create_engine_and_connection(self):
                # Arrange
        test_connection_string: str = self.in_memory_database_connection_string
        
        # Act
        test_database_context: ApplicationDbContext = ApplicationDbContext(connection_string = test_connection_string)

        # Assert
        actual_connection_engine: Engine = test_database_context.connection_engine
        actual_database_connection: Connection = test_database_context.database_connection
        self.assertIsInstance(actual_connection_engine, Engine)
        self.assertIsInstance(actual_database_connection, Connection)
        test_database_context.disconnect()

if __name__ == '__main__':
    unittest.main()
