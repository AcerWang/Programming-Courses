---
show: step
version: 1.0
enable_checker: true
---

# Implement Course Management System with C++

## 1. Introduction

In this lab, we'll implement a course management system by c++. Many features of C++ will be used in this project, and you can learn how to compile c++ in Linux and basic Makefile writing.

#### 1.1 Learning objectives

- Basic syntax of C++；
- Basic Makefile；
- Object-oriented programming using C++，class, virtual function, inherit,   overload；
- Standard C++ library；
- Some ways to use C++11, like `auto`.

#### 1.2 Experiment Environment

- g++
- Xfce terminal

## 2. Content

#### Analyze the Requirement

We can divide the requirement in this project into the 2 modules below:

- Input and process command
- Save and manage the courses

Exercise every participant in every module:

- Command management object
- Course object
- Course management object

The command management object manages the command. The course object stores the information of every course. The course management object maintains and manages the course list.

We need 3 classes: `class course`, `class course management`, `class command management`. If the information the command object contains is very complicated, you can design it as a class separately. In this project, command is only a number and a corresponding description message. In order to make the research easier, we only need to define the command in the `class command management`.

According to the needs, `class course` is a basic class. The child class are project course and assessment class. But we don't need the virtual function implementation of these two child classes. So this part will be the extension part.

### 2.1 Abstract and Detail

According to the analysis of needs, design the class in need:

1. Define class course `Course`, class course management `CourseManager` and class command management `CmdManager`.
2. The members of `class course` include
   - course ID（Created by default while creating a class object）
   - Course name
3. The member functions of `class Course` should at least include:
   - The constructor（Name of parameter course）
   - Copy courseco
   - Return and set the name of courses
   - Get the function of course ID
   - Print the information function（Consider overload `<<`）
4. The member of `class CourseManager` should at least include
   - Course list（Think about it: what kind of data should we use to store?）
5. The member functions of `class CourseManager` should at least include
   - The constructor（The parameter is course object vector）
   - Get the course number function
   - Add course function (The parameter is the name of the course)
   - Add course function (The parameter is the object of the course)
   - Delete the newest course function
   - Delete the course function (assign the ID or the course name)
   - Print the course list
   - Print the assigned course (assign the ID or the course name)
   - Print the course function with the longest name 
6. The memnber of `class CmdManager` shoul at least include:
   - Command list（Think about it: what kind of data should we use to store?）
   - Course management object（Use it in where needs the course management）
7. The mamber function of `class CmdManager` should at least include：
   - Initialize the function: Initialize the course and the command information
   - Print the help information
   - Command processing function
8. Pay attention while implementing
   - What functions can by defined as `const`?
   - Is there a class member that can be defined as `static` or `const`
   - What functions can be defined as friend functions?
   - What constructor can be defined as default constructors?

According how we plan to detail, we should create the necessary program file. Every class would create a head file and cpp file. Besides, for the extension of the future command objects, we create  a cmd.h first, to define all the command number we support.

First, name the program as `cmsys ` (The abbreviations of Course Manager System)

```sh
# Create code catalogue
mkdir cmsys
cd cmsys

# Created the required files
touch Course.h Course.cpp
touch CourseManager.h CourseManager.cpp
touch Cmd.h CmdManager.h CmdManager.cpp
touch main.cpp
touch Makefile
```

There are the all the required files in this project:

1. `Course.h` and `Course.cpp`： Define class course
2. `CourseManager.h` and `CourseManager.cpp`： Define class course management
3. `Cmd.h`，`CmdManager.h`，`CmdManager.cpp`：Define class command management 

`CourseManager` needs a Course container in it to store course list. `CmdManager` needs to store a `CourseManager` object in it to invoke the corresponding port to visit and process the course.

Next, let's implement the 3 classes.

### 2.2 Class course

 According the analysis above, class course should obtain two basic information: course ID and course name. So, add the following code in `Course.h` in `/home/labex/cmsys`:

```cpp
// Class course：Store and process the course information
class Course {
    // Course ID
    int id;

    // Course name
    string name;
};
```

