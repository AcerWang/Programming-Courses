---
show: step
version: 1.0
enable_checker: false
---

# MySQL Basic

## 1. Introduction

Web development can't leave the support from database. In this experiment, we will learn relational database MySQL and ORM SQLAlchemy. [MySQL](https://www.mysql.com/) is the most widely used database, and [SQLAlchemy](https://www.sqlalchemy.org/) is the most popular ORM in Python.

#### Knowledge 

- Basic knowledge of MySQL  
- Basic knowledge of relational database 
- Basic knowledge of SQLAlchemy  

## 2. MySQL

MySQL is the most widely used database. Relational database use relational model as the metod to save data organizations, it can be divided in structure of 4 layers:


- Database, an application is corresponding to a database 
- Table, a database contains multiple tables
- Records, a table is consisted of multiple records 
- Field，a recode is made of multiple fields 

You can imagine the table structure as an Excel table, which is consisted of multiple fields, with each field being able to save data of certain types like strings and numbers. The types can be assigned while creaing tables. The tables arr connected by relationship(logic relationship), enabling you to query between multiple tables by the relationship while querying data.


The most important feature of relational database is ACID:

- A means atomicity 
- C means consistency
- I means isolation 
- D means durability 

ACID can ensure reliability. It means, it can make sure that a seriess of database operations can consist a complete logic process. The process would only be all executed or not executed at all. It wouldn't be half processed. Take transfering money in bank for example: Deducting money from the original client, and adding money to the target client. The summation of these two operations consist a complete and inseparable logic process.

To implement the ACID feature, MySQL supports multiple constraints. For example, while inserting a data, we need  to check if the foreign key exists. Though these operations can ensure the consistency of data, the they would, most of the time, lower the abiliy of concurrent operations. So, in the websites nowadays, if there's any needs of concurrent operations, ACID won't be used. Some would even use NoSQL. 

Besides, we need to supplement some basic knowledge of the keys in relational database, to helo you understand the content below. 

- Primary key: A combination of data columns or properties, give the saved data objects unique and complete marks. A data column can only have one primary key, and its value can't be null. 
- Foreign key: Actually in database, every data table is connected with relationship. The primary key of parent entity will be put in another data table, as a property to create the mutual relationship. This property is foreign key.  

For instance, the relationship between student and teacher is teaching relationship. In student data table, there's a property named tacher(foreign key), and this value is corresponding to the teahcer number(primary key) in the teacher data table. 

In the following content, we will be learning basic operations of MySQL. 

### 2.1 Environment Preparation

We've installed MySQL in labex environment. You need to manually launch the MySQL service by the following commands: 

    $ sudo service mysql start

One more package to install 

    $ sudo pip3 install mysqlclient

The function of this package is to enable Python to connect to MySQL database. The following errors will happen if you don't install and use Python and SQLAlchemy to connect to MySQL database: 

    $ python3
    >>> import MySQLdb

`ImportError: No module named MySQLdb` or `Module MySQLdb not found`.

The reason why these error occurs is that `mysqlclient` hasn't been installed in the environment, or you haven't installed this package in the virtual environment while using virtualenv(we will learn it in the part of using python to connect to database). In addtion, if you didn't reactivate virtualenv environment, you may have this error even when you've install 

If this error occurs in the virtual environment created by virtualenv, then we need to execute `pip3 install mysqlclient` in virtualenv, execute `deactivate` to exit the virtualenv environment and enter virtualenv.

If you didn't create virtual environment by virtualenv, then just execute `sudo pip3 install mysqlclient`.

The function of virtualenv is avoiding the use conflict between python verson and package version. For example, if the system is only installed with python3.5, but a program has to execute on python2.7, virtualenv can deal with it. The python package installed in virtualenv will only be available when you enter virtualenv again. 

After successfully lauching the database, connect to the database by the following orders: 

    $ mysql -u root

MySQL database is consisted of client-side and server-side, the latter can be connected by former. In the command above, you can use `root` client to login the server. `Root`client is the supreme adminster account, not assigned with password information. That is because we didn't set the password of the `root` account in labex environment.
After login succeeds:


