# Games Api - Flask

> It's a Game Api to register Games (Title, Year, Developer) and Developers (Name)

### Requirements
* Docker

### Setup
1. Create and start the container, run in cmd: `docker compose up -d`;

### Tests
* To execute the tests, run in cmd: `docker exec games-api-flask-app-1 pytest`

### Swagger
* To accesse the swagger of the project, enter in: http://localhost:5000/docs

### What is used in this project
* Python:
    * Flask;
    * SQLAlchemy ORM;
    * Pytest;
    * SQLite.
* Swagger (flask_restx);
* Docker;
* Docker compose;
* Postgres.

### Future Improvements
* Improve Swagger;
* Create a Postgres DB tests (it uses SQLite for tests);
* Add some Error Messages like Bad Request.