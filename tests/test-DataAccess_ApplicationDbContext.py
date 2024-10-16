import unittest
import sqlite3
from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext, ConnectionDetails

class TestDataModelPerson(unittest.TestCase):
    def setUp(self):
        self.test_sql_database: sqlite3.Connection = sqlite3.connect(":memory:")
        # cursor = self.test_sql_database.cursor()

    def tearDown(self):
        self.test_sql_database.close()

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

if __name__ == '__main__':
    unittest.main()
