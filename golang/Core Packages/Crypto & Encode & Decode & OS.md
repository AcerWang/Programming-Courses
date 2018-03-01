# Crypto & Encode & OS

## 1. Introduction

This part is about security and os. Some messages, we do not want to show them to users in original form. You can use sha1, it's irreversible operation. The base64 is mainly used to encode and decode a string. The `os` package provides methods of comand-line arguments processing and environment variables acquiring.

### Learning Objective

- sha1
- base64
- command line with arguments and flags
- environment variables
- exit

## 2. Content

### 2.1 SHA1

*SHA1 hashes* are frequently used to compute short identities for binary or text blobs. For example, the git revision control system uses SHA1s extensively to identify versioned files and directories. Go implements several hash functions in various `crypto/*` packages. Here’s how to compute SHA1 hashes in Go. 

```
package main

import "crypto/sha1"
import "fmt"

func main() {
    
    s := "sha1 this string"
    
    // The pattern for generating a hash is sha1.New().
    h := sha1.New()
    
    // Write expects bytes.
    h.Write([]byte(s))
    
    // This gets the finalized hash result as a byte slice. 
    // The argument to Sum can be used to append to an existing byte slice.
    bs := h.Sum(nil)
    
    fmt.Println(s)
    fmt.Printf("%x\n", bs)
}
```

**Output:**

```
$ go run sha1-hashes.go
sha1 this string
cf23df2207d99a74fbe169e3eba035e633b65d94
```

Running the program computes the hash and prints it in a human-readable hex format. You can compute other hashes using a similar pattern to the one shown above. For example, to compute MD5 hashes import `crypto/md5` and use `md5.New()`. Note that if you need cryptographically secure hashes, you should carefully research hash strength!

### 2.2 Base64

Go provides built-in support for base64 encoding/decoding.

```
package main

import b64 "encoding/base64"
import "fmt"

func main() {

	// Here’s the string we’ll encode/decode.
	data := "abc123!?$*&()'-=@~"
	
	// Go supports both standard and URL-compatible base64.
    // Here’s how to encode using the standard encoder.
    // The encoder requires a []byte so we cast our string to that type.
	sEnc := b64.StdEncoding.EncodeToString([]byte(data))
    fmt.Println(sEnc)
    
    // Decoding may return an error,
    // which you can check if you don’t already know the input to be well-formed.
    sDec, _ := b64.StdEncoding.DecodeString(sEnc)
    fmt.Println(string(sDec))
    fmt.Println()
    
    // This encodes/decodes using a URL-compatible base64 format.
    // The result is slightly different from the URL base64 encode.
    uEnc := b64.URLEncoding.EncodeToString([]byte(data))
    fmt.Println(uEnc)
    uDec, _ := b64.URLEncoding.DecodeString(uEnc)
    fmt.Println(string(uDec))
}
```

**Output:**

```
$ go run base64-encoding.go
YWJjMTIzIT8kKiYoKSctPUB+
abc123!?$*&()'-=@~

YWJjMTIzIT8kKiYoKSctPUB-
abc123!?$*&()'-=@~
```

### 2.3 Command-Line

#### 2.3.1 Command-line arguments

*Command-line arguments* are a common way to parameterize execution of programs. For example, `go run hello.go` uses `run` and `hello.go` arguments to the `go`program. `os.Args` provides access to raw command-line arguments. Note that the first value in this slice is the path to the program, and `os.Args[1:]` holds the arguments to the program.

```
package main

import "os"
import "fmt"

func main() {

	argsWithProg := os.Args
    argsWithoutProg := os.Args[1:]
    
    // You can get individual args with normal indexing.
    arg := os.Args[3]
    
    // 
    fmt.Println(argsWithProg)
    fmt.Println(argsWithoutProg)
    fmt.Println(arg)
}
```

To experiment with command-line arguments it’s best to build a binary with `go build` first.

**Output:**

```
$ go build command-line-arguments.go
$ ./command-line-arguments a b c d
[./command-line-arguments a b c d]       
[a b c d]
c
```

Next we’ll look at more advanced command-line processing with flags.

#### 2.3.2 Command-line flags

*Command-line flags* are a common way to specify options for command-line programs. For example, in `wc -l` the `-l`is a command-line flag. Go provides a `flag` package supporting basic command-line flag parsing. We’ll use this package to implement our example command-line program.