In order to enable the chiled class to visit course ID and course name, let's define these as `protected`.
In order to generate different IDs, let's define an `int` type of static member variable. Plus one on it automatically while creating a new object.

```cpp
class Course {
    // Set satatic variable to generate the only ID value
    static int currentId;
};
```

According to the design of the port above, define the following ports separately. The functions of ports are corresponding to the design above.

```cpp
class Course {

    // Friend function：Read the input, create a new course.
    friend void read(istream &inputStream, Course &course);

public:
    // The constructor without a parameter
    Course();

    // The constructor of class course：Create course object by the course name
    Course(const string& cName): Course() { name = cName; };

    // The copy constructor of class course
    Course(const Course& course);

    // Print course message
    virtual void PrintInfo() const;

    // Return course name
    inline string GetName() const { return name; };

    // Set course name
    inline void SetName(const string& newName) { name = newName; };

    // Return course ID
    inline const int GetId() const { return id; };

    // The overload function of operator <<, use it while outputting course information by cout<<
    friend ostream& operator <<(ostream& out, const Course& course);
};
```

We can find two friend functions, the first can read the information to create course object from the standard input, the second can overload the output operator `<<` to print and output the course information. We won't be using the first one in this project, you can simply understand it by implementing. The overload of operator `<<` will be used many times while printing course information.

In the ports above, there's a virtual function named `virtual void PrintInfo() const`. The reason why we define it this way is that, the child class that project course and assessment course correspond to all have new members to display. So they will implement `PrintInfo` again after inheriting `Course`.

Let's add 2 new child classes in the `Course.h` head file. Add tag in project course and add limited time in assessment course. The former one is in the example code, please add the latter one by yourself:

```cpp
class ProjectCourse: public Course {
public:
    // Set tag
    inline void SetTag(const string& newTag) { tag = newTag; };

    // Return tag
    inline string GetTag() const { return tag; };

    // Print course information
    virtual void PrintInfo() const override;
private:
    string tag;
};
```

Pay attention: While changing `Course.h`, add the necessary head file and `using namespace std`;
After finishing the head file, implement every function above in Course.cpp. Part of the functions are implemented by `inline` in Course.h. We've put the complicated functions in the cpp file.

First, in order to make the ID unique, let's us static member and add the static member in the constructor:

```cpp
// Initialize the static member, set the first course ID as 1 by default.
int Course::currentId = 1;

// The constructor of class course
Course::Course(){
    // Assign the ID with the current value(C) of currentId , and increase currentId automatically.
    id = currentId++;

    // Set the course name as empty string by default
    name = "";
}
```

The operator of overloading. The implement of this function is inputting the course ID and course name by sertain form.

```cpp
// The overload function of operator <<, which is used while inputting course information by cout<<

ostream &operator<<(ostream &os, const Course& course)
{
    os << "Course: " << course.id << " : " << course.name;
    return os;
}
```

According to the description above, please combine the codes to implement class course, which means implementing Course.h and Course.cpp. Try to do it by yourself as possible. If you run into a problem, you can refer to the complete code offer by this course, or ask qunestions in LabEx forum.

After finishing the code, let's compile them as an object file:

```sh
g++ -std=c++11 -c Course.cpp
```

If it doesn't report any error, it can generate a Course.o file in the catalogue.

```checker
- name: Check if file is created  
  script: |
    #!/bin/bash
    ls -l /home/labex/cmsys/Course.h
  error: Oops! We found that you haven't created file "Course.h" in "/home/labex/cmsys/"!
- name: Check if content is created  
  script: |
    #!/bin/bash
    grep -i 'class' /home/labex/cmsys/Course.h | grep -i 'course'
  error: Oops! We found that you haven't created class "Course" in "Course.h".
```
### 2.3 Class course management

According to the analysis in 3.2, class course manager requires a course list. So let's add this in CourseManager.h:

```cpp
// Class course manager: maintain the course list and execute the course processing tasks.
class CourseManager {
private:

    // Store course list 
    vector<Course> courseList;
};
```

The reason why we use `vector` is that we need to search the course by ID and name, and delete the last course operation. The sequence container is the best choice, while associative containers like `map` or `set` are not.