![image desc](https://labex.io/upload/N/F/T/6uI4wz0VCHUm.png)


All the MySQL Commands(beginning with mysql>) will be inputted from MySQL client-side. 

### 2.2 Basic Operations:

It's quite easy to create database, just input `create database <db_name>;`. `<db_name>` means the database name, and you can see all the databases by command `show databases;`(note that a `"s"` is added here), delete a database by `drop database <db_name>`, the example below shows the creating and deleting process of database:
```sql
mysql> create database labex;
    Query OK, 1 row affected (0.00 sec)
    
    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | labex              |
    | sys                |
    +--------------------+
    5 rows in set (0.00 sec)
    
    mysql> drop database labex;
    Query OK, 0 rows affected (0.00 sec)
    
    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | sys                |
    +--------------------+
    4 rows in set (0.00 sec)
```
Note thae the output of `show databases;` shows multiple databases. That is because MySQL server has some default databases, the result might varys in different MySQL versions.


![image desc](https://labex.io/upload/H/E/K/UjawNBtLB66q.png)

After successfully created database, creating tables will be the next. Before that, you need connect to `labex` database by `use labex;` command.


The basic commands to create table is: 

```sql
CREATE TABLE TABLE NAME 
(
Column name a data type(data length) 
Column name b data type(data length)
Column name c data type(data length)
);
```

Next, try to create a table named `user`, with 3 fields: 

- id, an integer, use `int`  
- name, a string, use `varchar`
- email, a string, use `varchar`

Input the following commands in MySQL client-side: 

```sql
mysql> create database labex;
mysql> use labex;
Database changed
mysql> create table user
    -> (
    -> id int(10),
    -> name varchar(20),
    -> email varchar(64)
    -> );
Query OK, 0 rows affected (0.03 sec)
mysql> show tables;
+---------------------+
| Tables_in_labex     |
+---------------------+
| user                |
+---------------------+
1 row in set (0.00 sec)
```

You can create `user` table by the commands above. Note that after inputting `create table user` and press `enter`, the client side will automatically recognize that it's an unfinished command, so the prompt `->` would appear. After successfully creating the table, you can see all the tables by `show tables;`, delete tables by `drop table <table_name>;`.


![image desc](https://labex.io/upload/W/B/D/m1jk0I6Z8sQ0.png)


If you want to see the field information of a table, use `show create table <table_name>;` or `describe <table_name>；` command, as follows: 

```sql
mysql> show create table user;

| user  | CREATE TABLE `user` (
  `id` int(10) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
1 row in set (0.00 sec)

mysql> describe user;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(10)     | YES  |     | NULL    |       |
| name  | varchar(20) | YES  |     | NULL    |       |
| email | varchar(64) | YES  |     | NULL    |       |
+-------+-------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```

Fileds in MySQL table support multiple types, like integer, float, string, timestamp and so on. The lack of space forbids further introducion of these.


![image desc](https://labex.io/upload/A/H/I/mSkI49Y3Xrch.png)


After successfully creating the sheet, you can inser data with `inser` command. The complete command fomat is: 

```sql
INSERT INTO TABLE NAME(Column name a,column name b,column name c) VALUES(value 1,value 2,value 3);
```

When the inserted value and the field number defined by table are the same and in the same order, you can insert data into `user` table by the following order while ignoring the column name information:

```sql
mysql> insert into user(id, name, email) values(1, 'admin', 'admin@labex.io');
Query OK, 1 row affected (0.02 sec)

mysql> insert into user values(2, 'user1', 'user1@gmail.com');
Query OK, 1 row affected (0.00 sec)
```

Successfully inserted 2 data.
Use `select * from <table_name>;` to check the data of a table:

```sql
mysql> select * from user;
+------+-------+-----------------------+
| id   | name  | email                 |
+------+-------+-----------------------+
|    1 | admin | admin@labex.io        |
|    2 | user1 | user1@gmail.com       |
+------+-------+-----------------------+
2 rows in set (0.00 sec)
```

Now we have learnt basic how to create database & table, insert records and query records. Is it quite simple? 


![image desc](https://labex.io/upload/B/A/G/3obnIOT26eML.png)


### 2.3 Constraint

As a relational database, MySQL can restrain some operations with constraint. For example, while inserting data, you can check whether the data is restrained. If not, refuse the operation. We will demonstrate it by a simple example. 

In the part before, we've created `user` table and inserted 2 data:

```sql
mysql> select * from user;
+------+-------+-----------------------+
| id   | name  | email                 |
+------+-------+-----------------------+
|    1 | admin | admin@labex.io        |
|    2 | user1 | user1@gmail.com       |
+------+-------+-----------------------+
```

Now insert a data again: 

```sql
mysql> insert into user values(3, 'user2', 'user1@gmail.com');
Query OK, 1 row affected (0.01 sec)

mysql> select * from user;
+------+---------+-----------------------+
| id   | name    | email                 |
+------+---------+-----------------------+
|    1 | admin   | admin@labex.io        |
|    2 | user1   | user1@gmail.com       |
|    3 | user2   | user1@gmail.com       |
+------+---------+-----------------------+
3 rows in set (0.00 sec)
```

The data is successfully inserted, but here's a problem: as for a launched database, we don't usually allow users with same emails exist in the user table, which means, the e`mail` field should have a unique constraint. What do wo do now? As for a existed table, we can change the field by `alter` command to set the unique constraint:

```mysql
mysql> alter table user modify email varchar(64) unique;
ERROR 1062 (23000): Duplicate entry 'user1@gmail.com' for key 'email'
mysql> delete from user where id = 3;
Query OK, 1 row affected (0.00 sec)

mysql> alter table user add constraint unique (email);
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> insert into user values(3, 'user2', 'user1@gmail.com');
ERROR 1062 (23000): Duplicate entry 'user1@gmail.com' for key 'email'
```

In the commands above, first, we try to edit `email` field to set the unique constraint, but the database reports error, because there's a repeated email record in` user` table. Next, we use `delete from user where id = 3;` to delete the repeated record. The meaning of this command is to delete records with the id of 3. Then, we successfully set the unique index of `email`, and then it will be forbidden while inserting repeated record. There's another way to add the unique constraint: `alter table user modify email varchar(64) unique;`. Actually it adds the unique index by editing the field. 


![image desc](https://labex.io/upload/R/H/U/cBE6qmhIfTC7.png)


There's one more constraint, which is across the tables. While inserting data into the table, we require that one field value of the data should already exists in other tables, like foreign key constraint. If it doesn't meet the foreign key constraints while inserting data. If the foreign key constraint is damaged while deleting data, it would also forbid deleting data. When the foreign key constraint is created, primary key must exists in another table. The primary key can determine the number of a certain row. Next, we will try to create a `course` list with foreign key constraint. Before creating table, we need to set primary key in `user` table:

```sql
mysql> alter table user add constraint pk_id primary key (id);                                    Query OK, 0 rows affected (0.14 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> describe user;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int(10)     | NO   | PRI | NULL    |       |
| name  | varchar(20) | YES  | UNI | NULL    |       |
| email | varchar(64) | YES  | UNI | NULL    |       |
+-------+-------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```


![image desc](https://labex.io/upload/C/N/M/TcVbQmIZ5SL9.png)


Successfully set `id` field as primary key in `user` by `alter` command. And we've certainly found that `id` row becomes primary key by `describe user;`(because the value of row key is PRI, which means primary). Next, create `course` table: 

```sql
mysql> create table course 
    -> (
    -> id int(10) auto_increment,
    -> name varchar(64),
    -> teacher_id int(10),
    -> primary key (id),
    -> constraint fk_user foreign key (teacher_id) references user(id)
    -> );
Query OK, 0 rows affected (0.04 sec)
```

The commands above has more content than command for creating table. First, we use `auto_increment` to set the field `id` in automatically increasing mode. Then, we won't have to assign this field while inserting data. After inserting data, this field would automatically increase. Next, by `primary key (id) `, we assign the primary key of the table as `id`, and assign the field `teacher_id` as foreign key, and associate the` id` field of user table. Now, try to insert data which doesn't exist in `user` table before into `course` table:

```sql
mysql> insert into course(name, teacher_id) values('Python basics', 100);
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`labex`.`course`, CONSTRAINT `fk_user` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`))
```

You can see the insert is failed, because there's no data with an `id` of 100 in `user` table, so it doesn't meet the foreign key constraint. While deleting data, it would also fail deleting if it violates the foreign key constraint:

```sql
mysql> select * from user;
+----+-------+-----------------------+
| id | name  | email                 |
+----+-------+-----------------------+
|  1 | admin | admin@labex.io        |
|  2 | lxttx | lxttx@gmail.com       |
+----+-------+-----------------------+
2 rows in set (0.00 sec)

mysql> insert into course(name, teacher_id) values('Python basics', 2);
Query OK, 1 row affected (0.00 sec)

mysql> select * from course;
+----+---------------+------------+
| id | name          | teacher_id |
+----+---------------+------------+
|  2 |Python basic   |          2 |
+----+---------------+------------+
1 row in set (0.00 sec)

mysql> delete from user where id = 2;
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`labex`.`course`, CONSTRAINT `fk_user` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`))
```

In the example above, to demonstrate the failed situation, we insert a data in `course` table, then we try to delete the data with an `id` of 2 from `user` table but failed. That is because if we delete it, we would violate the existed foreign key constraint. 


![image desc](https://labex.io/upload/I/A/B/mIcitgRSvpdd.png)



We need to query across tables many times, like when you want to know the course name, teacher name and email information: 

```sql
mysql> select * from course join user on course.teacher_id = user.id;
+----+---------------+------------+----+-------+-----------------+
| id | name          | teacher_id | id | name  | email           |
+----+---------------+------------+----+-------+-----------------+
|  2 | Python basic  |          2 |  2 | lxttx | lxttx@gmail.com |
+----+---------------+------------+----+-------+-----------------+
1 row in set (0.00 sec)
```

In the example above, we use `join` command for union query. The keyword `on` assigns the union method of 2 tables.  


![image desc](https://labex.io/upload/P/N/U/Ih0nDHXfMydO.png)


## 3. Summary 

After learning the content above, we are capable of some basic oprerations of MySQL. MySQL is profound and involved with tons of knowledge. For further study of MySQL, you can learn other courses in labex and refer to more MySQL docs.
