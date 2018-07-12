---
show: step
version: 1.0
enable_checker: true
---

# Implementation

## 1. Introduction of the Experiment

In this course, we will write the implementing module of the function based on the last course. In the head file, many functions we declared are implemented based on these functions.

#### Knowledge

- Writing the main functions
- Writing a test example

## 2. Analysis

Without a doubt, indentation is very important for a strongly readable data. In python, indentation is even a part of the syntax, and this was exactly what stack is used for. If the indentation size is the same as the depth size:


![image desc](https://labex.io/upload/Y/I/Q/3wldbny0uCqd.png)


```cpp
void JsonWriter::Indent ()
{
    for (int i = 0, s = initialIndentDepth + depth.size (); i < s; i++)
        Write () << indent;
}
```

Both the start and the end of the element should be operated by function `StartContainer` and `EndContainer`. Container means the object or array. Use '[]' for the former and '{}' for the latter：

```cpp
void JsonWriter::StartContainer (ContainerType type, ContainerLayout layout)
{
    if (forceDefaultContainerLayout) {
        layout = defaultContainerLayout;
    } else if (layout == CONTAINER_LAYOUT_INHERIT) {
        if (depth.size () > 0)
            layout = depth.top ()->layout;
        else
            layout = defaultContainerLayout;
    }

    StartChild ();
    depth.push (new Container (type, layout));
    Write () << (type == CONTAINER_TYPE_OBJECT ? '{' : '[');
}
```

In the end of the container, add ']' or ’}‘ ，and finish the corresponding layouts: 

```cpp
void JsonWriter::EndContainer ()
{
    Container *container = depth.top ();
    depth.pop ();

    if (container->childCount > 0) {
        if (container->layout == CONTAINER_LAYOUT_MULTI_LINE) {
            Write () << endl;
            Indent ();
        } else {
            Write () << containerPadding;
        }
    }

    Write () << (container->type == CONTAINER_TYPE_OBJECT ? '}' : ']');

    delete container;
}
```

A start mark and end mark are needed in the container to set the executing process. If the depth of a node is 0, it can be considered a root node. And as for root nodes, indentation will be the only thing to consider. However, for child nodes, the type of element needs to be analyzed. If it's an array of a value in an object, then add ',' while continuing reading. Because data are separated by this mark. The main difference between one row layout and multiple row is line feeding and indentation:

```cpp
void JsonWriter::StartChild (bool isKey)
{
    if (depth.size () == 0) {
        if (initialIndentDepth > 0)
            Indent ();
        return;
    }

    Container *container = depth.top ();
    if (container->childCount > 0 && (
        container->type == CONTAINER_TYPE_ARRAY ||
        (container->type == CONTAINER_TYPE_OBJECT && !container->isKey))) {
        Write () << ",";
        if (container->layout == CONTAINER_LAYOUT_SINGLE_LINE) {
            Write () << containerPadding;
        } else {
            Write () << endl;
            Indent ();
        }
    } else if (container->childCount == 0) {
        Write () << containerPadding;
        if (container->layout == CONTAINER_LAYOUT_MULTI_LINE) {
            Write () << endl;
            Indent ();
        }
    }

    container->isKey = isKey;
    container->childCount++;
}
```

`StartChild` is mainly used for the indentation of objects, elements and key-values & problems in punctuation marks. 

While adding strings, implicitly, there's no quotes in the output, which is not standard. So we need to add marks by ourselves for strings, with considering escape characters: 

```cpp
void JsonWriter::WriteString (const char *str)
{
    Write () << "\"";
    for (int i = 0; str [i] != 0; i++)
        WriteEscapedChar (str [i]);
    Write () << "\"";
}
void JsonWriter::WriteEscapedChar (char c)
{
    switch (c) {
    case '"': Write () << "\\\""; break;
    case '\\': Write () << "\\\\"; break;
    case '\b': Write () << "\\b"; break;
    case '\f': Write () << "\\f"; break;
    case '\n': Write () << "\\n"; break;
    case '\r': Write () << "\\r"; break;
    case '\t': Write () << "\\t"; break;
    default: Write () << c; break;
    }
}
```

