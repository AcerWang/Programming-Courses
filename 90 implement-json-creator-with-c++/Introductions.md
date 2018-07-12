---
show: step
version: 1.0
enable_checker: true
---

# Introductions

## 1. Introduction of the Experiment 

In this experiment, we will introduce the basic feature of json and analyze its structure. Then based on the feature and structure of json, we will design the head file.

#### Knowledge Points

- Feature of json 
- History of json 
- Common c++ json libraries

## 2. Introduction of Json

Json is the object notation of javaScript. It's used for transporting data between the server-side and client-side. Though xml has the similar function, however, json is better in some ways. Let's learn the advantages of json briefly.

See this example first：

```json
var LabEx{
  "firstname" : "LabEx",
  "lastname" :  "io",
  "age" : 3
}
```

The feature of it is：

- Independent Language ： json has its own syntax structure, making it easy to read and writer for developers.
- Lightweight ： For example, while using ajax, the data should be loaded and asynchronously read quickly. Json is capable of finishing this job perfectly due to its feature of lightweight.
-  Extensibility ： As an independent language, not only can json be used in js, but also used widely in many languages. If we want to change the language of the server-side, json can decrease the damage of using a new language.

#### 2.1 Compare Json with Xml 

When we need to save the information of 4 students, the following ways can both be used:

json：

```json
{"students":[
   {"name":"LabEx1", "age":"23", "city":"Agra"},
   {"name":"LabEx2", "age":"28", "city":"Delhi"},
   {"name":"LabEx3", "age":"32", "city":"Chennai"},
   {"name":"LabEx4", "age":"28", "city":"Bangalore"}
]}
```

xml ：

```xml
<students>
  <student>
    <name>LabEx1</name> <age>23</age> <city>Agra</city>
  </student>
  <student>
    <name>LabEx2</name> <age>28</age> <city>Delhi</city>
  </student>
  <student>
    <name>LabEx3</name> <age>32</age> <city>Chennai</city>
  </student>
  <student>
    <name>LabEx4</name> <age>28</age> <city>Bangalore</city>
  </student>
</students>
```

By seeing the codes above, it's obvious to tell that json is much concise than xml. Besides, there're many unique advantages of json that xml doesn't have. 

#### 2.2 Main Structure of Json 

- The set of name/key-value
  In most languages, it's implemented as object, record, structure, dictionaries, hash table, keyed list and associative array.
- Ordered list of values
  In most languages, it's implemented as array, vector, list and sequence

Object：It's a disordered set of name/key-value. An object begins with '{' and ends with '}'. Evey name heel ":'' is seprated with name/key-value:

Array：An ordered set of array value. An array begins with '[' and ends with ']', the value is seprated with ','. 

Value: The value using quotes can be string, number or bool, in addtion, an object or array. These structures can be nested.

String: String is zero or multiple sequences of Unicode characters. Use backslash to escape in quotes. A characte means a string.

Number: Number is quite like the number type of C and Java, but not in octal or hexadecimal system.

json Data Structure Type

- json object
- json array
- Nested json object


json object：

```json
var labex = {
  "name" : "labex.io",
  "age" : "3",
  "website" : "labex.io"
};
```

json array：

```json
var students = [{
   "name" : "labex1",
   "age" :  "29",
   "gender" : "male"

},
{
   "name" : "labex2",
   "age" : "32",
   "gender" : "male"

},
{
   "name" : "labex3",
   "age" : "27",
   "gender" : "female"
}];
```

Nested json object：

```json
var students = {
  "steve" : {
  "name" : "Steve",
  "age" :  "29",
  "gender" : "male" 
},

"pete" : {
  "name" : "Peter",
  "age" : "32",
  "gender" : "male"
},

"sop" : {
  "name" : "Sophie",
  "age" : "27",
  "gender" : "female"
}
}
```

## 3. Common c++ json libraries

In the offcial website of json, we can see many json libraries. rapidjson ，jsoncpp ，json++ are what we are familiar with. 

rapidjson：

- Cross-platform
  - Compiler：Visual Studio, gcc, clang, etc. 
  - Framwork：x86, x64, ARM, etc. 
  - Operating system：Windows, Mac OS X, Linux, iOS, Android, etc.
- Easy installation 
  - The library only has a head file. All you need is to copy it into your project. 
- Independent
  - Not relying on STL, BOOST, etc.
  - Only containing ,, ,, ,.
- Not using C++ exceptions or RTTI
- High performance
  - Use template and inline function to lower the overhead of the function call.
  - The internal optimized Grisu2 & The parsing and implementation of float.
  - Selective support of SSE2/SSE4.2.


