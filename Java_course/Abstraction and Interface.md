# Abstraction & Interface

## 1. Experiment Introduction

Abstraction and Interface is another two significant thoughts in Java.  Abstract class and interface are very different although there are some common points. Start this lab, and comprehend the concept.

### Learning Objective

- Abstraction

- Interface


## 2. Content

### 2.1 Abstraction

Abstraction is aimed at modeling and maintaining organizational structure, it doesn't provide many details, details are remained for the implementary classes. For example, when you consider the case of Animal, complex details such as what behaviors they can do, its details are hidden from the user. Therefore, for every specific animal, they themselves implement the details, we just need to invoke the method. In OOP, abstraction is a process of hiding the implementation details from the user, only the functionality will be provided to the user. In other words, the user will have the information on what the object does instead of how it does it. In Java, abstraction is achieved using Abstract classes and interfaces.

We use keyword abstract to declare an abstract class. Abstract classes may or may not contain abstract methods (methods without body only declaration). But, if a class has at least one abstract method, then the class must be declared abstract. If a class is declared abstract, it cannot be instantiated. To use an abstract class, you have to inherit it in another class, provide implementations to the abstract methods in it. If you inherit an abstract class, you have to provide implementations to all the abstract methods in it.

**Example**  

```
// abstract class
abstract class Animal{
	// abstract method
	public abstract void grow();
}

abstract class Bird extends Animal{
    /*
     * this class extends from Animal,
     * but don't implement Animal's abstract method grow(),
     * so this class is also declared as abstract,
     * abstract class cann't be initialized.
    */
    
    // this class has a concrete method
    public void sing(){
        System.out.println("I'm singing a song...");
    }
}
class Dog extends Animal{
	// In this class, we must implement the abstract method, or the subclass must stay abstract.
	public void grow(){
		System.out.println("I'm dog, I grow up.");
	}
}
public class abstractTest{
	public static void main(String[] args){
		Dog dog = new Dog();
		dog.grow();
	}
}
```

**Output:**

```
I'm dog, I grow up.
```

![image desc](https://labex.io/upload/Y/E/Q/jN0schmfkDpY.png)

### 2.2 Interface

Interface is a collection of abstract methods, it means all the methods in the interface are abstract. An interface does not contain any constructors. An interface cannot contain instance fields, only static and final fields can be in interface. An interface is not extended by a class, it is implemented by a class. An interface can extend multiple interfaces. A class can implement many interfaces at a time.

**Example**

```
// use keyword interface to create an interface.
interface myInterface1 {
    // Variables in interface are public, static and final by default.
	String NAME = "Interface";  

    // methods are  abstract and public by default.
	public void method1();     
}
interface myInterface2 {
    // we can explicitly define variable in interface as public and final, or just like that of myInterface1.
	public final String ID = "1001";

	public void method2();
}
// myInterface3 has method of myInterface2, it extends from myInterface2.
interface myInterface3 extends myInterface2{
	public void method3();
}
// class interfaceTest must implement all the three methods of upper interface.
public class interfaceTest implements myInterface1,myInterface3 {
	 /*
     * this class has three methods from three interfaces
     * also get the two interfaces's variables
     */
    // implement method1()
	public void method1(){
		System.out.println("implement method1.");
	}
     // implement method2()
	public void method2(){
     // implement method3()
	public void method3(){
	public static void main(String[] args){
        // test the methods
		interfaceTest test = new interfaceTest();
		test.method1();
		test.method2();
		test.method3();
        System.out.println("I have properties:" + interfaceTest.NAME +", " +interfaceTest.ID);
	}
}
```

**Output:**

```
implement method1.
implement method2.
implement method3.
I have properties:Interface, 1001
```

![image desc](https://labex.io/upload/E/C/N/HLQcQvL7iz56.png)

## 3. Summary

Abstract class and interface can decouple classes and give us more clear design ideas. Both of the two cann't be instanced directly. Abstract class only surport single inheritance while interface surport multiple inheritance and a class can implement many interfaces. Both of them provide some features of polymorphism which is topic of next lab.