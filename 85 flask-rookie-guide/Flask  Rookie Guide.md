---
show: step
version: 1.0
enable_checker: true
---
#Flask  Rookie Guide

##1. Introduction

Flask is a famous microframework in Python, extensible for plugins. Besides, it only maintains one core. Comparing with Django, Django is more like a overall computer of a big brand, leaving you nothing to be worried about and offering you whatever you need. And for Flask, it's more like an assemble computer, or a well designed CPU, more precisely. So it's quite flexible for you to choose the fittings(plugins) you need.

####1.1 Knowledge

- Introduction of Flask 
- Configuration 
- Register route
- Rendering Templates 
- request object
- session
- cookies
- Error handling
- Plugins 

####1.2 A Simple Example

Here's a simple example, let's create /home/labex/app.py，and write：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

Flask offers a command line tool to manage the Flask application. First, configure the environment variable of the application: 

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=1
```

The environment variable FLASK_APP is used to point at the path of the Flask application's code, which is executed by flask run. The path is named app.py here. FLASK_DEBUG=1 means the opened DEBUG information, it can output the visiting and bug information, helping us to solve the problems occurred in the code. I suggest that you should always open FLASK_DEBUG while executing flask run.

Then, we can execute the Flask application this way:

```sh
flask run
```

By default, the application is executed in localhost:5000. Open the browser, visit this address, and you will see the Hello World! returned.

```checker
- name: Check if app.py is created
  script: |
    #!/bin/bash
    ls /home/labex/app.py
  error: Oops! We found that you didn't create file "app.py" in "/home/labex".
  timeout: 3
- name: Check if function index is created in app.py  
  script: |
    #!/bin/bash
    grep -i 'index' /home/labex/app.py
  error: Oops! We find that you didn't define "index()" method in "app.py".
  timeout: 3
```


####1.3 Flask shell

Besides flask run，here's a frequently used command: flask shell. These commands can load the code module assigned in the FLASK_APP environment variable. The difference is, flask run would enter the status of executing the app directly, whereas flask shell only loads and enters a Shell terminal. In this terminal, we can execute some codes, like the initializing database we'll mention later, and inserting some data into the database, etc.

```sh
$ flask shell
> 
```

####1.4 Configuration

After initializing a Flask app, we can manage the configure by app.config. The configuration information saved in app.config, in essence, is a dictionary. So, you can use the dictionary method to append or update the configuration. For example, after initializing the app, configure a secret key:

```python
app = Flask(__name__)
app.config.update({
	  'SECRET_KEY': 'a random string' 
})
```

All the configuration options should be capitalized. And multiple words should be connected with "_". In big projects, the configuration is usually written in a single config.py file. Then you can use the special method offered by app.config to update the config, and the argument is the path of config.py:

```python
app.config.from_pyfile('path/to/config.py')
```

Some other similar methods: 

- from_envvar(variable_name)： Use a configuration file assigned by the environment variable to update the configuration. 
- from_object(obj)： Use an object to update the configuration file. Dict is invalid. 
- from_json(filename)： Use JSON file to update configuration.
- from_mapping(*mapping, **kwargs)： Similar to the update before. The difference is, you don't have to capitalize the words in this method.

The way to get the configuration information, is to use the format of dictionary app.config['SECRET_KEY'] Then we can get the configuration value of SECRET_KEY

##2. Register Route

Flask uses decorator @app.route to register the route and its process function. In the example above, just use the homepage / to register a route. index function will process how to visit the homepage. 

You can pass variables in the route, in the format of <variable_name>. For example, the homepage of every user needs different routes, so we can use the username as the variable of the route:

```python
@app.route('/user/<username>')
def user_index(username):
    # Set the variable name in the function, so that we can get the variable value passed from the route. 
    return 'Hello {}'.format(username)
```

We can also assign the type of the route variable. For example, in a blog application, every blog article page can use the ID of this article as the route variable. Besides, the ID should be a value of int type: 

```python
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {}'.format(post_id)
```

The content of the registered route return will be contained in the HTTP response, which will be returned to users. As these two examples will all return strings, when users use browser to visit these two links, they will see two strings displayed in the browser page. 

```checker
- name: Check if function user_index is created in app.py  
  script: |
    #!/bin/bash
    grep -i 'def' /home/labex/app.py | grep -i 'user_index'
  error: Oops, we find that you didn't define "user_index()" method in "app.py".
  timeout: 3
- name: Check if show_post is created in app.py  
  script: |
    #!/bin/bash
    grep -i 'def' /home/labex/app.py | grep -i 'show_post'
  error: Oops, we find that you didn't define "show_post()" method in "app.py".
  timeout: 3