According to the design of the port in 3.2, define the following ports separately. The function of ports corresponds to the design in 3.2:
```cpp
class CourseManager {
    
public:
    // Default constructor
    CourseManager() = default;

    // Constructor：Create CourseManager by course vector
    CourseManager(const vector<Course>& courseVect);

    // Get the length of course list
    inline int GetCourseNum() { return courseList.size(); }

    // Add new courses
    void AddCourse(const Course &course);
    void AddCourse(const string& courseName);

    // Delete course: delete the last course
    void RemoveLast();

    // Delete courses: Delete the course with assigned name
    void RemoveByName(const string &name);

    // Delete courses: Delete the course with assigned ID
    void RemoveById(int id);

    // Print course list information
    void PrintAllCourse();

    // Print course information by course name
    void PrintCourse(const string &name);

    // Print course information by course ID
    void PrintCourse(int id);

    // Print the course with the longest name
    void PrintLongNameCourse();
};
```

These're functions with functional features, maybe part of them are not used in the project requirement, but can be used to extent new operation order. Refer to comment for the meaning of every function. There's no virtual or overload without inheriting.

Please add the necessary head file and `using namespace std` while changing CourseManager.h;

After finishing the head file, implement every function above in CourseManager.cpp. Part of the functions are already implemented in CourseManager.h by `inline`, for example, getting the length of course list. We will put the complicated function in cpp file.

In the implementation of the function, what we should pay attention to is the traverse and adding/deleting of course vector:

```cpp
 for (auto curs = courseList.begin(); curs != courseList.end(); ++curs){
}
```

Add new course object

```cpp
courseList.push_back(course);
```

Whilde deleting the last course, judge whether it's empty. If it's empty, alert abnormality or simple print prompt message. If it's not empty, delete it.

```cpp
courseList.pop_back();
```

While deleting course assigned with ID or name, search the index of course in vector first, and use the erase function in vector to delete.

```cpp
 int index = FindCourse(id);
 if (index > 0)
     courseList.erase(courseList.begin()+index);
 else
     cout << "NOT FOUND" << endl;
```

The implementation of search function is based on the traverse mentioned above.

According to the description above, please combine the codes to implement class course, which means implementing `CourseManager.h` and `CourseManager.cpp`. Try to do it by yourself as possible. If you run into a problem, you can refer to the complete code offer by this course, or ask questions in LabEx forum.

After finishing the code, let's compile them as a object file:

```sh
g++ -std=c++11 -c CourseManager.cpp
```

If it doesn't report any error, it can generate a `CourseManager.o` file in the catalogue.

```checker
- name: Check if file is created  
  script: |
    #!/bin/bash
    ls -l /home/labex/cmsys/CourseManager.cpp
  error: Oops! We found that you haven't created file "CourseManager.cpp" in "/home/labex/cmsys/".
- name: Check if content is created  
  script: |
    #!/bin/bash
    grep -i 'class' /home/labex/cmsys/CourseManager.cpp| grep -i 'coursemanager'
  error: Oops! We found that you haven't created class "CourseManager" in "CourseManager.cpp".
```

### 2.4 Class command manager

According the analysis in 3.2, we need to support 6 kinds of commands. So, in `Cmd.h`, we define an `enum` type which contains the 6 kinds of command numbers.

```cpp
enum CourseCmd
{
    // Print command help information
    Cmd_PrintHelp = 0,
    // Print course information
    Cmd_PrintCourse = 1,
    // Print course number
    Cmd_PrintCourseNum = 2,
    // Print the longestr course name
    Cmd_PrintLongName = 3,
    // Delete the lase course
    Cmd_RemoveLastCourse = 4,
    // Exit
    Cmd_Exit = 5,
};
```

Class command manager needs to obtain course manager object and command list. In command list, in order to support the function of search command help message by ID, we give precedence to `map` to implement. So we add this in `CmdManager.h`:

```cpp
// Class command manager
class CmdManager {
private:

    // Class manager object
    CourseManager manager;

    // Use map to store command and help information
    map<CourseCmd, string> cmdMap;
};
```

According to the design of the port in 3.2, define the following ports separately. The function of ports corresponds to the design in 3.2:

