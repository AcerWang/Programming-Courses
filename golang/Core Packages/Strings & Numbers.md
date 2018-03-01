# Strings & Numbers

## 1. Introduction

Strings and numbers are the most commonly used data types in our daily work. Not all these data is in form of what you want, in order to use them, you must convert them into the form fit for your program. Go provides useful built-in packages to help you do these operation. Start to learn how to use them.

### Learning Objective

- string functions
- string formatting
- random numbers
- number parsing

## 2. Content

### 2.1 String Functions

The standard library's `strings` package provides many useful string-related functions. Here are some examples to give you a sense of the package. Here's a sample of the functions available in `strings`. Since these are functions from the package, not methods on the string object itself, we need pass the string as the first argument to the function. You can find more functions in the `strings` package docs.

```
package main

// Import `strings` package, `s` is alias of `strings`
import s "strings"
import "fmt"

// use `p` as alias of the standard fmt.Println
var p = fmt.Println

func main() {
	
	// `Contanis` will return if `es` is in `test` as a substring.
	p("Contains:  ", s.Contains("test", "es"))
	
	// Count the how many times `t` appears in `test`.
    p("Count:     ", s.Count("test", "t"))
    
    // Return if `test` starts with `te`.
    p("HasPrefix: ", s.HasPrefix("test", "te"))
    
    // Return if `test` ends with `st`.
    p("HasSuffix: ", s.HasSuffix("test", "st"))
    
    // Get index of `e` in `test`.
    p("Index:     ", s.Index("test", "e"))
    
    // Use `-` to join items of a string slice.
    p("Join:      ", s.Join([]string{"a", "b"}, "-"))
    
    // Repeat 5 times of string `a`.
    p("Repeat:    ", s.Repeat("a", 5))
    
    // Replace 'o' with '0'.
    // -1 indicates replace all
    // 1 indicate replace once
    p("Replace:   ", s.Replace("foo", "o", "0", -1))
    p("Replace:   ", s.Replace("foo", "o", "0", 1))
    
    // Split a string with specific substring `-`, return a list.
    p("Split:     ", s.Split("a-b-c-d-e", "-"))
    
    // Convert all chars in a string into lowercase.
    p("ToLower:   ", s.ToLower("TEST"))
    
    // Convert all chars in a string into uppercase.
    p("ToUpper:   ", s.ToUpper("test"))
    p()
    
    // Return the length of a string.
    p("Len: ", len("hello"))
    
    // Return the byte(an int number) of char at specific index in a string.
    p("Char:", "hello"[1])
}
```

Note that `len` and indexing above work at the byte level. Go uses UTF-8 encoded strings, so this is often useful. If you're working with potentially multi-byte characters you'll want to use encoding-aware operations. See strings, bytes, runes and characters in Go for more information.

**Output:**

```
$ go run string-functions.go
Contains:   true
Count:      2
HasPrefix:  true
HasSuffix:  true
Index:      1
Join:       a-b
Repeat:     aaaaa
Replace:    f00
Replace:    f0o
Split:      [a b c d e]
ToLower:    test
ToUpper:    TEST

Len:  5
Char: 101
```

### 2.2 String Formatting

Go offers excellent support for string formatting in the `printf` tradition. Here are some examples of common string formatting tasks.

```
package main

import "fmt"
import "os"

type point struct {
    x, y int
}

func main() {
	
	// This prints an instance of our point struct.
	p := point{1, 2}
    fmt.Printf("%v\n", p)
    
    // If the value is a struct,
    // the %+v variant will include the struct's field names.
    fmt.Printf("%+v\n", p)
    
    // The %#v variant prints a Go syntax representation of the value.
    fmt.Printf("%#v\n", p)
    
    // Print the type of a value.
    fmt.Printf("%T\n", p)
    
    // Formatting booleans is straight-forward.
    fmt.Printf("%t\n", true)
    
    // Use this for standard, base-10 formatting.
    fmt.Printf("%d\n", 123)
    
    // This prints a binary representation.
    fmt.Printf("%b\n", 14)
   
    // This prints the character corresponding to the given integer.
    fmt.Printf("%c\n", 33)
    
    // This prints the hex encoding corresponding to the given integer.
    fmt.Printf("%x\n", 456)
    
    // Print a basic decimal formatting.
    fmt.Printf("%f\n", 78.9)

	// format the float in scientific notation.
    fmt.Printf("%e\n", 123400000.0)
    fmt.Printf("%E\n", 123400000.0)
    
    // Print a basic string.
    fmt.Printf("%s\n", "\"string\"")
    
    // Print the double-quote strings as in Go source
    fmt.Printf("%q\n", "\"string\"")
    
    // This renders the string in base-16.
    fmt.Printf("%x\n", "hex this")
    
    // Print a representation of a pointer.
    fmt.Printf("%p\n", &p)
    
    // When formatting numbers 
    // you will often want to control the width and precision of the results.
    // To specify the width of an integer, use a number after the % in the verb.
    // By default the result will be right-justified and padded with spaces.
    fmt.Printf("|%6d|%6d|\n", 12, 345)
    
    // The results will contain two decimals for each float.
    fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45)
    
    // The result is left-justified.
    fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45)
    
    // For basic string right-justified width.
    fmt.Printf("|%6s|%6s|\n", "foo", "b")
    
    // For basic string left-justified width.
    fmt.Printf("|%-6s|%-6s|\n", "foo", "b")
    
    // This formats and returns a string without printing it anywhere.
    s := fmt.Sprintf("a %s", "string")
    // You should print it manually.
    fmt.Println(s)
    
    // You can format+print to io.Writers other than os.Stdout using Fprintf.
    fmt.Fprintf(os.Stderr, "an %s\n", "error")
}
```

