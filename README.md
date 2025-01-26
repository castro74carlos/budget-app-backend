# budget-app-backend

## Set Up Steps:
1. Install venv for python
2. activate venv `source ./venv/bin/activate`
3. Create a superuser by running the following command: 
    ```
    cd backend
    python manage.py createsuperuser
    ```
4. Follow the prompts on screen


## Running Application:

### From CLI:
Run the following command to run any migrations and start up
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### From PyCharm: 
Run the `Migrate and Run` configuration


## Running Tests:

### Pytest:
From the root of project in Python Virtual Environment (Recommended),
run the following:

```
    cd backend
    pip install pytest-django
    pytest --ds=backend.settings
```

### In PyCharm:
Right click on [`tests.py`](./backend/accounts/tests.py) file name,
select the option to `Run Python tests in tests.py`


### Using Django cli
From the root of project in Python Virtual Environment (Recommended),
run the following:

```
    cd backend
    python manage.py test
```
or Run `Run Tests` configuration