```cpp
// Class commmand manager
class CmdManager {

public:
    // The constructor
    CmdManager() = default;

    // Initialize th function, initialize the supported command and course information
    void Init();

    // Print help information
    void PrintAllHelp() const;

    // Search information by command
    void PrintCmdHelp(const CourseCmd cmd) const;

    // Process command operation
    bool HandleCmd(const CourseCmd cmd);

    // Return course manager object
    CourseManager& GetCourseManager() { return manager; }
};
```

Pay attention: While changing `Course.h`, add the necessary head file and `using namespace std`.

After finishing the head file, implement every function mentioned above in `CmdManager.cpp`.

In all these functions, what you should pay attention to is `Init()`. It's used to initialize the class member in `CmdManager`.
```cpp
   // Initialize function
    void CmdManager::Init(){

   // Initialize course list
    manager.AddCourse("Linux");

    // Initialize command list
    cmdMap.insert(pair<CourseCmd, string>(Cmd_PrintHelp, "Help Info"));
}
```


The other function is `HandleCmd()`. It invoke the ports of `CourseManager` Objects separately by the command value to implement course operation:

```cpp
// Process the command operation. If it returns false, exit the program, else, return true.
bool CmdManager::HandleCmd(const CourseCmd cmd){
    // Search if the command supports:
    auto iter = cmdMap.find(cmd);

    // If the command doesn't support, print NOTFOUND and exit
    if (iter == cmdMap.end()) {
        cout << "NOT FOUND" << endl;
        return true;
    }

    // Choose different operations by the command value
    switch(cmd) {
        case Cmd_PrintHelp: PrintAllHelp(); break;
        case Cmd_PrintCourse: manager.PrintAllCourse(); break;
        case Cmd_PrintCourseNum: cout << manager.GetCourseNum() << endl; break;
        case Cmd_PrintLongName: manager.PrintLongNameCourse(); break;
        case Cmd_RemoveLastCourse: manager.RemoveLast(); break;
        // return false is used tp help the loop exit of the outter layer.
        case Cmd_Exit: return false;
        default: break;
    }

    return true;
}
```

In the implementation of the function, we should pay attention to the traverse and search of course `map`. The traverse use the code below:

```cpp
for (auto iter = cmdMap.begin(); iter != cmdMap.end(); iter++)
    cout << iter->first << ":" << iter->second << endl;
```

Search the command to be processed:

```cpp
auto iter = cmdMap.find(cmd);
```

According to the description above, please combine the codes to implement class course, which means implementing `CourseManager.h` and `CourseManager.cpp`. Try to do it by yourself as possible. If you run into a problem, you can refer to the complete code offer by this course, or ask questions in LabEx forum.

After finishing the code, let's compile them as a object file:

```sh
g++ -std=c++11 -c CmdManager.cpp
```

If it doesn't report any error, it can generate a `CmdManager.o` file in the catalogue.

```checker
- name: Check if file is created  
  script: |
    #!/bin/bash
    ls -l /home/labex/cmsys/CmdManager.cpp
  error: Oops! We found that you haven't created file "CmdManager.cpp" in "/home/labex/cmsys/".
- name: Check if content is created  
  script: |
    #!/bin/bash
    grep -i 'class' /home/labex/cmsys/CmdManager.cpp | grep -i 'cmdmanager'
  error: Oops! We found that you haven't created class "CmdManager" in "CmdManager.cpp".
```
### 2.5 Main Function

After finishing the 3 main classes, the main function is simple now. We only need to initialize and process the input of `cin`:
Part of the core code of the main function:

```cpp
// Create command manager object
CmdManager cmdManager;
cmdManager.Init();

// Print help information
cmdManager.PrintAllHelp();

cout << "New Command:";

// Enter the main loop and process input information
while (cin >> cmd) {
    if (cin.good()) {
        bool exitCode = cmdManager.HandleCmd((CourseCmd)cmd);
        if (!exitCode)
            return 0;
    }

    cout << "-------------------------" << endl;
    cout << "New Command:";

    // Clean input stream, avoid the characters in the stream from influencing the input later.
    cin.clear();
    cin.ignore();
}
```

Please implement the main function according to the code above.

