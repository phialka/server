# Database architecture
This tables contains description for each table in server database. 
Some fields in tables contain links for more information.

### users
| column name | description | type |
|:------------|:------------|:-----|
| id |  |  |
| username | user's login | string |
| userpass | user's password | string |

### user_info
| column name | description | type |
|:------------|:------------|:-----|
| id |  |  |
| user_id |  | foreign key |
| info | an object with [user information][uinfo] | json |

### user_settings
| column name | description | type |
|:------------|:------------|:-----|
| id |  |  |
| user_id |  | foreign key |
| info | an object with [user settings][usettings] | json |

[uinfo]: coming_soon
[usettings]: coing_soon