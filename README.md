# Phialka backend

## Project structure

- entities: Domain entities data models
- use_cases: Use cases and abstract classes which it use
- adapters: Realization of the use cases abstract classes
- rest_api: Api routers (now we using FasAPI)
- database: Database models 
- utils: Other utils which may come in handy


## Application launch

Using docker compose (you must be in project root directory)
```
docker compose up
```

Without docker compose

```bash
pip install -r requirements.txt
```
```bash
python app/main.py
```

> *You must have postgresql server running in your pc\
> Specify it in the .env file
> ```
> DATABASE_URL=postgresql://you_user:you_password@database:5432/test_db
> ```