jsoncpp：

- The json document for reading and writing.
- While parsing, add the comment of C++ style to elements.
- Rewrite JSON document and save the original document. 

JSON++：

- JSON Parser is based on C++11。
- It parses string and file of JSON format, and generates a memory tree representing the JSON structure.
- JSON object maps to standard basb table, array and vector.
- JSON type maps to c++ type. 
- Use standard class library instead of adding extra function libraries.

## 4. Use Stack to Control the Format of  Json  

In this experiment, we will use stack to store the depth of json objects. The depth is used to control the format of the outputted json(like punctuation marks, indentation and line feeds), making the outputted beautiful, neat and readable.

Stack is a container adapter, specially designed for LIFO, where elements can only be inserted and extracted on one side of the container. The underlying layer can be the template of any standard container class or some other specially designed container classes. The container should be able to support the following oprerations:

- empty    Test whether the container is empty 
- size     Return the size 
- top      Return the stack top element
- push     Push elements 
- emplace  Construct and insert elements
- pop      Delete the stack top element
- swap     Swap the contents

## 5. Write `json-writer.h`

The first thing to consider is, json has mainly two types: array and object. So let's write an enum type：

```cpp
enum ContainerType{
  CONTAINER_TYPE_ARRAY,        
  CONTAINER_TYPE_OBJECT
};
```

The layout of json has mainly 3 types： Inheriting the format of parent class, single line element and multiple line element:

```cpp
enum ContainerLayout {
        CONTAINER_LAYOUT_INHERIT,
        CONTAINER_LAYOUT_MULTI_LINE,
        CONTAINER_LAYOUT_SINGLE_LINE
    };
```

In additon, if you want the output can be conpressed, which means, decrease whitespaces and feeding lines, then you can write this function `ConfigureCompressedOutput()`：

```cpp
void ConfigureCompressedOutput ()
    {
        SetIndent ("");
        SetContainerPadding ("");
        SetKeyPaddingLeft ("");
        SetKeyPaddingRight ("");
        SetDefaultContainerLayout (CONTAINER_LAYOUT_SINGLE_LINE);
        SetForceDefaultContainerLayout (true);
    }
```

The function of the program is, outputting the json objects to the screen or files. So we overloaded the `write` function. When there's not a specify file, output it to the standard screen; when there's an output file, output to the file: 

```cpp
std::ostream& Write ()
    {
        if (writer == NULL)
            return std::cout;
        return *writer;
    }
```

In the last paragraph, we have introduced stack, and it can be used here now. Let's construct a `Container` structure and assign its initial value:

```cpp
struct Container{
  ContainerType type;
  ContainerLayout layout;
  bool isKey;
  int childCount;

  Container (ContainerType type, ContainerLayout layout):
          type (type),
          layout (layout),
          isKey (false),
          childCount (0)
  {}
};
std::stack<Container *> depth;
```

`isKey` is used to judge if the element is a key or a value. The layouts and marks of keys and values are different, so they should be treated differently. 

Indentation plays a vital role in our program. So corresponding functions for different situations have been written.

```cpp
int GetInitialIndentDepth () { return initialIndentDepth; }
void SetInitialIndentDepth (int depth) { initialIndentDepth = depth; }

const char *GetIndent () { return indent; }
void SetIndent (const char *indent) { this->indent = indent; }
```

There's a similar function about layout, which means the control of whitespaces in the left and right:

```cpp
const char *GetContainerPadding () { return containerPadding; }
void SetContainerPadding (const char *padding) { containerPadding = padding; }

const char *GetKeyPaddingLeft () { return keyPaddingLeft; }
void SetKeyPaddingLeft (const char *padding) { keyPaddingLeft = padding; }

const char *GetKeyPaddingRight () { return keyPaddingRight; }
void SetKeyPaddingRight (const char *padding) { keyPaddingRight = padding; }
```

## 6. Genericity and Overload

We know that, in different platforms, the length of data varys. So we can use the data types irrelevant to the platforms:

