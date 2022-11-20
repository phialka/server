# Content
- Environment requirements
- Project file structure
- Application layers
    - Database layer
    - ...
    - API layer

# Environment requirements
Information about used libraries and develop environment settings.

# Project file structure
At this stage in the project, there are three key places where the layers of our application are stored:

1. routers - the directory stores files in which request handler functions are declared. 
2. schemas - the directory stores schemas for validating the data that the server accepts in the request body.
3. dbmodels - the file stores classes that are mapping tables from the database to nursery classes.

In addition, there is:
- controllers directory - it should store functions that take query data and, in accordance with them, take/insert the necessary data from tables.
- main - puts everything together. to start the server, you need to run this file.

# Application layers

### Database layer
The database layer is described in the application using data models - classes, in this case, describing those tables that should exist in the database, and the relationships between them. The data models in the project are described in the file dbmodels.py using pydantic and ormar.

For example, let's try to add two related tables to the project - users and user_settings. Let 's say they will have the following structure:

***users***
| column name | description | type |
|:------------|:------------|:-----|
| id |  |  |
| username | user's login | string |
| userpass | user's password | string |

***user_settings***
| column name | description | type |
|:------------|:------------|:-----|
| id |  |  |
| user_id |  | foreign key |
| info | an object with user settings | json |

These tables will correspond to the following data models that we will add to the project:

```python
database = databases.Database(config.DATABASE_URL)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100)
    userpass: str = ormar.String(max_length=100)


class UserSettings(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_settings"
    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    settings: pydantic.Json = ormar.JSON()
```
You can read more about the description of data models in ormar in the [official documentation](https://collerek.github.io/ormar/models/).

Also, you can find more detailed information about the database architecture of the original project in the corresponding section: [database architecture](database_architecture.md)

### API layer
coming soon