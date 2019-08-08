# ipynb_creator

## Introduction

**ipynb creator** is a python program designed to:

1. Read a python progam and generate a Jupyter notebook *.ipynb* file.

2. Read a text file and based on delimiters to determine code or markdown cells, generate a Jupyter notebook *.ipynb* file.

The programs full help infromation is obtained as follows:



```
$ python3 ipynb_creator.py --help

ipynb_creator version: 0.3
Usage: ipynb_creator [OPTION]... [FILE]...

Create Jupyter notebook ipynb file(s) upon having been supplied python (.py) or
 text (.txt) file(s)

[OPTION]...
Options and arguments:
 -h print a brief help message and exits.
 --help print this full help message and exits.

[FILE]...
If no files are provided as arguments then the program will run in a menu
 driven mode and prompt you to select either a python (.py) or a text (.txt)
 file.

Any file with the .py or .txt extensions in the current working directory may
 be provided as an argument. The created ipynb file will have the same name as
the .py or .txt from which it was created.

A list of space separated files may be provided for which one Jupyter ipynb
file will be created for each file in the list.

The files may be selected by wildcarding with *, or *.py or *.txt. E.g.
$ ipynb_creator *.py
All .py files in current directory have a Jupyter notebook ipynb file created.
$ ipynb_creator *.py *.txt
All .py and .txt files have a Jupyter notebook ipynb files created.

Notes:
For an ipynb file created from a python file its first cell will be markdown
containing the python script file name. The second cell will be the python
 script in a code cell.

For an ipynb file created from a text file its cells will have been determined
by the <code> and <markdown> delimiters that were inserted into the text file.

For the text (.txt) files the delmiter guidelines are:
o Delimiters start with left angle bracket "<" and end with right angle ">".
o A delimiters left angle bracket "<" must be the first character on a line.
o Delimiters that create Jupyter notebook cells are <markdown> and <code>.
o Delimiter <raw> is accepted but not processed.
o Delimiter <comment> allows one line comments within the text file.
 E.g. < comment The next code cell is from my hello_world.py program>
o Other delimiters may include a comment.
 E.g. <code This is my /python/hello_world.py program>
o A delimiter may be surrounded by spaces. E.g. < code >
 o Text that follows a delimiter becomes the markdown or the code.
o Lines of text before the first delimiter are ignored.

Example hello_world.txt file:

Anything written here is ignored because its before the first delimiter.
This file is stored in my github repository and in my /python/dev/ folder.
I wrote this text in August 2019.

<markdown>
# Hello World Heading
This is my *hello world* program.
<code>
# hello_world
print("hello world")

< markdown The second python program will do some maths.>

# Maths

This is how to obtain the **square root of 2**

< code >
import math
< comment Remember to include the import math!>
a = 2
print(math.sqrt(a))
< markdown >

### *The End*

<comment This is the end of the hello_world.txt example file.>

Author: Ian Stewart - 7 August 2019
```





## Notes:

For an ipynb file created from a python file its first cell will be markdown containing the python script file name. The second cell will be the python script in a code cell.

For an ipynb file created from a text file its cells will have been determined
by the <code> and <markdown> delimiters that were inserted into the text file.

For the text (.txt) files the delmiter guidelines are:

* Delimiters start with left angle bracket "<" and end with right angle ">".
* A delimiters left angle bracket "<" must be the first character on a line.
* Delimiters that create Jupyter notebook cells are <markdown> and <code>.
* Delimiter <raw> is accepted but not processed.
* Delimiter <comment> allows one line comments within the text file. E.g. < comment The next code cell is from my hello_world.py program>
* Other delimiters may include a comment. E.g. <code This is my /python/hello_world.py program>
* A delimiter may be surrounded by spaces. E.g. < code >
* Text that follows a delimiter becomes the markdown or the code.
* Lines of text before the first delimiter are ignored.







Example hello_world text file:

Cut and paste this into the file help_text_example.txt__

```

Anything written here is ignored because its before the first delimiter.
This file is stored in my github repository and in my /python/dev/ folder.
I wrote this text in August 2019.
<markdown>
# Hello World Heading
This is my *hello world* program.
<code>
# hello_world
print("hello world")
< markdown The second python program will do some maths.>
# Maths
This is how to obtain the **square root of 2**
< code >
import math
< comment Remember to include the import math!>
a = 2
print(math.sqrt(a))
< markdown >
### *The End*
<comment This is the end of the hello_world.txt example file.>
```
