---
show: step
version: 1.0
enable_checker: true
---

# Jinja2 Template 

## Introduction 

Jinja2 is a Python package implemented with HTML template language. There're basicly two ways to render a page, one is front-end render, the other is back-end render. As for back-end render, it's usually executed by HTML template, which might contains some logics like inheritance other basic template. The inheritance function of these template logic can leave the support from template language, and Jinja2 is just the language needed. With Jinja2, writing HTML template will be an easy thing to do. In this experiment, we will learn all aspects of Jinja2, like template variables, loop function, filter, etc.

#### Knowledge:

- Jinja Syntax
- Jinja filter
- Use Jinja template in Flask 

## Flask and Jinja

Templates are usually used with Web framework together. The default template function of Flask is implemented by Jinja2. So it would be best to learn Jinja by Flask.   

Create Flask app by the command below:  

```sh
$ sudo pip3 install flask
$ cd /home/labex/Code
$ mkdir templates
$ echo "<h1>hello world</h1>" > templates/index.html
$ touch app.py
```

We've created `templates` directory by the commands above. Flask has integrated flask Jinja by default, and would load the corresponding template from `templates` directory automatically. Next, input the code in `app.py`:  

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():

    teacher = {
        'name': 'admin',
        'email': 'admin@labex.io'
    }

    course = {
        'name': 'Python Basic',
        'teacher': teacher,
        'user_count': 5348,
        'price': 199.0,
        'lab': None,
        'is_private': False,
        'is_member_course': True,
        'tags': ['python', 'big data', 'Linux']
    }
    return render_template('index.html', course=course)
```

A Flask application has been created in the code above. Note that we have configured `pp.config['TEMPLATES_AUTO_RELOAD'] = True`, thus making the template automatically re-rendered when the template changes. Then, we have created `index view`, in which we defined `course` dictionary to represent a course. The `view` would render `index.html` template, which is located in `~/Code/templates/index.html`. Next, let's see the result via browser, lauch flask application by the following commands: 

```sh
$ cd ~/Code
$ FLASK_DEBUG=1 FLASK_APP=app.py flask run
* Serving Flask app "app"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

While launching the application, use environment variable `FLASK_DEBUG=1` to configure flask to launch in `debug` mode. You can visit ` http://127.0.0.1:5000/ ` with your browser after launching successfully. Here's the effect: 


