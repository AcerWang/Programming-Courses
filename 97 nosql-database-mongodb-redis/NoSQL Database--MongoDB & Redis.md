---
show: step
version: 1.0
enable_checker: false
---
# NoSQL Database 

## 1. Introduction 

Websites nowadays want the data storage more and more flexible. Under this requirement, NoSQL, non-relational database, is getting more and more pupular. The so-called non-relational database means the database that doesn't use SQL to operate the data. Database of this kind doesn't have a settled mode to save data, doesn't support `join` in data table, and it can horizontal scale easily. There're many kinds of NoSQLs, among them, MongoDB and Redis are the most commonly used. In the experiment, we will learn basic MongoDB and Redis, and how to visit these databases by Python code. 

#### Learning Objective:

- Basic MongoDB  
- Basic Redis 
- Use Python to visit MongoDB and Redis 

## 2. MongoDB

MongoDB is a very popular NoSQL database, supporting automatically horizontal scaling. Meanwhile, it's also called document database, because the data is saved in the format of document(BSON object, like JSON). In MongoDB, the structure of saving data is mainly divided in 4 layers:  
- Database example, like an app uses a database  
- collection: document collection. A database is consisted of multiple document sets, like the tables in MySQL 
- document: A document represents a data, like a JSON object, corresponding to a record in MySQL table 

The data saved in MongoDB is schema-less. Fpr example, all the documents in a collection don't need to have the same structure, whcih means, while inserting different data in a same table, these data don't need to have the same fields. Compeletly different from NoSQL, when a table is created in MySQL, the filed of the data is already decided, and only the data of the same structure can be inserted into it.  

This experiment is based on  MongoDB 3.4.

### 2.1 Environment Preparations 

MongoDB has been installed in LabEx environment. You need to start MongoDB every
time after you start the experiment. As you launched the terminal in the desktop, launch the database by the following commands:  

```sh
$ sudo service mongodb start
```

When the database is successfully started, linke to the database by the commands below:  

```sh
$ mongo
```

`Mongo` is the client-side shell of MongoDB. You can assign the MongoDB address to connect to when you execute the command, if you don't, it would connect to the default address. By default, MongoDB would listen to the address in `127.0.0.1:27017 `. 
All the MongoDB commands in this course will be inputted based on `mongo shell`. 
As for using Python to visit MongoDB, you need to install `PyMongo` package, which has implemented the MongoDB drive of Python. Build the work environment by the commands below and install the package: 

```shell
$ cd ~/Code
$ sudo pip install virtualenv
$ virtualenv -p /usr/bin/python3.5 env
$ source env/bin/activate
$ sudo pip3 install pymongo lPython
```

Note that we use `virtualenv` environment here, and assign the python 3.5 version. And the package needed in the installation can be `pip`, which is the 
corresponding package of the Python 3.5 by default.  

The command above has created a `virtualenv` environment under directory `Code`. Then, the needed package have been installed in the virtual environment. The subsequent interactive commands will all be inputted by `lPython` terminal:

```sh
$ source env/bin/activate
$ IPython
```

In the subsequent code, characters like `In [1]` is the prompt of python, you don't need to input it.  

### 2.2 CRUD Operation

The document record saved in MongoDB is a BSON object. Like JSON object, it's consisted of key-value. Take a user record for example:  

```python
{
    name: "admin",
    age: 30,
    email: "admin@labex.io"
}
```

Every document has a `_id` field, which is a main key, used for deciding a unique record. If you don't assign the `_id` field while inserting data in MongoDB, then a `_id` field would be automatically generated, with the type of [ObjectId](https://docs.mongodb.com/manual/reference/bson-types/#objectid) and the length of `12 bytes`. The fiedls in MongoDB support types like string, number, timestamp and so on. The biggest document can be 16M, which is capable of saving many data.  

First, try to insert a data in MongoDB:  

```sql
$ mongo
> use labex
> db.user.insertOne({name: "admin", age: 30, email: "admin@labex.io", addr: ["CD", "SH"]})
{
        "acknowledged" : true,
        "insertedId" : ObjectId("59a8034064e0acb13483d512")
}
> show databases;
admin      0.000GB
config     0.000GB
labex      0.000GB
local      0.000GB
> show collections;
user
```


