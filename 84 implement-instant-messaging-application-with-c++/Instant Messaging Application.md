---
show: step
version: 1.0
enable_checker: true
---
# Instant Messaging Application

## 1.Introduction

#### 1.1 Content

In this lab, we will implement an instant messaging chatroom with the server-side and client-side by C++.

We will learn the basic knowledge of C++ network development in this project, meanwhile we will get to know basic Makefile writing and how C++ program compiles in Linux

#### 1.2 Knowledge


- The basic syntax of C++
- Basic makefile
- Object-oriented programming using C++ 
- Epoll network programming

#### 1.3 Experiment Environment

- g++
- Xfce terminal

## 2. Steps

#### 2.1 Analyze the Requirements

There're 2 programs in the chatroom app:

1. Server-side：It can accept new client-side to connect, and send the message from every client-side to every other client-side.
2. Client-side：It can connect the server, send message to the server and accept any message from the server.

It's the simplest need of a chatroom. We'll only implement group chat, you can implement the private conversation between two single client-sides later. To lower the difficulty and emphasize the key points, we'll make the codes as simple as possible and remove the complicated functions in the project, including thread pool, multithreaded programming, timeout retransmission, and confirming receiving package. So you can thoroughly learn the C/S model and the use of epoll.

#### 2.2 Abstracting and Detailing

According to the need mentioned above, analyze and design the required class. 

The required character is quite simple, and so is the function. So we only need to design class client-side and class server-side according to the function character.

We need to implement these functions in class server-side:

1. Content the server.
2. Enable users to input message and send it to the server.
3. Accept and display the message from server.
4. Exit the connection.

According the needs above, the implementation of server-side need 2 processes that support the functions below:

Function of child process：

1. Waiting for users to input message
2. Write message to the pipe and send it to the father process.

Function of father process：

1. Use epoll mechanism to accept message from server-side and display it to users, so users can see the message from other users.
2. Read the message from child process from pipe and send it to server-side.

The server-side should support：

1. Support multiple server-sides to connect, implement the basic functions of chatroom. 
2. Launch the service to build listener port to wait for users to connect.
3. se epoll mechanism to implement concurrence, make it more efficient.
4. When the server-side connects, send welcome message and save the connection record.
5. When server-side sends a message, broadcast it all the other client-sides.
6. When the server-side exits, remove the connection message.

We need to learn some basic knowledge of network programming to implement these two classes.

#### 2.3 C/S Model

Let's introduce the model first. The server-side and client-side use the classic C/S model and TCP connection. Here's the model:

![image desc](https://labex.io/upload/C/R/G/PWaUwWO1sXVd.jpg)





Explain:

Server-side：

1. socket() Build listener Socket
2. bind() Bind the server port
3. listen() Connect the listener server-side
4. accept() Receive the connection
5. recv/send Receive and send data
6. close()Close socket

Client-side：

1. socket() Build listener Socket
2. connect()Connect to server
3. recv/send Receive and send data
4. close() Close socket

#### 2.3.1 Conventional steps of TCP Server-side Messaging

1. Use socket() to build TCP socket. (socket)
2. Bind the socket to a local address and port. (bind)
3. Set the socket as listen mode to accept requests from server-side. (listen)
4. Wait for requests: When the requests come, accept connection request and return a new socket corresponding to this connection. (accept)
5. Use the socket returned from accept to chat with server-side（usew write()/send() or send()/recv() )
6. eturn and wait for another request frome client.
7. Close socket

Example code of server-side：

    //Server.cpp code（communication module）：
    //Server-side address ip address + port id
    struct sockaddr_in serverAddr;
    serverAddr.sin_family = PF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_HOST);
    
    //Build listening socket in server-side
    int listener = socket(PF_INET, SOCK_STREAM, 0);
    if(listener < 0) { perror("listener"); exit(-1);}
    printf("listen socket created \n");
     
    //Bind the server-side address with the listening socket
    if( bind(listener, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("bind error");
        exit(-1);
    }
    //Start listening
    int ret = listen(listener, 5);
    if(ret < 0) { perror("listen error"); exit(-1);}
    printf("Start to listen: %s\n", SERVER_HOST);

We will introduce the accept connection and communication after explaining epoll.

#### 2.3.2 Conventional Steps of TCP Client-side Messaging

1. Create socket.（socket）
2. Use connect() to build a connection to the server.（connect)
3. Communicate with server-side（usewrite()/send() orsend()/recv())
4. Use close() close the connection of client.