![image desc](https://labex.io/upload/H/J/C/XsfBzTgBYW3R.png)

![image desc](https://labex.io/upload/E/L/P/pg0qb1Pk60cu.png)

```checker
- name: Check if app.py is created  
      script: |
        #!/bin/bash
        ls -l /home/labex/Code/app.py
      error: 
        Oops! We found that you haven't created file "app.py" in /home/LabEx/Code/
    - name: Check if function index is created in app.py  
      script: |
        #!/bin/bash
        grep 'index' /home/labex/Code/app.py
      error:
        Oops! Function "index()" is not created in "app.py".
    - name: Check if index.html is created  
      script: |
        #!/bin/bash
        ls -l /home/labex/Code/templates/index.html
      error: Oops, we found that you haven't create file "index.html" in /home/labex/Code/templates/
```

## Basic Jinja2 

In Jinja syntax, we use some special characters to contain the code that needs to be parsed and executed. The other code won't be parsed. The special characters mainly contain(`...` means the code to execute):

- `{% ... %} ` The code is a executable statement, like loop statement or 
  inheritance statement.  
- `{{ ... }}` It contains python object. It parses the value of these objects, often used in printing content. 
- `{# ... #}` Used to add comments, which won't be processed or ouputted to HTML source code.

## Variables

In Jinja2, variables can be displayed in the format of `{{ variable }}`. You can visit its properties by `.`. If the variable passed to the template is a dictionary, then you can use `.` to visit the field of the dictionary. In the `app.py` we created before, we have passed a `course` object to the `index.html` template. Now, change the `index.html` template into the following content. Then you can refresh the browser to check the properties of course:

```html
<p> name: {{ course.name }}</p>
<p> user count: {{ course.user_count }}</p>
<p> teacher: {{course.teacher }} </p>
<p> is_private: {{ course.is_private }} </p>
<p> not exist: {{ course.not_exist }} </p>
```

Effect：


![image desc](https://labex.io/upload/G/N/G/d6WFo1S8fCq6.png)


We can also find out that, if we visit a nonexistent property, it would return `NULL`, without error. This is different from visiting nonexistent property in Python code. 

Jinja2 also supports assigning values. Sometimes, executing method can consume many resources. Then we can assign the executing result to Jinja2 variable by keyword `set`. In the subsequent visitings, we can all visit by this variable:


```html
{% set result = heavy_operation() %}

<p> {{ result }}</p>
```

## Logic Comparison 

The logic comparison in Jinja can be implemented by `if` statement: 

```html
{% if course.is_private %}
    <p> course {{course.name}} is private </p>
{% elif course.is_member_course %}
    <p> course {{course.name}} is member course </p>
{% else %}
    <p> course {{course.name}} is normal course </p>
{% endif %}
```

You can see that the syntax is pretty much similar to the `if` judgement statement, but it needs to be packaged in `{% %}`. Besides, an `endif` statement is needed in the end too. After inputting the code in `index.html`, check the result:  


![image desc](https://labex.io/upload/G/C/I/u6atT45QvEK7.png)


## Loop 

In Jinja, loop is mainly finished with `for` statement. Here's the syntax: 

```html
{% for tag in course.tags %}
    <span> {{ tag }} </span>
{% endfor %}
```

## Macro 

In python, we can define all kinds of functions. Likewise, we can define macro in Jinja2, which is like the function in python. We can write the common used HTML codes in a macro, then the same HTML code will be generated wherever you call the macro. The reusability of code is increased. Macro is defined with macro keywords. For example, you can render the code of a course information into a macro: 

```html
{% macro course_item(course, type="bootstrap") %}
    <div>
        <p> type: {{ type }} </p>
        <p> name: {{ course.name }}</p>
        <p> user count: {{ course.user_count }}</p>
        <p> teacher: {{course.teacher }} </p>
        <p> is_private: {{ course.is_private }} </p>
    </div>
{% endmacro %}

<div> {{ course_item(course) }} </div>
<p>{{ '=' * 20 }}</p>
<div> {{ course_item(course, type="louplus") }} </div>
```

In the code above, we have defined `course_item` macro. This macro has two parameters, the first is course, the second is type(with default value), which is quite like the python function. Next, we called the macro twice with method `{{ course_item(course) }}`. Write the code above in `index.html`, see the effect after refreshing:   


![image desc](https://labex.io/upload/Y/Y/G/vGRwBFTFMDYq.png)


## Module: 

The macro defined before might need to be invoked by other templates. The good thing is, Jinja2 also supports module. First, create `macro.html` under directory `/home/LabEx/Code/templates`. Second, write the code that defined `course_item` macro into the file. Then, we can import the macro by keyword `import` in `index.html`: 

    {% from 'macro.html' import course_item %}
    
    <div> {{ course_item(course) }} </div>

You can find the method to import module similar to python. 

```checker
- name: Check if macro.html is created 
  script: |
    #!/bin/bash
    ls -l /home/labex/Code/templates/macro.html
  error:
    Oops! We found that you haven't created file "macro.html" in /home/labex/Code/templates/
```

## Template Inheritance

Jinja 2 supports the inheritance between modules as well. In pages, many componets are shared. For example, the title and tail of the page, can shard the componets by inheritance easily. The inheritance function is implemented by keywords like `extends` and `block`. First, create `base.html` template under directory `/home/LabEx/Code/templates`, and write the code below:  

```html
<body>
    <div> 
        {% block header %}
            <p> this is header </p>
        {% endblock %}
    </div>
    <div>{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2018 by <a href="https://labex.io/">LabEx</a>.
        {% endblock %}
    </div>
</body>
```

In the code above, we've defined 3 blocks: `header`, `content` and `footer	` by `block`. Other templates can rewrite them. If they haven't been rewritten by other templates, the default content would be displayed. Input the following code in `index.html`: 

```html
{% extends "base.html" %}
{% from 'macro.html' import course_item %}

{% block header %}
    <h1> header </h1>
{% endblock %}

{% block content %}
    {{ course_item(course) }}
{% endblock %}
```

In the code above, first, we told Jinja2 that, the template is inherited from `base.html` by keyword `extends`. Second, we imported the macro from the `macro.html`(defined in the last experiment) by keyword `import`. Next, we used keyword `block` to cover the block `header`and `content` defined in template `base.html`. And as for `content`, it would display the default content. Refresh the browser to see the effect:


![image desc](https://labex.io/upload/A/V/X/c0EpVuY1MYAT.png)


```checker
- name: Check if base.html is created:
  script: |
    #!/bin/bash
    ls -l /home/labex/Code/templates/base.html
  error:
    Oops! We found that you haven't created file "base.html" in /home/labex/Code/templates/
```

## Filter:

Jinja2 also supports filter, which is executed by `|`, like `{{ var | abs }}`, it means computing the absolute value of `var` by filter `abs`. There're many built-in filters in Jinja2:  

- `abs`: Evaluate the absolute value:
- `capitalize`: Capitalize the first character of the string, and change the other characters into lowercase. 
- `first`: Get the first element of the list 
- `int`: Convert into integer 
- `length`: Evaluate the length of the list

Jinja2 also supports defining filters by yourself. It's easy to append filer by flask, just change `app.py` into the code below: 
```python
# -*- coding:utf-8 -*-
    
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
def hidden_email(email):
    parts = email.split('@')
    parts[0] = '*****'
    return '@'.join(parts)
        
app.add_template_filter(hidden_email)
    
@app.route('/')
def index():    
    teacher = {
       'name': 'admin',
        'email': 'admin@labex.io'
    }
    course = {
        'name': 'Python Basic',
        'teacher': teacher,
        'user_count': 5348,
        'price': 199.0,
        'lab': None,
        'is_private': False,
        'is_member_course': True,
        'tags': ['python', 'big data', 'Linux']
    }
    return render_template('index.html', course=course)
```
In the code above, we've registered filter `hidden_email` by method `app.add_template_filter`. The function of this filter is hiddig the prefix of the email. Next, input the code below in `index.html`: 

    {% extends "base.html" %}
    {% from 'macro.html' import course_item %}
    
    {% block content %} 
        <p> teacher email: {{ course.teacher.email | hidden_email }}</p>
        <p> course tag length: {{ course.tags | length }} </p>
    {% endblock %}

Refresh the browser:


![image desc](https://labex.io/upload/U/C/J/c4ovBQDCV2fB.png)

## url_for

Do you remember that we learnt `url_for` to construct URL address in `Flask Rookie Guide`? This method can also be implemented in Jinja in the same way. But you need to add 2 braces in the front and end to parse it into the corrcet URL address in Jinja: 

    {{ url_for('user_index', username='testuser') }}

Besides, there's another common method of `static` directory. While developing  a web application, you need to put some images, js and css files into a unitive `static` directory. Get the address of these files by the code below:  

    {{ url_for('static', filename='css/style.css') }} 

The default `static` directory in Jinja2 is in the same layer with `templates`directory. As long as you put images, js and css files under this directory, you can use this method to get the URL address of the files. 


## Summary  

Most of the knowledge in Jinja2 has been invovled in this experiment, including:

- Variable handling  
- Logic judging 
- Loop   
- Macro defining  
- How to use template and module  
- Template inheritance  
- url_for

In real projects, all the functions above might be used, so try to master the knowledge invovled. The subsequent courses will have many combats of Web development, with many Jinja template code to be written. The good thing is, comparing with CSS/HTML/JS, the syntax of Jinja is much easier. 
