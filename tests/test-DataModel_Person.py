import unittest
from pyBuildReleaseTest.DataModel_Person import Person
from datetime import datetime

class TestDataModelPerson(unittest.TestCase):
    def test_create_new_person_should_return_correct_class(self):
        # Arrange / Act
        expected_id: int = 123
        expected_last_name: str = "Doe"
        expected_modified_date: datetime = datetime.now()
        test_person: Person = Person(
            BusinessEntityID = expected_id,
            PersonType = "AB",
            NameStyle = 0,
            Title = "Mr",
            FirstName = "John",
            MiddleName = None,
            LastName = expected_last_name,
            Suffix = None,
            EmailPromotion = 1,
            AdditionalContactInfo = None,
            Demographics = None,
            rowguid = "abc",
            ModifiedDate = expected_modified_date
        )

        # Assert
        self.assertIsInstance(test_person, Person)
        self.assertEqual(expected_id, test_person.BusinessEntityID)
        self.assertEqual(expected_last_name, test_person.LastName)
        self.assertEqual(expected_modified_date, test_person.ModifiedDate)

if __name__ == '__main__':
    unittest.main()
