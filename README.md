# HW Riskyfiy

<p>
    this project base on open source project that i build for [fun](https://github.com/Sivanwol/demo-ecom-server)
    this fully working project that allow to connect to many types of db's.
</p>
<p>
    The project been tested on unit test this required to add FLASK_ENV=testing
    as well copy .env.template into .env.testing (the system will load based the FLASK_ENV value means abc env then .env.abc is required)
</p>


### Virtual environments

```angular2html
$ sudo apt-get install python-virtualenv
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install Flask

Install all project dependencies using:

```
When need install the deps of the system
```angular2html
$ pip install -r requirements.txt
```

if ever need add a dep to the project please do as follow
```angular2html
$ pip install packagename
$ pip freeze > requirements.txt # this will regenerate the requirements.txt
```

### Testing
see: [here](https://docs.python.org/3/library/unittest.htm)
<p>
for run use this command:
</p>

```angular2html
$ python -m unittest
```
### Running
 
```angular2html
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ python -m flask run
```

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production.

If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

```angular2html
$ flask run --host=0.0.0.0
```

##### Command Lines

###### getting list of route on the system
```angular2html
$ python manage.py list_routes
```


### Running using Manager

This app can be started using Flask Manager. It provides some useful commands and configurations, also, it can be customized with more functionalities.

```angular2html
$ python manage.py runserver
```

### Alembic Migrations

Use the following commands to create a new migration file and update the database with the last migrations version:

```angular2html
$ flask db revision --autogenerate -m "description here"
$ flask db upgrade head
```

This project also uses the customized manager command to perform migrations.
```angular2html
$ python manage.py db revision --autogenerate -m "description here"
$ python manage.py db upgrade head
```

To upgrade the database with the newest migrations version, use:

```angular2html
$ python manage.py db upgrade head
```
