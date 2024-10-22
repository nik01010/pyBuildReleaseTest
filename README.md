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
from pyBuildReleaseTest.DataAccess.ApplicationDbContext import ApplicationDbContext, ConnectionDetails
from pyBuildReleaseTest.Helpers.Logger import initialise_logger
from pyBuildReleaseTest.DataAccess.PersonService import PersonService
from pyBuildReleaseTest.DataModel.Person import Person
from logging import Logger
from pandas import DataFrame

logger: Logger = initialise_logger()

# TODO: pass connection parameters from config (DEV/UAT/PROD)
connection_details: ConnectionDetails = ConnectionDetails(
    server = "localhost",
    database = "AdventureWorks2022",
    driver = "ODBC+Driver+17+for+SQL+Server"
)
connection_string: str = connection_details.get_connection_string()

def main():
    logger.info("Starting ETL Process")

    logger.info("Connecting to Database")
    database_context: ApplicationDbContext = ApplicationDbContext(connection_string = connection_string)

    logger.debug("Setting up Data Services")
    person_service: PersonService = PersonService(database_context = database_context)

    logger.info("Extracting Data")

    people_count: int = person_service.get_people_count()

    people: DataFrame = person_service.get_people()

    person_by_id: DataFrame = person_service.get_person_by_id(id = 16003)

    person_bob: DataFrame = person_service.get_people_by_name(first_name = "Bob")
    person_chapman: DataFrame = person_service.get_people_by_name(last_name = "Chapman")
    person_bob_chapman: DataFrame = person_service.get_people_by_name(first_name = "Bob", last_name = "Chapman")

    new_person: Person = Person(
        PersonType = "EM", NameStyle = 0, Title = "Mr", FirstName = "Tom", LastName = "Jerry", EmailPromotion = 1
    )
    new_person_id: int = person_service.create_person(new_person = new_person)
    logger.debug(f"Created new Person with BusinessEntityID: {new_person_id}")

    database_context.disconnect()

    logger.info("ETL Process completed")

if __name__ == '__main__':
    main()
```

## Sample Data
- This project uses the [AdventureWorks2022.bak](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#download-backup-files) sample dataset from Microsoft
- Use [these instructions](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#restore-to-sql-server) to load the sample dataset into SQL Server Management Studio (SSMS)