| **Identification** | Equivalent to        | Signed/Unsigned | Bits | Bytes | 最小值                     | 最大值                     |
| ------------------ | -------------------- | --------------- | ---- | ----- | -------------------------- | -------------------------- |
| `int8_t`           | `signed char`        | Signed          | 8    | 1     | −128                       | 127                        |
| `uint8_t`          | `unsigned char`      | Unsigned        | 8    | 1     | 0                          | 255                        |
| `int16_t`          | `short`              | Signed          | 16   | 2     | −32,768                    | 32,767                     |
| `uint16_t`         | `unsigned short`     | Unsigned        | 16   | 2     | 0                          | 65,535                     |
| `int32_t`          | `int`                | Signed          | 32   | 4     | −2,147,483,648             | 2,147,483,647              |
| `uint32_t`         | `unsigned int`       | Unsigned        | 32   | 4     | 0                          | 4,294,967,295              |
| `int64_t`          | `long long`          | Signed          | 64   | 8     | −9,223,372,036,854,775,808 | 9,223,372,036,854,775,807  |
| `uint64_t`         | `unsigned long long` | Unsigned        | 64   | 8     | 0                          | 18,446,744,073,709,551,615 |

`VALUE_DEF(t)` means the value, used when the arry list is full of single values. For instance, "short-array": [ 1, 188900967593046, 3.14159 ]. `KEYVALUE_DEF(t)` means key-value, used for hash table, like "animal": "cat", "life-expectancy": "forever".

If `value()` can only append the value of `int` type, then we need to write many functions to finish the program, and calling them won't be a easy thing to do. Now is the show time for genericity: It can implement all the formats by one function, which means, all the functions above can be implemented by it. But there're can be problems regrading to `string ，char* and bool`: the internal oprerations of the functions are different. We can implement by overloading:

```cpp
#define VALUE_DEF(t) void Value (t value) { StartChild (); Write () << value; }
#define KEYVALUE_DEF(t) void KeyValue (const char *key, t value) { Key (key); Value (value); }

VALUE_DEF(int8_t)
VALUE_DEF(uint8_t)
VALUE_DEF(int16_t)
VALUE_DEF(uint16_t)
VALUE_DEF(int32_t)
VALUE_DEF(uint32_t)
VALUE_DEF(int64_t)
VALUE_DEF(uint64_t)
VALUE_DEF(float)
VALUE_DEF(double)

void KeyNullValue (const char *key) { Key (key); NullValue (); }

KEYVALUE_DEF(const char *)
KEYVALUE_DEF(std::string)
KEYVALUE_DEF(bool)
KEYVALUE_DEF(int8_t)
KEYVALUE_DEF(uint8_t)
KEYVALUE_DEF(int16_t)
KEYVALUE_DEF(uint16_t)
KEYVALUE_DEF(int32_t)
KEYVALUE_DEF(uint32_t)
KEYVALUE_DEF(int64_t)
KEYVALUE_DEF(uint64_t)
KEYVALUE_DEF(float)
KEYVALUE_DEF(double)

void Value (const char *value);
void Value (std::string value);
void Value (bool value);
```

## 7. Core Functions

There're several function left unintroduced. They will be implemented in `json-write.cpp`. Let's make a declarition in the head file: 

```cpp
void WriteEscapedChar (char c);
void WriteString (const char *str);
void StartChild (bool isKey);
void StartChild () { StartChild (false); }
void EndContainer ();
void Key (const char *key);
void NullValue ();
```

Here's the source code of the head file `json-writer.h` , make sure this file is in `/home/labex/Code`：

