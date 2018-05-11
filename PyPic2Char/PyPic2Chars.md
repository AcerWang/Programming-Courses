

# Transform a Picture into Character Drawing - Python

## 1. Introduction

In this lab, we will use Python - only 50 lines of code - to complete the transformation of a picture to character drawing. You should be quite familiar with Linux command operation, basics of Python, as well as how to use pillow and argparse library.


### Learning Objevtive

1. Linux command operation
2. Python fundamental concepts 
3. pillow library
4. argparse library

### Project Display

**Project Structure**

![image desc](https://labex.io/upload/S/H/H/jj2asYEuX8rz.png)

**Project Display**

![](https://labex.io/upload/C/T/M/XADA7ThDM0cn.png)

##2. Implementation Steps

###2.1 Download the Resources

You can use these command to download the resources and unpack them.

```bash
wget https://labexfile.oss-us-west-1-internal.aliyuncs.com/courses/51/PyCharDrawing.zip
unzip PyCharDrawing.zip -d PyCharDrawing
```

After downloading the resources, in the folder `PyCharDrawing`, there are only some pictures. You should create a python source file here by yourself.

![](1.png)

###2.2 Related Concept - Gray value

Character painting is a combination of a series of characters. We can think of characters as relatively large pixels. A character can represent a color (for now, we'll understand it this way). The more types of characters, the more colors that can be represented. The picture will be more layered.

So, if we want to transform a color picture, how would we achieve that with so many colors? Here, we'll introduce a new term called *Gray Value*.

> Gray value: refers to the color depth of the black and white image midpoint; the range is generally from 0 to 255. White is 255, and black is 0, so the black and white picture is also called gray image

We can use the gray value formula to map a pixel's RGB value to a gray value:

```python
gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
```

With this done, it is much simpler. We can create a non-repeating list of characters, symbols with a small gray (dark) starting with the list, and symbols with a large (bright) gray value using the end of the list.

###2.3 Install Python Library - pillow

`pillow` is a Python image processing library, an important tool used in this tutorial. Use this command to install the `pillow` (PIL) library:

```sh
$ sudo pip3 install pillow -i https://mirrors.cloud.aliyuncs.com/pypi/simple --trusted-host mirrors.cloud.aliyuncs.com
```

![](https://labex.io/upload/Y/J/T/NUdDdOFek2Ok.png)

###2.4 Write the Python Code

Edit ascii.py file:
```sh
$ cd PyCharDrawing
$ gedit ascii.py
```

**(1)** Import the necessary libraries. `argparse` library is used to manage the input of command line parameters.

```python
from PIL import Image
import argparse
```

**(2)** The following is the character set used by our character paintings. There are 70 characters in total. The type and number of characters can be debugged by themselves based on the effect of the character drawing.

```python
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
```

**(3)** The following is the function of RGB value to character:

```python
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]
```

Full sample code:

```python
from PIL import Image
import argparse

#Command line input parameter processing
parser = argparse.ArgumentParser()

parser.add_argument('file')     #input file
parser.add_argument('-o', '--output')   #output file
parser.add_argument('--width', type = int, default = 80) #output the width of drawing
parser.add_argument('--height', type = int, default = 80) #output the height of drawing

#obtain parameter
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# Map 256 gradations to 70 characters
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)
    
    #output drawing to file
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)
```

**(4)** Enter the following command to run the script, and see the effect:

```sh
$ python3 ascii.py ascii_dora.png
```

**Result showing:**

It will create a file output.txt in the folder, and print the drawing in the terminal.

![](https://labex.io/upload/S/Y/S/ww2NFQbFGU4K.png)

![](https://labex.io/upload/C/T/M/XADA7ThDM0cn.png)

please note: you might not have the exact output like the one shown here. It is acceptable since there are many other varaibels in different environmnet which may affect the output.

## 3. Exercise

You can try to use the other two pictures (1.jpg and 2.jpg) and see the output. You can set the width and height of the drawing like this.

```shell
python3 ascii.py 1.jpg --width 40 --height 40
python3 ascii.py 2.jpg --width 35 --height 35
```

##4. Summary

We have consolidated the basic knowledge of Python through this simple exercise. We hope that everyone who encounters unfamiliar functions in the process of learning will try to search and understand it.