In the last course, we've used function `value()`. Now it's time to implement it,as well as `key()` and `NullValue()`：

```cpp
void JsonWriter::Value (const char *value)
{
    StartChild ();
    WriteString (value);
}

void JsonWriter::Value (string value)
{
    StartChild ();
    WriteString (value.c_str ());
}

void JsonWriter::Value (bool value)
{
    StartChild ();
    Write () << (value ? "true" : "false");
}
void JsonWriter::Key (const char *key)
{
    StartChild (true);
    WriteString (key);
    Write () << keyPaddingLeft << ":" << keyPaddingRight;
}

void JsonWriter::NullValue ()
{
    StartChild ();
    Write () << "null";
}
```

```checker
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/Code/json-writer.cpp
  error: Sorry, you didn't create file "json-writer.cpp" in /home/labex/Code!
  timeout: 3
```

## 3. Write Test File

Create a file `test.cpp` in `/home/labex/Code`. The code of this file as following:

```cpp
//
// test.cpp
//
#include <iostream>
#include <cmath>
#include "json-writer.h"
using namespace std;

int main()
{
auto writer = new JsonWriter;
writer->StartArray ();

  writer->StartShortObject ();
    writer->KeyValue ("name", "labex1");
    writer->KeyValue ("age", 3);
  writer->EndObject ();

  writer->StartObject ();
    writer->KeyValue ("skills", "c++");
    writer->KeyValue ("skills","python");
    writer->KeyValue ("skills","php");
    writer->KeyValue ("skills","java");
    writer->KeyValue ("url", "http://labex.com");

    writer->Key ("path");
    writer->StartArray ();
      writer->Value ("web");
      writer->Value ("algorithm");
      writer->Value ("linux");
    writer->EndArray ();

    writer->Key ("short-array");
    writer->StartShortArray ();
      writer->Value (1);
      writer->Value ((uint64_t)0xabcdef123456);
      writer->Value (M_PI);
    writer->EndContainer ();

  writer->EndObject (),
  writer->Value (false);
writer->EndArray ();
}
```

Write makefike `MakeFile` in `/home/labex/Code`.

```makefile
CXX = g++
CXXFLAGS = -g -Wall -std=c++11

test:json-writer.h json-writer.cpp test.cpp
    $(CXX) $(CXXFLAGS) json-writer.h json-writer.cpp test.cpp -o test
```

```sh
$ make
```