Example code of client-side：

    //Client.cpp code（communication module）：
    //The server-side address which the client connects to（ ip address + port id）
    struct sockaddr_in serverAddr;
    serverAddr.sin_family = PF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);
    
    // Create socket（socket）
    int sock = socket(PF_INET, SOCK_STREAM, 0);
    if(sock < 0) { perror("sock error"); exit(-1); }
    //Send connection request to server（connect）
    if(connect(sock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("connect error");
        exit(-1);
    }

We'll introduce in detail about how server-side implements the communication between pipes and server-side.

After it, we need to learn the following important connects.

#### 2.4 Basic Technical Introduction

#### 2.4.1 Blocking and nonblocking Socket

Generally, for a file or device that file descriptor assigned, there're two ways to work: blocking and nonblocking

1. Blocking means: While trying to read and write the file descriptor,if there's no data to read or it can't be read temporarily, the program will be in waiting mode until there's something to read or write. 
2. Nonblocking means： If there's no data to read or write, the function will return immdeiatly rather than waiting.

For example, James comes to chat with a girl, but she's not there. If James doesn't want to leave, all he can do is to wait at her door and rest. When the girl comes, she can wake him up (because he's in the way lol), that's blocking. If James leaves as soon as he doesn't find her here, and come back to check in every 10 minutes, still leaves when she's absent. This's nonblocking. He can do other things when he leaves.

The only different between blocking and nonblocking is: whether it returns immediately or not. This project uses a more efficient way: set socket as nonblocking. So we can fully use the resource of server.

Example code of nonblocking：

    //Set file descriptor as nonblocking（use fcntl function）
    fcntl(sockfd, F_SETFL, fcntl(sockfd, F_GETFD, 0)| O_NONBLOCK);

#### 2.4.2 Epoll

We've introduced blocking and nonblocking, now it's time for epoll mechanism. Eproll is a really important concept. It's required in the job interview of backend developer or system developer in IT companies. When online clients in server-side get more and more, system resource will be short-handed, and I/O efficiency will be lower and lower. This's the time to consider epoll. Epoll is a poll that Linux core improved to access loads of handlers. And it's an I/O function that only Linux has. Here are it's features.

1. Epoll is an enhanced version of multiplexing IO port select/poll in Linux. The ways to implement and use it are very different from select/poll. Epoll finish the work from a group of functions, not a single function.
2. The reason why epoll is efficient is that, epoll put the files descriptor that clients care about into an advent list inside the core, rather than loading file descriptor set or event set repeatly like select/poll. For example, when an event happens(like reading), epoll doesn't have to traverse the whole descriptor set which is being listened to. It only needs to traverse the descriptor set which is asynchronously awaked by core IO event and join the ready queue.
3. Epoll works in 2 ways，LT:level triggered and ET:edge-triggered. LT is the trigger that select/poll uses，it's not efficient enough. However, epoll works very efficiently in ET.（In this project, we use ET. ）

In layman's terms,  for example, there're many girls, some are beautiful, some are not. Now you want to chat with a beautiful one. LT means, you need to see all of the girls to find the beautiful one (ready event) ; ET means, your friend(core) can tell the id of N beautiful girls, so you can check on them directly. So ET is efficient. Besides, do you still remember the example about how James going to chat with a girl? By nonblocking, he needs to return to check in every 10 minutes (selcet) ; If he has a friend(core), his friend would stand at the door for him and call him when she returns. This's what epoll is about.

There're 3 functions of epoll:

Create an epoll handle：

    // int epoll_create(int size) Create an epoll handle, parameter size is used to tell the core how many is being listened. Size is the largest number of handlers that epoll supports.

Epoll event register function：

    /*
    What the function does： epoll event register function
    　 parameter epfd is the handler of epoll, the return value of epoll_create
    　 Parameter op means action, express it with 3 macroes:
    　　  EPOLL_CTL_ADD(Register the new fd to epfd)， 
    　EPOLL_CTL_MOD(Change the event listener of the registered fd)，
    　　  EPOLL_CTL_DEL(Delete fd from epfd)； 
    　　  The parameter fd is the identifier that needs to be listened；
    　 The parameter event tell the core about the events that need to be listened. Here's the structure of event :
    struct epoll_event {
      __uint32_t events; //Epoll events
      epoll_data_t data; //User data variable
    };
    Events are the set of macroes, we mainly use EPOLLIN in this project.(it means the corresponding file descriptor is readable, which means the reading event has happened). You can google the other types of macro.
    */
    int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)

Waiting for the event to happen：

    // Waiting for the event to happen, the function returns the number of events to be processed. (The number is actually the number of the ready events, which means the number of beautiful girls: N.)
    int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout)

