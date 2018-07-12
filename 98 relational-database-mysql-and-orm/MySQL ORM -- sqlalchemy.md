---
show: step
version: 1.0
enable_checker: false
---

# MySQL ORM -- SQLAlchemy

## 1. Introduction

Web development can't leave the support from database. In this experiment, we will learn relational database MySQL and ORM SQLAlchemy. [MySQL](https://www.mysql.com/) is the most widely used database, and [SQLAlchemy](https://www.sqlalchemy.org/) is the most popular ORM in Python.

#### Knowledge

- Basic knowledge of MySQL  
- Basic knowledge of relational database 
- Basic knowledge of SQLAlchemy  

## 2. SQLAlchemy

In real projects, we don't visit database by writing SQL statement directly, instead, we use ORM tool. The fullname of ORM is Object  Relational Mapping. With ORM, we can map the python object into database, so we won't need to write any SQL statements anymore. And in python, SQLAlchemy is a powerfull ORM package, which is worth learning. Meanwhile, SQLAlchemy supports multiple relational data, if the project needs to conver to database of other types in the later period, it will be easier to use `SQLAlchemy`.

### 2.1 Environment Preparations 

The experiment environment is mainly built based on `virtualenv`. Being of great importance, `virtualenv` can be understood as a seprated virtual environment. The packages installed under virtualenv won't effect the packages of the whole system, which can avoid the influence between packages of different versions. Besides, all you need about virtualenv is knowing how to create, activate and deactivate.

While using virtualenv, note that after you installed a package, you need to use `deactivate` command to exit virtualenv and re-activate virtualenv to use this package. 

After opening the terminal in the desktop, input the following commands by order to build the environment(`$` is the prompt of `shell`, the content after it is the command you need to input):
```
$ cd ~/Code
$ sudo pip install virtualenv
$ virtualenv -p /usr/bin/python3.5 env
$ source env/bin/activate
$ pip3 install sqlalchemy lPython mysqlclient
$ deactivate
```
The commands above have created a `virtualenv` environment in `Code` environment, next, installed the software packages needed in this experiment, like `sqlalchemy` and `lPython`. Next, it used `deactivate` to exit `env`. The subsequent interactive commands are all inputted by `lPython` terminal. Launch `lPython` terminal by the following commands: 
```
$ source env/bin/activate
$ lPython
```
Similar to the Python3 interactive environment we used before, lPython is an interactive computing system. But it's an interactive "Python shell" with more convenient functions. The main advantages of it are: 

1. Get many types of information of the objects in the code easily 
2. Use "!" to call Linux commands directly 
3. Support code auto-completion by TAB
4. Save all the inputted code into history record database 

So, if you are familiar with `lPython`, you would give up the previous `Python Shell` gradually.

In the subsequent codes, characters like `In [1]` are the prompt of lPython, you don't need to input these. 

The subsequent basic oprerations of SQLAlchemy are offered with detailed codes and expectant results, without involved with hard oprerations. In the operating process, understand the function of every module and function in SQLAlchemy carefully. 

Note: In lPython, pressing "enter" for two continuous times will lead to a new input. So if you haven't finished writing your class, do not press "enter" for two continuous times. 

### 2.2 Connect to Database  

Using SQLAlchemy to connect to database is mainly executed by `Engine` object.
Input the following code in lPython terminal: 

```python
In [1]: from sqlalchemy import create_engine

In [2]: engine = create_engine('mysql://root:@localhost/labex')

In [3]: engine.execute('select * from user').fetchall()python
Out[3]: [(1, 'admin', 'admin@labex.io'), (2, 'user1', 'user1@gmail.com')]
```

First, we've imported `create_engine`. This method is used to create `Engine` example. The parameters passed to `create_engine` defined the visiting address of MySQL server, with the format of `mysql://<user>:<password>@<host>/<db_name>`. What we visit in the example is just the `labex` database created before.