![image desc](https://labex.io/upload/X/G/F/QgGR5DOoCQr7.png)


Of course, you can write the json data into the file by redirecting：

```sh
./test > 1.txt
```

```checker
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/Code/test.cpp
  error: Sorry, you didn't create file "test.cpp" in /home/labex/Code!
  timeout: 3
```

## 4. Test Multiple Formats

Macro substitution is the technical feature of C/C++, which provide a great macro substitution function. Before the source codes enter the compiler, they need to cross a module called "preprocessor", which will expand the macros by the compiling arguments and actual codes. Only by being expanded can the codes get into the compiler officially, to make lexical analysis and syntax analysis. In this test example, for conciseness, implement the test function with macro function and nest another macro function to release memory. Create `json-writer-test.cpp` in `/home/labex/Code`.

```cpp
//
// json-writor-test.cpp
//

#include "json-writer.h"

#define BEGIN_TEST(name) { \
    JsonWriter *w = new JsonWriter; \
    w->SetInitialIndentDepth (2); \
    if (compress) { \
        w->ConfigureCompressedOutput (); \
    } \
    std::cout << #name << ":" << std::endl << std::endl;

#define END_TEST \
    delete w; \
    std::cout << std::endl << std::endl; \
}

int main (int argc, char **argv)
{
    bool compress;
    for (int i = 0; i < 2; compress = i == 0, i++) {

    BEGIN_TEST(null)
        w->NullValue ();
    END_TEST

    BEGIN_TEST(bool-false)
        w->Value (false);
    END_TEST

    BEGIN_TEST(bool-true)
        w->Value (true);
    END_TEST

    BEGIN_TEST(int)
        w->Value (30000);
    END_TEST

    BEGIN_TEST(double)
        w->Value (0.123456789);
    END_TEST

    BEGIN_TEST(empty-string)
        w->Value ("");
    END_TEST

    BEGIN_TEST(simple-string)
        w->Value ("Hello");
    END_TEST

    BEGIN_TEST(escaped-string)
        w->Value ("\"newline\ntab\t\"");
    END_TEST

    BEGIN_TEST(empty-object)
        w->StartObject ();
        w->EndObject ();
    END_TEST

    BEGIN_TEST(empty-array)
        w->StartArray ();
        w->EndArray ();
    END_TEST

    BEGIN_TEST(short-object)
        w->StartShortObject ();
        w->KeyValue ("name", "Aaron");
        w->EndObject ();
    END_TEST

    BEGIN_TEST(short-array)
        w->StartShortArray ();
        for (int i = 0; i < 10; i++) {
            w->Value (i);
        }
        w->EndArray ();
    END_TEST

    BEGIN_TEST(array-with-objects)
        w->StartArray ();
            w->StartShortObject ();
                w->KeyValue ("name", "Aaron");
                w->KeyValue ("age", 7);
            w->EndObject ();
            w->StartObject ();
                w->KeyValue ("animal", "cat");
                w->KeyValue ("life-expectancy", "forever");
                w->KeyValue ("url", "http://catoverflow.com");
                w->Key ("catch-phrases");
                w->StartArray ();
                    w->Value ("meow");
                    w->Value ("hiss");
                    w->Value ("purr");
                w->EndArray ();
            w->EndObject (),
            w->Value (false);
        w->EndArray ();
    END_TEST

    BEGIN_TEST(nested-objects)
        w->StartObject ();
            w->Key ("a");
            w->StartObject ();
                w->Key ("b");
                w->StartObject ();
                    w->Key ("c");
                    w->StartObject ();
                    w->EndObject ();
                w->EndObject ();
            w->EndObject ();
        w->EndObject ();
    END_TEST

    BEGIN_TEST(nested-arrays)
        w->StartArray ();
            w->StartArray ();
                w->StartArray ();
                    w->StartArray ();
                    w->EndArray ();
                w->EndArray ();
            w->EndArray ();
        w->EndArray ();
    END_TEST

    }

    return 0;
}
```

You may find this amazing: How can you write C++ like python? The use of macro is quite amazing indeed. Besides, the object of `jsonWriter` is created on a heap, so it can be directly invoked in `main` function, and release the resource after every invoking. As the heap is not a resource assigned automatically by system, so it needs to be deleted manually. 

Rewrite makefile：

```makefile
CXX = g++
CXXFLAGS = -Wall -g -std=c++11

json-writer-test: json-writer.h json-writer.cpp json-writer-test.cpp
    $(CXX) $(CXXFLAGS) json-writer.h json-writer.cpp json-writer-test.cpp -o json-writer-test
```


![image desc](https://labex.io/upload/W/F/O/6K3d5x0garaO.png)


## 5. Source Codes

You can get all the codes of this course by the command below: 

```sh
$ wget https://labexfile.oss-us-west-1-internal.aliyuncs.com/courses/90/json-writer.zip
```

## 6. Summary

In the experiment, we've learned how to generate json. It's not good as most libraries, not able to operate files, however basics are always important.

## 7. Challenges

There's a dungeon in LabEx company, a n*m lattice matrix. And every lattice has a treasure in it, and each treasure has a certain value. The entry of the dungeon is in the upper left corner, the exit is in the lower right corner.

You're taken to the entry of the dungeon, the guard demands that you can only walk right or down.
While walking through a lattice, if the treasure in the has bigger value than any treasure in you got, you can take(of course you can choose not to).

When you walk to the exit, if you just have k treasure, you can get them all. 
Please think, in the given situation, how many ways can you get the k treasures?

Input 3 integers in a row, seperate by whitespace：
`n m k (1<=n,m<=50, 1<=k<=12)`
Next are n rows of data, each row has m integers, Ci means the value of the treasure in the lattice.

Output a integer that means the number of the ways to get k treasures. The number might be very big, please output the result of it mod 1000000007.
Input Example

```
2 2 2
1 2
2 1
```
Output Example
```
2
```
Input Example
```
2 3 2
1 2 3
2 1 5
```
Output Example
```
14
```