Here's the steps when server-side uses epoll：

1. Invoke epoll_create function to create an event list in the Linux core.
2. Then, add file operator(lisen to the socket listener) to the event list.
3. In the main loop, invoke epoll_wait to wait to return the ready file descriptor set.
4. Process the ready event set respectively. There're two kinds of events in this project: new client connects and client sends a message.(There're many other events in epoll. In order to make this project concise, we won't introduce them here. )

Next we'll introduce how to add a socket into an event list:

    //Add file descriptor fd into the core event list that epollfd marks, and register EPOLLIN and EPOLLET event. The former is a data-readable event, the latter means the ET. In the end, set file descriptor as nonblocking.
    /**
      * @param epollfd: epoll handler
      * @param fd: file descriptor
      * @param enable_et : enable_et = true, 
         Use ET of epoll, else use LT.
    **/
    void addfd( int epollfd, int fd, bool enable_et )
    {
        struct epoll_event ev;
        ev.data.fd = fd;
        ev.events = EPOLLIN;
        if( enable_et )
            ev.events = EPOLLIN | EPOLLET;
        epoll_ctl(epollfd, EPOLL_CTL_ADD, fd, &ev);
        setnonblocking(fd);
        printf("fd added to epoll!\n\n");
    }

#### 2.5 Structure of the Code

According to the detailing demand, let's create the essential program files.

First, name the program as chatroom:

    # Create menu for code
    mkdir chatroom && cd chatroom
    
    # Create the demanding files
    touch Common.h Client.h Client.cpp ClientMain.cpp
    touch Server.h Server.cpp ServerMain.cpp
    touch Makefile

What every file is used for：

1. Common.h：Common headfile，includes all the macro definition and socket network programming headfile.
2. Client.h， Client.cpp：Implement class client-side.
3. Server.h，Server.cpp：Implement class server-side.
4. ClientMain.cpp ServerMain.cpp：Main functions of client-side and server-side.

We'll start to implement the class required.

```checker
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/chatroom/Common.h
  error: Sorry, you didn't create file "Common.h" in /home/labex/chatroom!
  timeout: 3
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/chatroom/Client.h
  error: Sorry, you didn't create file "Client.h" in /home/labex/chatroom!
  timeout: 3
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/chatroom/Server.h
  error: Sorry, you didn't create file "Server.h" in /home/labex/chatroom!
  timeout: 3
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/chatroom/ClientMain.cpp
  error: Sorry, you didn't create file "ClientMain.cpp" in /home/labex/chatroom!
  timeout: 3
```
#### 2.6 Common.h

In this project, we only need to define a single function to be invoked by the class member function. The function of it is what we've mentioned in the end of 2.4: Add fd, the file descriptor to the core event list that epoll marks. So we put the definition of the function in the headfile Common.h.

