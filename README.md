# Json_to_db_parser

This app pulls data from a json file and extracts interfaces configurations to insert into a postgres database.

### Prerequisites
- [python3](https://www.python.org/)
- [postgres](https://www.postgresql.org/)
- [psycopg2](https://pypi.org/project/psycopg2/)
- [sqlalchemy](https://www.sqlalchemy.org/)

### Usage
Firstly need to change database configuration in .env file to connect to your specific postgres server
Then run the next command.
```
python app.py
```