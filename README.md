# pyBuildReleaseTest

Python port of [rBuildReleaseTest](https://github.com/nik01010/rBuildReleaseTest)

## Installation
### Local Build
- pip install -q build
- python -m build

### Local Install
- pip install .\dist\pybuildreleasetest-0.1.0.tar.gz

## Usage
```python
from pyBuildReleaseTest.Helpers.Logger import initialise_logger
from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext, ConnectionDetails
from pyBuildReleaseTest.DataAccess.PersonService import PersonService
from pyBuildReleaseTest.DataModel.Person import Person
from configparser import ConfigParser
from logging import Logger
from pandas import DataFrame


def main():
    logger: Logger = initialise_logger()
    logger.info("Starting ETL Process")

    # Connect ---------------------------------------------------------------------
    logger.info("Connecting to Database")
    connection_details: ConnectionDetails = ConnectionDetails(
        server = "localhost",
        database = "AdventureWorks2022",
        driver = "ODBC+Driver+17+for+SQL+Server"
    )
    connection_string: str = connection_details.get_connection_string()

    database_context: ApplicationDbContext = ApplicationDbContext(connection_string = connection_string)

    person_service: PersonService = PersonService(database_context = database_context)


    # Read ------------------------------------------------------------------------
    logger.info("Extracting Data")
    people_count: int = person_service.get_people_count()

    people: DataFrame = person_service.get_people()

    person_by_id: Person = person_service.get_person(id = 16003)

    people_bob: DataFrame = person_service.get_people_by_name(first_name = "Bob")
    people_chapman: DataFrame = person_service.get_people_by_name(last_name = "Chapman")
    people_bob_chapman: DataFrame = person_service.get_people_by_name(first_name = "Bob", last_name = "Chapman")


    # Create ----------------------------------------------------------------------
    logger.info("Creating Data")
    new_person: Person = Person(
        PersonType = "EM", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry", EmailPromotion = 1
    )
    new_person_id: int = person_service.create_person(new_person = new_person)


    # Edit ------------------------------------------------------------------------
    logger.info("Editing Data")
    edited_person: Person = new_person
    edited_person.MiddleName = "Anderson"
    person_service.edit_person(id = new_person_id, edited_person = edited_person)
    

    # Delete ----------------------------------------------------------------------
    logger.info("Deleting Data")
    deleted_records: int = person_service.delete_person(id = new_person_id)


    # Disconnect ------------------------------------------------------------------
    database_context.disconnect()

    logger.info("ETL Process completed")

if __name__ == '__main__':
    main()
```

## Sample Data
- This project uses the [AdventureWorks2022.bak](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#download-backup-files) sample dataset from Microsoft
- Use [these instructions](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#restore-to-sql-server) to load the sample dataset into SQL Server Management Studio (SSMS)