```cpp
#ifndef _JSONWRITER_H
#define _JSONWRITER_H

#include <iostream>
#include <string>
#include <stack>

class JsonWriter
{
public:

    enum ContainerType {
        CONTAINER_TYPE_ARRAY,
        CONTAINER_TYPE_OBJECT
    };

    enum ContainerLayout {
        CONTAINER_LAYOUT_INHERIT,
        CONTAINER_LAYOUT_MULTI_LINE,
        CONTAINER_LAYOUT_SINGLE_LINE
    };

    explicit JsonWriter () :      
        writer (NULL),
        initialIndentDepth (0),
        indent ("  "),
        containerPadding (" "),
        keyPaddingLeft (""),
        keyPaddingRight (" "),
        defaultContainerLayout (CONTAINER_LAYOUT_MULTI_LINE),
        forceDefaultContainerLayout (false)
    {
    }

    void ConfigureCompressedOutput ()
    {
        SetIndent ("");
        SetContainerPadding ("");
        SetKeyPaddingLeft ("");
        SetKeyPaddingRight ("");
        SetDefaultContainerLayout (CONTAINER_LAYOUT_SINGLE_LINE);
        SetForceDefaultContainerLayout (true);
    }

    std::ostream *GetWriter () { return writer; }
    void SetWriter (std::ostream *writer) { this->writer = writer; }

    int GetInitialIndentDepth () { return initialIndentDepth; }
    void SetInitialIndentDepth (int depth) { initialIndentDepth = depth; }

    const char *GetIndent () { return indent; }
    void SetIndent (const char *indent) { this->indent = indent; }

    const char *GetContainerPadding () { return containerPadding; }
    void SetContainerPadding (const char *padding) { containerPadding = padding; }

    const char *GetKeyPaddingLeft () { return keyPaddingLeft; }
    void SetKeyPaddingLeft (const char *padding) { keyPaddingLeft = padding; }

    const char *GetKeyPaddingRight () { return keyPaddingRight; }
    void SetKeyPaddingRight (const char *padding) { keyPaddingRight = padding; }

    ContainerLayout GetDefaultContainerLayout () { return defaultContainerLayout; }
    void SetDefaultContainerLayout (ContainerLayout layout) { defaultContainerLayout = layout; }

    bool GetForceDefaultContainerLayout () { return forceDefaultContainerLayout; }
    void SetForceDefaultContainerLayout (bool force) { forceDefaultContainerLayout = force; }

    std::ostream& Write ()
    {
        if (writer == NULL)
            return std::cout;
        return *writer;
    }

    void WriteEscapedChar (char c);
    void WriteString (const char *str);

    void StartChild (bool isKey);
    void StartChild () { StartChild (false); }

    void StartContainer (ContainerType type, ContainerLayout layout);
    void EndContainer ();

    void StartArray () { StartContainer (CONTAINER_TYPE_ARRAY, CONTAINER_LAYOUT_INHERIT); }
    void StartArray (ContainerLayout layout) { StartContainer (CONTAINER_TYPE_ARRAY, layout); }
    void StartShortArray () { StartContainer (CONTAINER_TYPE_ARRAY, CONTAINER_LAYOUT_SINGLE_LINE); }
    void EndArray () { EndContainer (); }

    void StartObject () { StartContainer (CONTAINER_TYPE_OBJECT, CONTAINER_LAYOUT_INHERIT); }
    void StartObject (ContainerLayout layout) { StartContainer (CONTAINER_TYPE_OBJECT, layout); }
    void StartShortObject () { StartContainer (CONTAINER_TYPE_OBJECT, CONTAINER_LAYOUT_SINGLE_LINE); }
    void EndObject () { EndContainer (); }

    void Key (const char *key);

    void NullValue ();
    void Value (const char *value);
    void Value (std::string value);
    void Value (bool value);

    #define VALUE_DEF(t) void Value (t value) { StartChild (); Write () << value; }
    #define KEYVALUE_DEF(t) void KeyValue (const char *key, t value) { Key (key); Value (value); }

    VALUE_DEF(int8_t)
    VALUE_DEF(uint8_t)
    VALUE_DEF(int16_t)
    VALUE_DEF(uint16_t)
    VALUE_DEF(int32_t)
    VALUE_DEF(uint32_t)
    VALUE_DEF(int64_t)
    VALUE_DEF(uint64_t)
    VALUE_DEF(float)
    VALUE_DEF(double)

    void KeyNullValue (const char *key) { Key (key); NullValue (); }

    KEYVALUE_DEF(const char *)
    KEYVALUE_DEF(std::string)
    KEYVALUE_DEF(bool)
    KEYVALUE_DEF(int8_t)
    KEYVALUE_DEF(uint8_t)
    KEYVALUE_DEF(int16_t)
    KEYVALUE_DEF(uint16_t)
    KEYVALUE_DEF(int32_t)
    KEYVALUE_DEF(uint32_t)
    KEYVALUE_DEF(int64_t)
    KEYVALUE_DEF(uint64_t)
    KEYVALUE_DEF(float)
    KEYVALUE_DEF(double)

private:

    std::ostream *writer;
    int initialIndentDepth;
    const char *indent;
    const char *containerPadding;
    const char *keyPaddingLeft;
    const char *keyPaddingRight;
    ContainerLayout defaultContainerLayout;
    bool forceDefaultContainerLayout;

    struct Container {
        ContainerType type;
        ContainerLayout layout;
        bool isKey;
        int childCount;

        Container (ContainerType type, ContainerLayout layout) :
            type (type),
            layout (layout),
            isKey (false),
            childCount (0)
        {
        }
    };

    std::stack<Container *> depth;

    void Indent ();
};

#endif /* _JSONWRITER_H */
```

```checker
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/Code/json-writer.h
  error: Sorry, you didn't create file "json-writer.h" in /home/labex/Code!
  timeout: 3
```

## 8. Summary

In this course, first we got to know the features of json. Second, we designed the class `JsonWriter` to generate json files by these features. The content in the next course is implementing the functions in `JsonWriter`

## 9. Reference

[json.org](http://www.json.org/)