Except this function, we also need to put the common macro definition of server-side and client-side in Common.h, for example:

1. Server address
2. Server port number 
3. The cache scale of message
4. Welcome and exit message of the server by default

Please implement Common.h by yourself according to the description above. You can refer to the example code offered by the course, or ask questions in LabEx forum.

#### 2.7 Implement Server-side

According to 2.2, we need the port below:

1. Initialize: Init()
2. Close the service: Close()
3. Start the service: Start()
4. Broadcast the message to all the clients: SendBoradcastMessage()

In the main loop of server, it would check and access the ready event of EPOLL every time. And there're two types of ready event list: new connection and new message. Server would extract message from the list by order to process. If it's a new connection, accept it and invoke addfd(). If it's a new message, send broadcast message to all the client-sides of the server, thus making it like a chatroom.

In the code of broadcast message, invoke recv() first to read the message, and then check the length of it. If the length is 0, then it's a message disconnected by client-side. Next we invoke close() and remove this client-side from the client-side list; If the length isn't 0, then it's an effective message, wew need to invoke sprintf() to format the message and add some important message in it. Next, extract the fd of every client-side from client-side list loop, invoke send() to send message to every client-side.

The pseudocode of every function is shown below, please implement them by yourself according to the content of 2.3 and 2.4.

#### 2.7.1 Init()

    // Initialize server-side and launch listening
    void Server::Init() {
    
        // Step 1：create listening socket
        // use socket()
    
        // Step 2：bind the <address></address>
        // use bind()
    
        // Step 3：listening
        // use listen()
    
        // Step 4：create event list
        // epoll_create()
    
        // Step 5：add listener fd to epoll fd
        // addfd()
    }

#### 2.7.2 Close()

It's quite simple, just close all the open file descriptors.

#### 2.7.3 SendBroadcastMessage()

    // Broadcast message to all the client-sides
    int Server::SendBroadcastMessage(int clientfd) {
        // Step 1：Accept new message
        // recv()
    
        // Step 2：Judge whether client-side stops the connection
    
        // Step 3：Judge whether there're other client-sides in the chatroom
    
        // Step 4：Format the content of the message
        // sprintf()
    
        // Step 5：raverse the list of client-side  to sand message in order
        // send()
    }

#### 2.7.4 Start()

    // Launch server-side
    void Server::Start() {
        // Step 1：initialize server-side
        // Init()
    
        // Step 2：enter main loop
     
        // Step 3：get the ready events
        // epoll_wait()
    
        // Step 4：process all the ready events by loop
        // 4.1 If it's a new connection, accept it and add it to epoll fd
        // accept() addfd()
    
        // 4.2 If it's a new message, broadcast it to other client-sides.
        // SendBroadcastMessage
    }

From the previous basic introduction of knowledge, you can find the example code of the functions above. If you think it's too hard, refer to the full code which this project offers or ask a qunestion in LabEx forum.

After implementing Server.h and Server.cpp, we need to finish the main funcions in ServerMain.cpp. The main function need to create a Server object and invoke Start() port.

#### 2.8 Implement Client-side:

According to the analyses in 2.2, we need a port below:

1. Connect to server, Connect()
2. Exit connection, Close()
3. Launch server-side, Start()

The pseudocode of every function is shown below, please implement it by yourself by referring to the content of 2.2 and 2.4.

#### 2.8.1 Connect()

    //  Connect server
    void Server::Connect() {
    
        // Step 1：create ocket
        // use socket()
    
        // Step 2：connect server-side
        // connect()
    
        // Step 3：create pipe, fd[0] is used for father process to read，fd[1] is uesd for child process to write
        // use pipe()
    
        // Step 4：use epoll
        // epoll_create()
    
        // Step 5：Add sock and the pipe reader descriptor to the core event list.
        // addfd()
    }

#### 2.8.2 Close()

Close all the opened file descriptors.

Pay attention, judge if it's in father process and child process. The pipe file descriptor of them are different.

