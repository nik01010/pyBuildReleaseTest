import unittest
from pyBuildReleaseTest.DataModel_Person import Person
from datetime import datetime

class TestDataModelPerson(unittest.TestCase):
    def test_create_new_person_should_return_correct_class(self):
        # Arrange / Act
        expected_id = 123
        test_person: Person = Person(
            BusinessEntityID = expected_id,
            PersonType = "AB",
            NameStyle = 0,
            Title = "Mr",
            FirstName = "John",
            MiddleName = None,
            LastName = "Doe",
            Suffix = None,
            EmailPromotion = 1,
            AdditionalContactInfo = None,
            Demographics = None,
            rowguid = "abc",
            ModifiedDate = datetime.now()
        )

        # Assert
        self.assertIsInstance(test_person, Person)
        self.assertEqual(test_person.BusinessEntityID, expected_id)

if __name__ == '__main__':
    unittest.main()
