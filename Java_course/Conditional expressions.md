# Conditional Expressions
## 1. Experiment Introduction
In the last lab, we learned basic datatypes of Java and operators. In this section, we'll start to learn  to write procedure-oriented program. The main idea is using paradigm of controlling structure: conditional expressions.
### Learning Objective
- Conditional expressions
  - if-else
  - switch-case

## 2. Content

### 2.1 Conditional Expressions
To write useful programs, we almost always need to check conditions and change the behavior of the program accordingly. Conditional statements give us this ability.
#### 2.1.1 if-else conditional expression
The simplest form is the if-else statement:

**Example**

    public class ifelseTest{
      public static void main(String[] args){
        int x = 1;
        if (x > 0) {
        	System.out.println("x is positive");
    	}
    	else{
        	System.out.println("x is negative");
    	}
      }
    }
**Output:**

    x is positive
![image desc](https://labex.io/upload/U/J/E/EFNw06WGP8Vb.png)

The expression in parentheses is called the condition. If it is true, then the statements in brackets get executed. If the condition is not true, nothing happens.

The condition can contain any of the comparison operators, sometimes called relational operators:

**Example**

    if (x == y){ }               // x equals y
    if (x != y){ }               // x is not equal to y
    if (x > y) { }               // x is greater than y
    if (x < y) { }               // x is less than y
    if (x >= y){ }               // x is greater than or equal to y
    if (x <= y){ }               // x is less than or equal to y
Although these operations are probably familiar to you, the syntax Java uses is a little different from mathematical symbols like =, ≠ and ≤. A common error is to use a single = instead of a double ==. Remember that = is the assignment operator, and == is a comparison operator. Also, there is no such thing as =< or =>.

The two sides of a condition operator have to be the same type. You can only compare ints to ints and doubles to doubles. The operators == and != work with Strings, but they don’t do what you expect. And the other relational operators don’t do anything at all. 

An example: if the remainder when x is divided by 2 is zero, then we know that x is even, and this code prints a message to that effect. If the condition is false, the second print statement is executed. Since the condition must be true or false, exactly one of the alternatives will be executed. As an aside, if you think you might want to check the parity (evenness or oddness) of numbers often, you might want to “wrap” this code up in a method, as follows:

**Example**

    public class conditionTest
    {
        public static void printParity(int x) {
    	    if (x%2 == 0) {
    	      System.out.println(x + " is even");
    	    } else {
    	      System.out.println(x + " is odd");
    	    }
        }
    	public static void main(String[] args){
    		printParity(17);
    		printParity(18);
    	}
    }
​**Output:**   
    17 is odd
    18 is even

![image desc](https://labex.io/upload/K/A/H/r4UU4x6tfjNB.png)

Now you have a method named printParity that will print an appropriate message for any integer you care to provide. In main you would invoke this method. Always remember that when you invoke a method, you do not have to declare the types of the arguments you provide. Java can figure out what type they are. You should resist the temptation to write things like: printParity(int a) , In addition, you can also nest one conditional within another.

**Example**

    public class nestedConditionTest{
      public static void main(String[] args){
      	int x = 0;  // you can try x = 1, x = -1
        if (x == 0) {
        	System.out.println("x is zero");
    	} 
    	else {
       		if (x > 0) {
            	System.out.println("x is positive");
        	}
        	else {
            	System.out.println("x is negative");
        	}
      	}
      }
    }
**Output:**
    x is zero
![image desc](https://labex.io/upload/Q/K/X/JiqKn7Cabb15.png)

There is now an outer conditional that contains two branches. The first branch contains a simple print statement, but the second branch contains another conditional statement, which has two branches of its own. Those two branches are both print statements, but they could have been conditional statements as well.

Indentation helps make the structure apparent, but nevertheless, nested conditionals get difficult to read very quickly. Avoid them when you can. On the other hand, this kind of nested structure is common, and we will see it again, so you better get used to it.
#### 2.1.2 switch-case conditional expression
Switch-case statement is another conditional expression. The syntax of switch-case statement is like this: 

**Example**

    //value type can be byte、short、int、char、String, but long type is not correct.
    switch (variable or an value expression) 
    {
    	 //case value must be a constant value
         case value1:
         // code
         ;
         case value2:
         // code
         ;
         default:
         // code
         ;
    }

**Example**

    public class switchTest
    {
        public static void main(String[] args){
            // you can change i = 2, then try again
    		int i = 2;
    	    switch(i) 
    	    { 
    		    case 1: 
    		    	System.out.println(1); 
    				
    		    	break;    				
    		    case 2: 
    			    System.out.println(2); 
    			    // if no break expression, sometimes you'll get a confused answer.
    			    // you can try deleting the break expression and see what would happen.
    			    break;
    			// if none above matches, execute the default statements
    		    default:
    			    System.out.println("default"); 
    			    break; 
    	    }
        }
    }

​**Output:**   
    2
![image desc](https://labex.io/upload/R/D/B/fUTgiWaLaH18.png)

## 3. Summary

In this lab, you learned conditional expressions, two style of condition. They are very useful for programming. in next lab, you'll learn another controll structure: the recursion and loop.