![image desc](https://labex.io/upload/P/J/K/vvHcXTwClSpi.png)


As you can see, by command `use`, we switch to `LabEx` database before inserting data. Though the database is doesn't exist for now, but when we insert data in it, the database would be automatically created. `show databases` shows the currently existed database and `show collections` shows the document collection of the current database. When the data is inserted, `_id` field is automatically appended. You can use `db.collection.insertMany` method to insert multiple data:  

```sql
> db.user.insertMany([
... {name: "user1", age: 28, email: "user1@labex.io", addr: ["NY", "Soul"]},
... {name: "user2", age: 31, email: "user2@labex.io", addr: ["GZ", "SZ"]},
... {name: "user3", age: 26, email: "user3@labex.io", addr: ["NJ", "AH"]}
... ])
{
        "acknowledged" : true,
        "insertedIds" : [
                ObjectId("59a8034564e0acb13483d513"),
                ObjectId("59a8034564e0acb13483d514"),
                ObjectId("59a8034564e0acb13483d515")
        ]
}
```


![image desc](https://labex.io/upload/T/H/E/6OV5B1WTzTgQ.png)


Method `db.collection.find` is used to query data. And you can assign the filter condition:  

```sql
> db.user.find()
{ "_id" : ObjectId("59a8034064e0acb13483d512"), "name" : "admin", "age" : 30, "email" : "admin@labex.io", "addr" : [ "CD", "SH" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d513"), "name" : "user1", "age" : 28, "email" : "user1@labex.io", "addr" : [ "NY", "Soul" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d514"), "name" : "user2", "age" : 31, "email" : "user2@labex.io", "addr" : [ "GZ", "SZ" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d515"), "name" : "user3", "age" : 26, "email" : "user3@labex.io", "addr" : [ "NJ", "AH" ] }

> db.user.find({name: "user1"})
{ "_id" : ObjectId("59a8034564e0acb13483d514"), "name" : "user1", "age" : 28, "email" : "user@labex.io", "addr" : [ "GZ", "SZ" ] }

> db.user.find({age: {$gt: 30}})
{ "_id" : ObjectId("59a8034564e0acb13483d514"), "name" : "user2", "age" : 31, "email" : "user2@labex.io", "addr" : [ "GZ", "SZ" ] }

> db.user.find({addr: "CD"})
{ "_id" : ObjectId("59a8034064e0acb13483d512"), "name" : "admin", "age" : 30, "email" : "admin@labex.io", "addr" : [ "CD", "SH" ] }
```

In the example above, first we use `db.user.find()` to get all the data inserted before. Second, we query with different filer conditions. Take `{age: {$gt: 30}}` for example, it means query the users older than 30. Besides, it's also easy to find whether a certain element exists in the array. The example above queried out all the users whose address contains `CD`.


![image desc](https://labex.io/upload/F/S/K/A026ifXATl7X.png)

The query function of MongoDB is very powerfull. It can combine all kinds of query condition. For more operating methods, you can learn other courses in LabEx. By `db.user.updateOne` or `db.user.updateMany`, you can update the data. The former updates one record, and the latter update multiple records:

```sql
> db.user.updateOne(
... {name: "admin"},
... {$set: {age: 29, addr: ["CD", "SH", "BJ"]}}
... )
{ "acknowledged" : true, "matchedCount" : 1, "modifiedCount" : 1 }
> db.user.find({name: "admin"})
{ "_id" : ObjectId("59a8034064e0acb13483d512"), "name" : "admin", "age" : 29, "email" : "admin@labex.io", "addr" : [ "CD", "SH", "BJ" ] }
```

![image desc](https://labex.io/upload/R/M/U/zCKtXxngBmXK.png)


You can see that a record as been successfully updated. Besides, deleting data is also quite easy, just use method `db.user.deleteMany` or `db.user.deleteOne`:

```sql
> db.user.deleteMany({addr: "CD"})
{ "acknowledged" : true, "deletedCount" : 2 }
> db.user.find()
{ "_id" : ObjectId("59a8034564e0acb13483d514"), "name" : "user1", "age" : 28, "email" : "user1@labex.io", "addr" : [ "GZ", "SZ" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d515"), "name" : "user2", "age" : 31, "email" : "user2@labex.io", "addr" : [ "GZ", "SZ" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d516"), "name" : "user3", "age" : 26, "email" : "user3@labex.io", "addr" : [ "NJ", "AH" ] }
```

The commands above can successfully delete the user whos address contains "CD". 2 records have been deleted in total. 


![image desc](https://labex.io/upload/X/P/G/6ZH3ajs0vvap.png)


### 2.3 MongoDB with Python

Visiting MongoDB database in Python is usually relied on [PyMongo](https://api.mongodb.com/python/current/tutorial.html)  package. This package contains a `MongoClient` object, which can be used to build `MongoDB` client-side. Input the following code in `lPython` to create client-side:  

```python
In [2]: from pymongo import MongoClient

In [3]: client = MongoClient('127.0.0.1', 27017)

In [4]: db = client.labex
```

We've learnt that Mongo listens address `127.0.0.1:27017` by default. So while creating `client`, this address is used. When the client side is created, we use `client.LabEx` to choose `LabEx` database. Then you can query all the files:


```python
In [13]: for user in db.user.find():
    ...:     print(user)
    ...:
{ "_id" : ObjectId("59a8034564e0acb13483d514"), "name" : "user1", "age" : 28.0, "email" : "user1@labex.io", "addr" : [ "GZ", "SZ" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d515"), "name" : "user2", "age" : 31.0, "email" : "user2@labex.io", "addr" : [ "GZ", "SZ" ] }
{ "_id" : ObjectId("59a8034564e0acb13483d516"), "name" : "user3", "age" : 26.0, "email" : "user3@labex.io", "addr" : [ "NJ", "AH" ] }
```


![image desc](https://labex.io/upload/A/M/V/hEDLE1COXSym.png)


It's also easy to insert data by `PyMongo`, just use method `insert_one`:

```python
In [14]: user = {'name': 'admin', 'age': 30, 'addr': ['CD', 'SH', 'BJ']}

In [15]: db.user.insert_one(user)
Out[15]: <pymongo.results.InsertOneResult at 0x10730aa08>
In [17]: db.user.find_one({'name': 'admin'})
Out[17]:
{'_id': ObjectId('59a80988a75acb3615913dc6'),
 'addr': ['CD', 'SH', 'BJ'],
 'age': 30,
 'name': 'admin'}
```

After the data is inserted, we use `find_one` to query the record(The query method is quite the same as mongo shell). We find that, `email` fiedl hasn't been set. We can update the record by `update_one` method: 

```python
In [19]: db.user.update_one({'name': 'admin'}, {'$set': {'email': 'admin@labex.io'}})
Out[19]: <pymongo.results.UpdateResult at 0x1070dce08>

In [20]: db.user.find_one({'name': 'admin'})
Out[20]:
{'_id': ObjectId('59a80988a75acb3615913dc6'),
 'addr': ['CD', 'SH', 'BJ'],
 'age': 30,
 'email': 'admin@labex.io',
 'name': 'admin'}
```

As you might have found, many operations of PyMongo are similar to mongo shell. It's quite simple.  


![image desc](https://labex.io/upload/F/C/V/8Gyoolo4Xp7f.png)


## 3. Redis

Redis, a memory database, uses Key-value to save data. As most of its data is saved in the memory, so the speed of visiting is impressively fast. So Redis is largely used in cache system to save hot spot data, to increase the response speed of websites largely. Comparing with oterh memory database, Redis has the following advantages:  

- Support the persistence of data. With configuration, the data in memory can be saved in disk. When Redis restarts, the data will be loaded into the memory again. 
- Support data structures like list, Hash, sorted sets and so on, largely extends to usage of Redis. 
- Support atomic operation. All the oprerations of Redis is atomic, making it easy to implement distributed locks based on Redis.  
- Support publishing and subscripting. Support data expiring.  

### 3.1 Environment Preprations 

Redis has been installed in LabEx environment. After launching the experiment every time, you need to lauch Redis manually. When you have launched the terminal in the desktop, launch the database by the command below:  

```sh
$ sudo service redis-server start
```

As database lauched, link to the database by the command below:  

```sh
$ redis-cli
127.0.0.1:6379>
```

`redis-cli` is the client-side shell of Redis. While executing this command, you can assign information like the service address of the Redis you connect to. Redis service listens `127.0.0.1:6379` by default. All the subsequent Redis operation commands are based on `redis-cli`. 
As for using Python to visit Redis，we need to install `redis-py` package first. It contians the Redis drive of python. Build the work environment and install the package by the commands below:  

```sh
$ cd ~/Code
$ sudo pip install virtualenv
$ virtualenv -p /usr/bin/python3.5 env
$ source env/bin/activate
$ pip install redis IPython
```

The commands above created a `virtualenv` environment under `Code` directory. Next, it installed the package needed in the virtual environment. The subsequent interactive commands are inputted by `lPython` terminal. You can launch lPython terminal by the commands below: 

```sh
$ source env/bin/activate
$ lPython
```

In the subsequent code, characters like `In [1]` is the prompt of python, you don't need to input it. 

`Basic Operations`

Redis is a Key-Value memory database, with all the operations executed by commands. For example, `SET` command can set the key-value, and `GET` can get the value of a key. For different data structures, Redis has dozens of different commands. We will introduce some common commands next: 

Redis has many kinds of commands for key, whihc mainly are(In the commands below, all the strings in lowercase are parameters for you to define by yourself): 

- `SET key value`: Set key value 
- `EXISTS key`: Judge whethe key exists 
- `EXPIRE key seconds`: Set the expiring time of the key, then it will be automatically deleted when it's expired 
- `TTL key`: Get the left surviving time of key  
- `DEL key`: Delete key 
- `TYPE key`: Get the corresponding type of the key   

Demonstrate the commands above by redis-cli:

```sh
$ redis-cli
127.0.0.1:6379> exists user
(integer) 0
127.0.0.1:6379> set user admin
OK
127.0.0.1:6379> get user
"admin"
127.0.0.1:6379> type user
string
127.0.0.1:6379> expire user 5
(integer) 1
127.0.0.1:6379> ttl user
(integer) -2
127.0.0.1:6379> exists user
(integer) 0
```

First, judge whether `user` key exists, and set the value by `SET`. Second, use `EXPIRE` set the expiring time as 5s. You can see that, after 5 seconds, the `user` key will be automatically deleted. 

Sometimes you may find the outputted string has prefix like `b`, which means the byte coding string. The other example is unicode coding string like `u'xxxxx'`. They are all kind of common.  

As we mentioned before, Redis supports other data structures. Besides simple string key-value, it also supports hash key-value. In this data structure, key is related to a hash, and hash contains multiple fields and the corresponding value. As for this type, we have the commands below:


- `HSET key field value`: Set the hash field named key as value 
- `HGET key field`: Get the hash field named key  
- `HGETALL key`: Get all the fields and value named key  
- `HKEYS key`: Get all the hash fields named key   
- `HLEN key`: Get the length of the hash fields named key  

Demonstrate by redis-cli as below: 

```sh
127.0.0.1:6379> exists user
(integer) 0
127.0.0.1:6379> hset user name admin
(integer) 1
127.0.0.1:6379> hset user age 30
(integer) 1
127.0.0.1:6379> hset user email admin@labex.io addr NY
(integer) 2
127.0.0.1:6379> hgetall user
1) "name"
2) "admin"
3) "age"
4) "30"
5) "email"
6) "admin@labex.io"
7) "addr"
8) "NY"
127.0.0.1:6379> hkeys user
1) "name"
2) "age"
3) "email"
4) "addr"
127.0.0.1:6379> hget user addr
"NY"
127.0.0.1:6379> hlen user
(integer) 4
```

In the example above, we set a hash named `user`. First, use `HSET` to assign value to a single field. Second, use `HMSET` to assign value to multiple fields. You can get all the fiedls and values at one time by using `HGETALL`.
(In the 4.0 version of `redis-server`, `HSET` can also set multiple key-value. The redis-server in LabEx environment is this version). 


![image desc](https://labex.io/upload/O/U/U/aHrEx5BCU31C.png)


Redis also supports ordered set, which can implement sorting function quickly. The main operation commands are:   

- `ZADD key score member`: Add the members and the corresponding score to the ordered sets 
- `ZREVRANK key member`: Get the ranking of `member` in the ordered set   

Demonstrate by `redis-cli`:

```sh
127.0.0.1:6379> zadd rank 100 admin
(integer) 1
127.0.0.1:6379> zadd rank 120 user1
(integer) 1
127.0.0.1:6379> zadd rank 80 user2
(integer) 1
127.0.0.1:6379> zrevrank rank admin
(integer) 1
127.0.0.1:6379> zrevrank rank  user
(nil)
127.0.0.1:6379> zrevrank rank  user1
(integer) 0
127.0.0.1:6379> zrevrank rank  user2
(integer) 2
```

In the example above, we add 3 members in `rank` by `ZADD`, and in the end, with `ZREVRANK`, we get the rank of members by order. We can find that, the rank is calculated from 0. The member ranks at 0 has the highest score. In addition, Rerdis has other kinds of operation commands. Due to the limit of passage length, we won't talk about them all.  


![image desc](https://labex.io/upload/P/I/K/mpjM6vu0L0jo.png)


### 3.2 Operate Redis with Python 

Python can visit Redis by [redis-py](https://github.com/andymccurdy/redis-py) . Similar to `PyMongo`, you also need to create a Redis client-side first by code below:  

```python
$ ipython

In [1]: import redis

In [2]: r = redis.StrictRedis(host='127.0.0.1', db=0)

In [3]: r.ping()
Out[3]: True
```

In this code, we created a Redis client-side by `redis.StrictRedis`. Parameter `db` set that the logic database number of the link is `0`. Databases of different numbers can have the key with the same name. After successfully created the client-side, we can make all kinds of operations now. First we tried method `ping`. When it returns `True`, it means the database works normally. `redis-py` client-side has many methods that have the same name with Redis. We can finish all kinds of operations with these methods. Take the hash key `user` created before for example:  

```python
In [4]: r.hgetall('user')
Out[4]:
{b'addr': b'NY',
 b'age': b'30',
 b'email': b'admin@labex.io',
 b'name': b'admin'}
```

You can see that, `redis-py` automatically converts the returned result into a dictionary.   


Sometimes you may find the outputted string has prefix like `b`, which means the byte coding string. The other example is unicode coding string like `u'xxxxx'`. They are all kind of common.  


![image desc](https://labex.io/upload/C/W/S/4974vNUMoG7w.png)


Redis also supports publishing ans subscripting messages mode. This mode implements the decoupling between the publisher and subscripter. The publisher only needs to send data on a certain channel, and the subscripter who has subscripted this channel would get the message automatically. We will demonstrate this next. First, subscript `labreport-channel` channel in `redis-py` client-side, and listen to the message: 

```python
In [5]: p = r.pubsub()

In [6]: p.subscribe('labreport-channel')

In [7]: for msg in p.listen():
   ...:     print(msg)
   ...:
{'type': 'subscribe', 'pattern': None, 'channel': b'labreport-channel', 'data': 1}
```

Then, in `redis-cli` client-side, use command `PUBLISH channel message` to send `message` to this channel:

```sh
127.0.0.1:6379> publish labreport-channel "1 msg from redis-cli"
(integer) 1
127.0.0.1:6379> publish labreport-channel "2 msg from redis-cli"
(integer) 1
127.0.0.1:6379>
```

When it's published, you can see the `lPython` terminal receive the message immediately:  

```python
In [7]: for msg in p.listen():
   ...:     print(msg)
   ...:
{'type': 'subscribe', 'pattern': None, 'channel': b'labreport-channel', 'data': 1}
{'type': 'message', 'pattern': None, 'channel': b'labreport-channel', 'data': b'1 msg from redis-cli'}
{'type': 'message', 'pattern': None, 'channel': b'labreport-channel', 'data': b'2 msg from redis-cli'}
```


![image desc](https://labex.io/upload/V/Q/W/L5p9KOWFKheh.png)

You should open another terminal and enter redis-cli mode, publish some messages so that you can receive these messages in your redis client.

## 4. Summary 

In this experiment, we have learnt the basic knowledge of `MongoDB` and `Redis`.
When we have the kind of projects in the project combats later on, we will talke about these more deepyly. 

Knowledge invovled：

- Basic MongoDB
- Basic Redis
- Use python to visit MongoDB and Redis

NoSQL is quite widely used. Especially in Internet projects, the unstructured data is mostly saved with NoSQL.  
