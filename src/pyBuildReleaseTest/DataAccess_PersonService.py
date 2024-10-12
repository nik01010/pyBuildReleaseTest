from pyBuildReleaseTest.DataAccess_ApplicationDbContext import ApplicationDbContext

class PersonService:
    # TODO: add logging
    # TODO: add schema validator
    def __init__(self, database_context: ApplicationDbContext) -> None:
        self._context: ApplicationDbContext = database_context

    def get_people_count(self) -> int:
        # TODO: add implementation
        people_count = 1
        return people_count
    