#### 2.8.3 Start()

    // Start clint-side
    void Client::Start() {
        // Step 1：Connect  to server
        // Connect()
    
        // Step 2：Create child process
        // fork()
    
        // Step 3：Enter the execution process of child process
        // The child process collects the message input by clients and write it in the pipe.
        // fgets() write(pipe_fd[1])
    
        // Step 4：Enter the execution process of father process
        // The father process reads the pipe data and epoll event
        // 4.1 Receive ready events
        // epoll_wait()
        // 4.2 Process ready events
        // Receive server-side message and display： recv()
        // Read pipe message and send it to server-side :read() send() 
    }

You can find example code of all the functions above from the previous basic knowledge introduction. If it's hard for you, please refer to the complete code offered by this project, or ask questions in LabEx forum.

Client.h and Client.cpp 

After implementing the file, we need to implement the main function in ClientMain.cpp. The main function only creates a Client object and invoke Start port.

#### 2.9 Compile and Run

Save you file as /home/labex/chatroom, edit Makefile file in the same catalogue：

    cd /home/labex/chatroom
    vim Makefile

The content of Makefile file is the integration of every compiling and links.

    CC = g++
    CFLAGS = -std=c++11
    
    all: ClientMain.cpp ServerMain.cpp Server.o Client.o
        $(CC) $(CFLAGS) ServerMain.cpp  Server.o -o chatroom_server
        $(CC) $(CFLAGS) ClientMain.cpp Client.o -o chatroom_client
    
    Server.o: Server.cpp Server.h Common.h
        $(CC) $(CFLAGS) -c Server.cpp
    
    Client.o: Client.cpp Client.h Common.h
        $(CC) $(CFLAGS) -c Client.cpp
    
    clean:
        rm -f *.o chatroom_server chatroom_client

Pay attention again, what's before (CC) (CFLAGS) ...is a tab, not a space.

After saving Makefile, we only need to execute make under the catalogue to generate executable files: chatroom_server and chatroom_client.

Now let's test it. First, start server-side:

    ./chatroom_server

And then open the new XFCE terminal, start client-side：

    ./chatroom_client

You can find there're are some logs input input in both server-side and client-side. Client-side can receive welcome message.

In order to add more clients, you can open a new XFCE terminal and start the new client-side. Every client has a different clientfd. When a message is sent, other clients can see the source of it.

You can send message in different server-sides and test:

![image desc](https://labex.io/upload/A/M/P/j06VFa3kVOoh.png)



If you run into question like this while testing, it means the server is closed abnormally, and the port isn't released. You can change the server-side port used in the Common.h to change the compilation to go on using.

![image desc](https://labex.io/upload/S/U/S/g6slXluFCmf1.png)



If you there's any question, you need to check the bug of the code according to the mistake message. You are welcomed to ask questions in LabEx forum.

```checker
- name: check if file exist
  script: |
    #!/bin/bash
    ls /home/labex/chatroom/Makfile
  error: Sorry, you didn't create file "Makefile" in /home/labex/chatroom!
  timeout: 3
```
## 3. References of the full code

We offer the full code and detailed comments to be referred to. Because the code is too long, we won't put it here. Please download the code.

    # Download code
    wget https://labexfile.oss-us-west-1-internal.aliyuncs.com/courses/84/chatroom.zip
    
    # Unzip code
    unzip chatroom.zip
    
    # Enter code folder
    cd chatroom

## 4. Extension

In this lab, we only implemented a simple instant messaging chatroom application based on CS structure. Based on what you learned in this course, you can make some extension on the the basis of this code.
  1. Private chat, decide which client-side to send by command.
  2. Input name instead of id number while connecting to the server.
  3. Multithreadingly increase concurrency
  4. Add functions like timeout retransmission and confirming receiving package to improve the stability.

## 5. Summary

After studying this course, we implement a chatroom application, learned basic syntax of c++ and some concepts of object-oriented programming, network programming development and how to use epoll.