**Output:**

```
$ go run string-formatting.go
{1 2}
{x:1 y:2}
main.point{x:1, y:2}
main.point
true
123
1110
!
1c8
78.900000
1.234000e+08
1.234000E+08
"string"
"\"string\""
6865782074686973
0x42135100
|    12|   345|
|  1.20|  3.45|
|1.20  |3.45  |
|   foo|     b|
|foo   |b     |
a string
an error
```

### 2.3 Random Numbers

Go's `math/rand` package provides pseudorandom number generation. See the `math/rand` package docs for references on other random quantities that Go can provide.

```
package main

import "time"
import "fmt"
import "math/rand"

func main() {
	
	// Generate a random int number between [0,100)
	fmt.Print(rand.Intn(100), ",")
    fmt.Print(rand.Intn(100))
    fmt.Println()
    
    // Generate a random float64 number between [0.0,1.0]
    fmt.Println(rand.Float64())
    
    fmt.Print((rand.Float64()*5)+5, ",")
    fmt.Print((rand.Float64() * 5) + 5)
    fmt.Println()
    
    // The default number generator is deterministic,
    // so it'll produce the same sequence of numbers each time by default.
    // To produce varying sequences, give it a seed that changes.
    // Note that this is not safe to use for random numbers you intend to be secret,
    // use crypto/rand for those.
    s1 := rand.NewSource(time.Now().UnixNano())
    r1 := rand.New(s1)
    
    // each time you execute the program, the output is different
    fmt.Print(r1.Intn(100), ",")
    fmt.Print(r1.Intn(100))
    fmt.Println()
    
    // Seed a source for random generator
    s2 := rand.NewSource(42)
    r2 := rand.New(s2)
    fmt.Print(r2.Intn(100), ",")
    fmt.Print(r2.Intn(100))
    fmt.Println()
    
    // If you seed a source with the same number,
    // it produces the same sequence of random numbers.
    s3 := rand.NewSource(42)
    r3 := rand.New(s3)
    fmt.Print(r3.Intn(100), ",")
    fmt.Print(r3.Intn(100))
}
```

**Output:**

```
$ go run random-numbers.go
81,87
0.6645600532184904
7.123187485356329,8.434115364335547
0,28
5,87
5,87
```

### 2.4 Number Parsing

Parsing numbers from strings is a basic but common task in many programs. The built-in package `strconv` provides the number parsing. Here's how to do it in Go.

```
package main

// Import `strconv` package
import "strconv"
import "fmt"

func main() {

	// With ParseFloat, this 64 tells how many bits of precision to parse.
	f, _ := strconv.ParseFloat("1.234", 64)
    fmt.Println(f)
    
    // the 0 means infer the base from the string.
    // 64 requires that the result fit in 64 bits.
    i, _ := strconv.ParseInt("123", 0, 64)
    fmt.Println(i)
    
    // The method will recognize hex-formatted numbers.
    d, _ := strconv.ParseInt("0x1c8", 0, 64)
    fmt.Println(d)
    
    // Result is an uint64 number.
    u, _ := strconv.ParseUint("789", 0, 64)
    fmt.Println(u)
    
    // Atoi is a convenience function for basic base-10 int parsing.
    k, _ := strconv.Atoi("135")
    fmt.Println(k)
    
    // This will return an error on bad input.
    _, e := strconv.Atoi("wat")
    fmt.Println(e)
}
```

**Output:**

```
$ go run number-parsing.go 
1.234
123
456
789
135
strconv.ParseInt: parsing "wat": invalid syntax
```

## 3. Summary

These functions metioned above are helpful in your programming, you should use them fluently. The built-in packages contains two many functions, we can not cover all of them. If you are unclear about  a method, refer to the source code of the standard library.