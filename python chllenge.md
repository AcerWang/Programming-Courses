# Immutable dictionary

## 1. Introduction

In Python, `dict` is a basic and core data structure and can be used to store key/value pairs. In Web application, it can be used to store http header. Actually, when server receiving http header, the information in the header remains the same all the time, so it's reasonable to store these information in an immutable data strucure.

## 2. Task

In this challenge, you need to implement a data structure named `ImmutableDict` in `/home/labex/Code/immutabke_dict.py`, any instance of it is not allowed to change its data. Operation of changing the data will result in throwing `TypeError` exception. Instance of `ImmutableDict` class should pass the following test:

```python
In [6]: d = ImmutableDict(Connection='keep-alive', Host='https://labex.io')

In [7]: d['Connection']
Out[7]: 'keep-alive'

In [8]: d['Host']
Out[8]: 'https://labex.io'

In [9]: d['Host'] = 'test.com'
TypeError: 'ImmutableDict' objects are immutable

In [10]: d.pop('Host')
TypeError: 'ImmutableDict' objects are immutable

In [11]: d.get('Host')
Out[11]: 'https://labex.io'
```

## 3. Requirement

- All code should be in `/home/labex/Code/immutable_dict.py`.
- Implement a class named `ImmutableDict`.
- `ImmutableDict` will provide all data getter methods which Python built-in `Dict` provides.
- Any operation of changing `ImmutableDict` object data will throw a `TypeError` exception.
- Use Python 3 syntax.

## 4. Tips

- Python built-in `Dict` provides all kinds of updating data operation.
- You can use inheriting, and overloading to implement a custom subclass.