```
package main

import "flag"
import "fmt"

func main() {

	// Basic flag declarations are available for string, integer, and boolean options.
    // Here we declare a string flag word with a default value "foo" and a short description. 		// This flag.String function returns a string pointer.
	wordPtr := flag.String("word", "foo", "a string")
	
	// This declares numb and fork flags, using a similar approach to the word flag.
	numbPtr := flag.Int("numb", 42, "an int")
    boolPtr := flag.Bool("fork", false, "a bool")
    
    // It’s also possible to declare an option 
    // that uses an existing var declared elsewhere in the program.
    // Note that we need to pass in a pointer to the flag declaration function.
    var svar string
    flag.StringVar(&svar, "svar", "bar", "a string var")
    
    // Once all flags are declared,
    // call flag.Parse() to execute the command-line parsing.
    flag.Parse()
    
    fmt.Println("word:", *wordPtr)
    fmt.Println("numb:", *numbPtr)
    fmt.Println("fork:", *boolPtr)
    fmt.Println("svar:", svar)
    fmt.Println("tail:", flag.Args())
}
```

**Outout:**

```
$ go build command-line-flags.go

$ ./command-line-flags -word=opt -numb=7 -fork -svar=flag
word: opt
numb: 7
fork: true
svar: flag
tail: []

$ ./command-line-flags -word=opt
word: opt
numb: 42
fork: false
svar: bar
tail: []

$ ./command-line-flags -word=opt a1 a2 a3
word: opt
...
tail: [a1 a2 a3]

$ ./command-line-flags -word=opt a1 a2 a3 -numb=7
word: opt
numb: 42
fork: false
svar: bar
tail: [a1 a2 a3 -numb=7]

$ ./command-line-flags -h
Usage of ./command-line-flags:
  -fork=false: a bool
  -numb=42: an int
  -svar="bar": a string var
  -word="foo": a string

$ ./command-line-flags -wat
flag provided but not defined: -wat
Usage of ./command-line-flags:
...
```

Use `-h` or `--help` flags to get automatically generated help text for the command-line program. If you provide a flag that wasn’t specified to the `flag`package, the program will print an error message and show the help text again.

### 2.4 Environment Variables

Environment variables are a universal mechanism for conveying configuration information to Unix programs. Let’s look at how to set, get, and list environment variables. 

```
package main
	
import "os"
import "strings"
import "fmt"

func main() {

	// To set a key/value pair, use os.Setenv.
	// To get a value for a key, use os.Getenv.
	// This will return an empty string if the key isn’t present in the environment.
	os.Setenv("FOO", "1")
    fmt.Println("FOO:", os.Getenv("FOO"))
    fmt.Println("BAR:", os.Getenv("BAR"))
    
    // Use os.Environ to list all key/value pairs in the environment.
    // This returns a slice of strings in the form KEY=value.
    // Use strings.Split them to get the key and value.
    fmt.Println()
    for _, e := range os.Environ() {
        pair := strings.Split(e, "=")
        fmt.Println(pair[0])
    }
}
```

**Output:**

```
$ go run environment-variables.go
FOO: 1
BAR:

TERM_PROGRAM
PATH
SHELL
...

$ BAR=2 go run environment-variables.go
FOO: 1
BAR: 2
...
```

### 2.5 Exit

Use `os.Exit` to immediately exit with a given status. Note that unlike e.g. C, Go does not use an integer return value from `main` to indicate exit status. If you’d like to exit with a non-zero status you should use `os.Exit`.

```
package main

import "fmt"
import "os"

func main() {

	// defer will not take effect when using os.Exit,
    // so this fmt.Println will never be called.
	defer fmt.Println("!")
	
	// Exit with status 3.
	os.Exit(3)
}
```

If you run `exit.go` using `go run`, the exit will be picked up by `go` and printed. By building and executing a binary you can see the status in the terminal.

**Output:**

```
$ go run exit.go
exit status 3

$ go build exit.go
$ ./exit
$ echo $?
3
```

## 3. Summary

Now, you know how to set command-line arguments and get environment variables. Encryption is based on mathematical theories, we just use  standard library to achieve some simple tasks without knowing the detail.