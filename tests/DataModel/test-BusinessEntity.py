import unittest
from pyBuildReleaseTest.DataModel.BusinessEntity import BusinessEntity
from datetime import datetime

class TestBusinessEntity(unittest.TestCase):
    def test_create_new_business_entity_should_return_correct_class(self):
        # Arrange / Act
        expected_id: int = 123
        expected_modified_date: datetime = datetime.now()
        test_person: BusinessEntity = BusinessEntity(
            BusinessEntityID = expected_id,
            rowguid = "abc",
            ModifiedDate = expected_modified_date
        )

        # Assert
        self.assertIsInstance(test_person, BusinessEntity)
        self.assertEqual(expected_id, test_person.BusinessEntityID)
        self.assertEqual(expected_modified_date, test_person.ModifiedDate)

if __name__ == '__main__':
    unittest.main()