```

##3. Rendering Templates

In the example above, what the process function returns are all strings. However, in real projects, we need to use HTML to write pages, making it unlikely to write all the contents into the strings. The function of template engine is writing HTML page by the syntax of the template engine, assigning templates in process function, as well as passing the corresponding template variables. In this way, Flask can invoke the template engine to automatically render a complete HTML page.

By default, the template engine of Flask is jinja2. Theoretically, you can use other template engines instead, but jinja2 is useful enough. 

Flask uses function render_template to render templates. After assigning a template name, Flask will find the template under directory templates. Next, it will use the variables passed in to render the template.

If we use template to rewrite the example of the user's homepage, then the process function can be put like this: 

```python
from flask import render_template

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
```

Next, create directory templates. The directory structure will be like this: 

    /flask-test-app
        app.py
        /templates
            user_index.html

In user_index.html:

```html
<h1>Hello, {{ username }}!</h1>
```

In jinja2, {{ }} is used to render a string variable. The username here is the keyword argument username passed in render_template. Now, visit a user's homepage, for example: 

    localhost:5000/user/labex

You can see shiyanlou! packaged with h1 label.

Additionally, flask also offers url_for to create URL address by the function name of the route, as well as redirect jump to other routes. Check out the example below: 

```python
from flask import render_template, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('user_index', username='default'))

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
```

In this example, while visiting / index page, it would automatically jump to /user/default page. The URL address of the target page to jump to, is generated by url_for. Meanwhile, the jumping process is done by function redirect. 

##4. Request Object

Flask requests for corresponding data through request object. Import from flask to use it: 

```python
from flask import request
```

Get the requested header data from request.headers. It can be used as a dictionary, for example, while getting the user-agent of users: 

```python
request.headers.get('User-Agent')
```

Get the requested arguments from request.args. Suppose the application as a blog application, with paging function. Use this URL to visit the homepage: 

    localhost:5000?page=2&per_page=10

Get the argument agter：

```python
page = request.args.get('page')
per_page = request.args.get('per_page')
```

Besides, you can get the list data from request.form, and get the current requested method(GET or POST) by request.method  

##5. Session

HTTP is a stateless protocol. Every request is mutually independent. However, in actual applications, we have many data for the server to remember indeed, but meanwhile, not suitable for saving in a database. 

For example, in a login page, after typing the password wrong for 3 times, the user will be requested to input verification code. That means the server needs a counter to record the times of the wrong input. However, saving it in the database is not proper. session is just a place for each user to save some data individually, and  the data saved in session can be shared between multiple requests of a certain user. 

##6. Cookies

It's similar to session, only that cookie is the classified inform saved in the client-side. In flask, cookie uses the configured SECRET_KEY as the signature to classify. 

For example, in the route of the visiting user's homepage, set the username as a cookies, then we will find out who the user is when he/she visits here:

```python
from flask import make_response

@app.route('/user/<username>')
def user_index(username):
    resp = make_response(render_template('user_index.html', username=username))
	resp.set_cookie('username', username)
    return resp
```

After configuring the cookies，users can get the username we configured while visiting other pages:

```python
from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
	return 'Hello {}'.format(username)
```

##7. Error Handling

Register error handlers by decorating a function with errorhandler(). Take the 404 error for example, we'd return a certain 404.html page. 

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
```

The example also shows a tip on how to use render_template, that is, you can set the status code returned this time behind it.

In flask, there's a method named abort() to handle errors frequently. You can use abort(404) to directly enter the handling logic that the page can't be found(status code:404). Here's an example: 

```python
from flask import render_template, abort

@app.route('/user/<username>')
def user_index(username):
    if username == 'invalid':
        abort(404)
    return render_template('user_index.html', username=username)
```

When the username is an invalid string, or, in other words, visiting the address /user/invalid, it will directly return that the page can not be found.  

```checker
- name: Check whether func not_found is created in app.py  
  script: |
    #!/bin/bash
    grep -i 'def' /home/labex/app.py | grep -i 'not_found'
  error: Oops, we find that you didn't define "not_found()" method in "app.py".
  timeout: 3
```

##8. Plugins

We've listed some of the frequently used plugins in Flask development, most of them will be used in the projects later on. Every plugin can be explored in Github, you can get to know them first.

- flask-sqlalchemy：ORM，packaged with sqlalchemy，easier to use 
- flask-login：Manage the session of users，like login, logout, and expiration session management.
- flask-migrate：Database version management 
- flask-wtf：Packaged with wtforms form generation and validation tools, offering  CSRF support.
- flask-session：In flask, session is based on cookie by default. This plugin makes it easier to do session in the server-side.

##9. Summary

In this experiment, we have learnt the basics of developing Flask Web applications by some simple developing examples. The content of this course contains the following knowledges: 

1. Introduction of Flask 
2. Configuration 
3. Register route
4. Rendering Templates 
5. request object
6. session
7. cookies
8. Error handling
9. Plugins 

In the development of actual projects, many plugins will be used in flask, like using flask_sqlalchemy to connect to the database, using flask-login to manage login and logout. Our efficiency in developing web applications can be extremely improved by using these plugins. So, when you have any requirement in the development, search whether there's already a module for us to use first. If there is, then you can directly use it by referring to the readme.


