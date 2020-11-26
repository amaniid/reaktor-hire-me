# reaktor-hire-me
Assignment done for Spring 2021 junior dev position in Reaktor. Flask App, that shows installed packages on your server/computer.

This assignment was originally for the Autumn 2020 position. I wasn't then ready to apply, but I did most of the task. And I can't find the assignment itself anymore, but I suppose this has most features in place.

## Setting up
### Clone repository (Linux)
Open terminal and navigate to directory of your choice. 

```
$ git clone https://github.com/amaniid/reaktor-hire-me.git
```

### Run app
Go to the project directory:

```
$ cd reaktor-hire-me
```

Set the `main.py` as the starting point:
```
$ export FLASK_APP=app/main.py
```

 Run:
 ```
$ python3 -m run flask
```
 (Your Python might be under different alias.)
 
 `Pipfile`, `Procfile`, `wsgi.py` and `runtime.txt` are there for Heroku deployment, meaning they are not needed for local running of app.