After finishing the code, let's compile the object file first:

```sh
g++ -std=c++11 -c main.cpp
```

When all the object files are generated, we only need the last step to generate the executable file:

```sh
g++ -std=c++11 main.o CmdManager.o Course.o CourseManager.o -o cmsys
```

cmsys is the executable file we generated. We only have to run ./cmsys to enter the course command program, and input command by the prompt.

```checker
- name: Check if file is created  
  script: |
    #!/bin/bash
    ls -l /home/labex/cmsys/main.cpp
  error: Oops! We found that you haven't created file "main.cpp" in "/home/labex/cmsys/".
```
### 2.6 Compile and Run

In Linux, we often use `GNU make` to build and manage C/C++ projects. Though you can find the advantage of it from the file or the program, but when the program scale increases, `GNU make` will be very important. Because the dependency between source files will be quite complicated. When `GNU make` executes, it need a Makefile file, Makefile defines a series of rules to decide what files should be edited first, later, or again. Or even for some more complicated functional operations. Because Makefile is like a Shell script that can execute the command of the system in it.

Save the file you finished as `/home/labex/Code/labex_cs454/cmsys`，let's edit Makefile file in the same catalogue:

```sh
cd /home/labex/cmsys/
vim Makefile
```
The content in Makefile file is the integration of every compile and link step above.

```makefile
CC = g++
CFLAGS = -std=c++11

all: main.o CmdManager.o Course.o CourseManager.o
    $(CC) $(CFLAGS) main.o CmdManager.o Course.o CourseManager.o -o cmsys

main.o: main.cpp
    $(CC) $(CFLAGS) -c main.cpp

CmdManager.o: CmdManager.cpp CmdManager.h
    $(CC) $(CFLAGS) -c CmdManager.cpp

CourseManager.o: CourseManager.cpp CourseManager.h
    $(CC) $(CFLAGS) -c CourseManager.cpp

Course.o: Course.cpp Course.h
    $(CC) $(CFLAGS) -c Course.cpp

clean:
    rm *.o cmsys
```

Pay attention, what's before`$(CC) $(CFLAGS) ...`s a tab, not a blank.
Let's explain:

- `all` or `xxx.o` are the objects we should compile. While executing `make`, we'll execute the operation in every object by order. Of course there's dependency between objects, for example, `all` relies on other objects.
- `$(CC) $(CFLAGS) -c Course.cpp `are the executed compile or link command. Here we compile the course.cpp file to generate object file.
- `clean` is the deleted compiling object file and executable file while executing `make clean`.

After saving Makefile, we only need to input and execute `make` in the catalogue to generate executable file `cmsys`, run `./cmsys` and then enter the execution process of our program. If there's any question, you need to check the bug in your code by the reported errors.

```checker
- name: Check if file is created  
  script: |
    #!/bin/bash
    ls -l /home/labex/cmsys/Makefile
  error: Oops! We found that you haven't created file "Makefile" in "/home/labex/cmsys/".
```
### 2.7 Execute the Program

Here's the screenshot of the executing program:

![image desc](https://labex.io/upload/S/C/W/sL6RzbDOJtec.png)


## 3. Reference of the Complete Code

We offer the complete code and detaild comment of this project for your reference. As there's too many codes, we won't put them here. Please download to check it out.

```sh
# Downlod the code of course management program
wget https://labexfile.oss-us-west-1-internal.aliyuncs.com/courses/92/cmsys.zip

# Unzip the code
unzip cmsys.zip

# Enter the code fodler to check out
cd cmsys
```

## 4. Extension

In this lab, we only implemented a simple course management program. Based on what we learned in this course, you can implement the extension based in the code:
1. Course persistence: Save the course information in the file, and read it when the program starts.

2. Support different types of course management: use the implemented project course and assessment course in the code.

3. Add when the course executes: Input new course by the input of users

4. Command extension: Add courses research, add the command of deleting assigned courses.

## 5. Summary

By learning this course, we've implemented course management program, learned basic C++ syntax, some concepts of object-oriented, standard library, how to use auto and the most basic Makefile writing.

Tip: You're welcomed to ask any question in LabEx forum, we will answer your question in time.