![image desc](https://labex.io/upload/U/U/I/pM6yhw6n34eE.png)


Next, we've executed a SQL statement by `engine.execute` method, queryed all the users in user table. Quite easy. 

### 2.3 Object-relational Mapping

If you want to map Python class into database table, you will need `declarative base class` based on `SQLAlchemy`, which is, declaring base class to create class. When you create Python class based on the base class, it would automatically map to the corresponding database table. You can use `declarative_base` method to create declarative base class:

```python
In [5]: from sqlalchemy.ext.declarative import declarative_base

In [6]: Base = declarative_base()
```

After creating base class, input the following code in lPython terminal to create `User` class. This class will map to the `user` table created before:

```python
In [10]: from sqlalchemy import Column, Integer, String

In [11]: class User(Base):
    ...:     __tablename__ = 'user'
    ...:     id = Column(Integer, primary_key=True)
    ...:     name = Column(String)
    ...:     email = Column(String)
    ...:     def __repr__(self):
    ...:         return "<User(name=%s)>" % self.name
    ...: 
    
In [12]:
```

When the code above executes, class `User` will be successfully defined. Note that `__repr__` has two underlines both in the front and end. The function with two underlines in the front and end represents a special function, named the magic method of python class. `__init__` is also a magic method. `__repr__` method would be called when directly calling objects in examples. `__tablename__` means the table name.

User has a `__table__` property to record the table information of the defined table. The property is shown below: 

```python
In [27]: User.__table__
Out[27]: Table('user', MetaData(bind=None), Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(), table=<user>), Column('email', String(), table=<user>), schema=None)
```


![image desc](https://labex.io/upload/L/U/N/sYyp7a2ps2Aj.png)


What if you want to query the database by `User` ? Import `Session` first. `Seesion` is the bridge between map class and database, containing the function of transaction management. Create `Session` by the following code: 

```python
In [13]: from sqlalchemy.orm import sessionmaker

In [14]: Session = sessionmaker(bind=engine)

In [15]: session = Session()
```

This code imports `sessionmaker` from `sqlalchemy.orm`, and creates a `sessionmaker` object `Session`. The `Session` object has a magic method (call), enabling the `Session` object to be called like a function, making it possible for ` Session()` to get a `session` object. 

When `Session` is successfully created, you can query the users now, mainly by `session.query` method: 

```python
In [16]: session.query(User).all()
Out[16]: [<User(name=admin)>, <User(name=lxttx)>]

In [17]: session.query(User).filter(User.name=='admin').first()
Out[17]: <User(name=admin)>
```

Queried successfully. And you can directly  use field of `User` class to filter query. 


![image desc](https://labex.io/upload/V/O/U/fTRlnFjgDtYi.png)


If you chose to show SQL statement by `echo` parameter while creating Engine before(`engine = create_engine('mysql://root:@localhost/labex', echo=True)`), then you will see the corresponding SQL output when you use session to query. 
```python
In [20]: session.query(User).filter(User.name=='admin').first()
2017-08-30 18:02:37,878 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
2017-08-30 18:02:37,878 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,883 INFO sqlalchemy.engine.base.Engine SELECT DATABASE()
2017-08-30 18:02:37,883 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,885 INFO sqlalchemy.engine.base.Engine show collation where `Charset` = 'utf8' and `Collation` = 'utf8_bin'
2017-08-30 18:02:37,885 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,889 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS CHAR(60)) AS anon_1
2017-08-30 18:02:37,889 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,893 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS CHAR(60)) AS anon_1
2017-08-30 18:02:37,893 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,895 INFO sqlalchemy.engine.base.Engine SELECT CAST('test collated returns' AS CHAR CHARACTER SET utf8) COLLATE utf8_bin AS anon_1
2017-08-30 18:02:37,895 INFO sqlalchemy.engine.base.Engine ()
2017-08-30 18:02:37,897 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2017-08-30 18:02:37,898 INFO sqlalchemy.engine.base.Engine SELECT user.id AS user_id, user.name AS user_name, user.email AS user_email
FROM user
WHERE user.name = %s
  LIMIT %s
2017-08-30 18:02:37,899 INFO sqlalchemy.engine.base.Engine ('admin', 1)
Out[69]: <User(name=admin)>
```
In the query above, we used `filter` to filter the data. The operator in filter can be the operators in WHERE clause of SQL(like ==, !=, <, >, etc), or operators like AND, OR. Besides, the filter here can be changed to `filter_by` function. The latter is not flexible as the former, se we recommend `filter`. 

### 2.4 Creating database table 

You can create database table based on the class defined by `SQLAlchemy`. Next, try to create a new experiment table `lab`, a course will be related to multiple experiments. So the relationship between `course` and `lab` is 1:M. Before defineing `Lab` class, you need to create `Course` class, to make it map to the `courese` table you defined before:

```python
In [18]: from sqlalchemy.orm import relationship

In [19]: from sqlalchemy import ForeignKey

In [20]: class Course(Base):
    ...:     __tablename__ = 'course'
    ...:     id = Column(Integer, primary_key=True)
    ...:     name = Column(String)
    ...:     teacher_id = Column(Integer, ForeignKey('user.id'))
    ...:     teacher = relationship('User')
    ...:     def __repr__(self):
    ...:         return '<Course(name=%s)>' % self.name
    ...:
```

We've imported something new in the code above. Thw `course` table created above has foreign key `teacher_id`, we can use `ForeignKey` to configure foreign key in SQLAlchemy. After configuring foreign key, it would be quite convenient to visit the corresponding records in `user` table from the example in `Course` directly. We can implement it by `relationship`. The code above defined `teaher` property by `relationship`, thus enabling you to get the corresponding user record by `course.teacher` directly. After finishing defineing `Course` class, let's define `Lab` class next: 

```python
In [21]: class Lab(Base):
    ...:    __tablename__ = 'lab'
    ...:    id = Column(Integer, primary_key=True)
    ...:    name = Column(String(64))
    ...:    course_id = Column(Integer, ForeignKey('course.id'))
    ...:    course = relationship('Course', backref='labs')
    ...:    def __repr__(self):
    ...:         return '<Lab(name=%s)>' % self.name
    ...:
```


The code above defined class `Lab`. Note when we are defineng the property of `course`, we used the parameter `backref` of `relationship`. With this parameter, we can visit the all the corresponding experiment record by `course.labs` in `Courese` example.  

Next, let's create the corresponding `lab` table in MySQL by the following commands. 

```python
In [22]: Base.metadata.create_all(engine)
```


Then we can see the table has been successfully created in the MySQL server:

```sql
mysql> show tables;
+---------------------+
| Tables_in_labex     |
+---------------------+
| course              |
| lab                 |
| user                |
+---------------------+
3 rows in set (0.00 sec)

mysql> describe lab;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| id        | int(11)     | NO   | PRI | NULL    | auto_increment |
| name      | varchar(64) | YES  |     | NULL    |                |
| course_id | int(11)     | YES  | MUL | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```


![image desc](https://labex.io/upload/F/R/C/Y6zSTJtI48et.png)


### 2.5 Simple Oprerations of CRUD 

Based on the class `User`, `Course` and `Lab`, we will learn further about creating, querying, updating and deleting. With ORM mapping, creating database records becomes easier. For example, if you want to create an experiment, relate it to the course, and then just create an example of `Lab`: 
```python
In [37]: course = session.query(Course).first()
    
In [38]: lab1 = Lab(name='ORM basics', course_id=course.id)
   
In [39]: lab2 = Lab(name='relational database', course=course)
    
In [41]: session.add(lab1)
    
In [42]: session.add(lab2)
    
In [43]: session.commit()
  
In [44]: course.labs
Out[44]: [<Lab(name=relational database)>, <Lab(name=ORM basics)>]
```

In the code above, we queried the course objects to manage, created 2 experiments, and submit them to the database by `session.commit（）`. Before submitting the data changes into the database, we need to add the data to `session` by `session.add` method. Besides, we can see that, while creating experiments, there're two ways to relate them to the courses: 1. Assign the value to `course_id` directly. 2.Assign value to the relationship property `course`. When the data is successfully inserted into the database, we can get them by `course.labs`. 

We can query that 2 data has been inserted into `lab` table in MySQL server.

```sql
mysql> select * from lab;
+----+--------------------+-----------+
| id | name               | course_id |
+----+--------------------+-----------+
|  2 | relational databas |    2      |
|  3 | ORM basics         |    2      |
+----+--------------------+-----------+
2 rows in set (0.00 sec)
```


![image desc](https://labex.io/upload/Y/R/U/y1ryKKhWyAl6.png)


It's easy to update. All you need is updating the property of the objectm, and then submit it to the database by `session.commit（）`. The code below shows how to update the course name: 

```python
In [58]: course.name
Out[58]: 'Python basics'

In [59]: lab1.course
Out[59]: <Course(name=Python basics)>

In [60]: course.name = 'Python data analysis'

In [61]: session.add(course)

In [62]: session.commit()

In [63]: lab1.course
Out[63]: <Course(name=Python data analysis)>

In [64]: session.query(Course).all()
Out[64]: [<Course(name=Python data analysis)>]
```


While deleting data, just delete the objects by `session.delete`:
```python
In [65]: session.delete(lab1)
    
In [66]: session.commit()
    
In [67]: course.labs
Out[67]: [<Lab(name=relationship database)>]
```
After deleting, the number of experiments got from the course example also decreases. 


![image desc](https://labex.io/upload/U/F/S/AnOoa0UVXkhL.png)


We can see that, with SQLAlchemy, the CRUD oprerations of database all become the corresponding Python object oprerations, which is very convenient and easy.

### 2.6 Building the Relationship of 1:1 and M:M 

In relational database, there're 3 types of relationships: 

- 1:1，the data in two tables are in a 1:1 relationship. Suppose the user has only one attached information, then the user table and attached information table are in a 1:1 relationship.
- 1:M，like the relationship between course and experiment, a course is corresponding to multiple experiments. 
- M:M，many to many. Like the course and table, a course has many tables, and a table is corresponding to many courses.  

We've leant about the method to create the 1:M relationship, mainly done with foreign key. Actually, the 1:1 relationship can also be created by foreign key. Use the code below to create the attached information table of users `UserInfo`:

```python
In [86]: class UserInfo(Base):
    ...:     __tablename__ = 'userinfo'
    ...:     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    ...:     addr = Column(String(512))
    ...:
    
In [87]: Base.metadata.create_all(engine)
```


In the code above, we've successfully created `UserInfo` table, whose relationship between `User` table is 1:1, as its main key and foreign key are all `user_id` and relied on the main key of `User` table.

As for the M:M relationship, it can be created by two 1:M relationships. If two tables are in a relationship of 1:M with the same table(suppose its name is T), then we can use T as the intermediary table, to create the M:M relationshi+p of two tables. Take the relationship between course table and tag table for example, we can create it with the code below: 

```python
In [90]: from sqlalchemy import Table, Text

In [91]: course_tag = Table('course_tag', Base.metadata,
    ...:     Column('course_id', ForeignKey('course.id'), primary_key=True),
    ...:     Column('tag_id', ForeignKey('tag.id'), primary_key=True)
    ...: )
    
In [92]: class Tag(Base):
     ...:     __tablename__ = 'tag'
     ...:     id = Column(Integer, primary_key=True)
     ...:     name = Column(String(64))
     ...:     courses = relationship('Course',
     ...:                            secondary=course_tag,
     ...:                            backref='tags')
     ...:     def __repr__(self):
     ...:         return '<Tag(name=%s)>' % self.name
    
In [93]: Base.metadata.create_all(engine)  
```


1. `Base.metadata` is a `sqlalchemy.schema.MetaData` object, representing the 
  set of all Table objects. `create_all()` will strike all the tables created by statement `CREATE TABLE`. 
2. `course_tag` is a double main key. The purpose of using double key is to avoid the existence of two repeated main key records. It's mostly used in the M:M intermediary table.
3. `secondary` means the intermediary table.`backref` is the table pointing at itself. 
4. The internal implementation of `session` is calling the ports of `engine`, so `session` is like a package of `engine`. For example, `session.commit` would invole `engine.connect()` first to connect to database, and then call the port related to executing sql.


![image desc](https://labex.io/upload/S/A/Q/HBGtaV02VAaw.png)


In the code above, we've created a intermediary table `course_tag` with class `Table`. As this table doesn't need to map to any python object, we directly created the table. We can see `Course`, `Tag` table and `course_tag` table are all in 1:M relationship. And we've created M:M relationship with intermediary table `course_tag`. What's more, property `courses` is defined in `Tag` table. By the parameter `secondary` of function `relationship`, this property tells SQLAlchemy that, it should relate to the object of `Course` table by table `course_tag`. We will show you how to make CRUD opreration of M:M relationship below: 

```python
In [126]: session.close()
In [130]: course = session.query(Course).first()

In [131]: course.tags
Out[131]: []

In [132]: tag1 = Tag(name='tag_1')

In [133]: tag2 = Tag(name='tag_2')

In [136]: course.tags.append(tag1)

In [137]: course.tags.append(tag2)

In [138]: session.add(course)

In [139]: session.commit()

In [140]: course.tags
Out[140]: [<Tag(name=tag_1)>, <Tag(name=tag_2)>]

In [141]: engine.execute('select * from tag').fetchall()
Out[141]: [(1, 'tag_1'), (2, 'tag_2')]

In [142]: engine.execute('select * from course_tag').fetchall()
Out[142]: [(2, 1), (2, 2)]
```


![image desc](https://labex.io/upload/E/E/D/9v986UqpnuMX.png)


In the code above, we've added tags into courses by `course.tags.append(tag1)`. It's easy as operating python list. In the end, by `engine.execute`, we executed SQL query to verify that the tags are inserted into the database indeed, and the corresponding relationship record is also generated in table `course_tag`. Now, let's try to add course in object `Tag`:


```python
In [153]: teacher = session.query(User).filter(User.name=='admin').first()

In [154]: course1 = Course(name='Linux basics', teacher=teacher)

In [155]: session.add(course1)

In [156]: session.commit()

In [157]: tag1.courses
Out[157]: [<Course(name=Python data analysis)>]

In [159]: tag1.courses.append(course1)

In [160]: session.add(tag1)

In [161]: session.commit()

In [163]: tag1.courses
Out[163]: [<Course(name=Python data analysis)>, <Course(name=Linux basics)>]

In [164]: engine.execute('select * from course_tag').fetchall()
Out[164]: [(2, 1), (3, 1), (2, 2)]
```


First, created another course `course1`, and then added `course1` to tag `tag1` successfully.  


![image desc](https://labex.io/upload/K/P/Y/92plrZ2ZtbOA.png)


I believe that after the examples above, you have basicly mastered the method to created all kinds of relationships in SQLAlchemy. 

## 3. Summary:

This experiment mainly talked about the basic knowledge of `MySQL` and `SQLAlchemy`. `MySQL` mainly contains the knowledge below: 

- How to create database and table  
- Basic CRUD operations 
- How to create basic constraints 

SQLAlchemy mainly contains the following knowledge: 

- How to connect to database  
- How to define mapping class(table) 
- How to make CRUD operations by python objects  
- How to define common relationships  

Loads of code are involved in this course, but you need to write all of it to truly master the content of the course. 
