## Project structure

At this stage in the project, there are three key places where the layers of our application are stored:

1. routers - the directory stores files in which request handler functions are declared
2. schemas - the directory stores schemas for validating the data that the server accepts in the request body.
3. db_models - the file stores classes that are mapping tables from the database to nursery classes.

In addition, there is:
- controllers directory - it should store functions that take query data and, in accordance with them, take/insert the necessary data from tables.
- main.py - puts everything together. to start the server, you need to run this file.
