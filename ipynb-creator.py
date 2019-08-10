#!/usr/bin/env python3
#
# ipynb-creator.py
#
# Reads a plain text file and creates an ipynb file.
# Expects <> as the cell delimiters in the text file. Valid delimiters are:
# <code>, <markdown>, <raw>
# Comments, which are ignored may exist in the text file as:
# <comment This is a comment>
# 
# Uses the title of the plain text file as the ipynb filename.
#
# Ian Stewart
# V0.1 - 2019-08-05
#
# V0.2 - 2019-08-06
# Fixed some menu prompt text
# Fixed if there are no .txt files in the directory.
# Add ability to read python files.
#   o Read to a code cell
#   o Include Markdown header cell with program name.
#
# V0.3 - 2019-08-10
# Fixed constants to be uppercase and moved out of the way to the bottom 
# Pass filename(s) via command line arguments.
# renamed ipynb_extractor to ipynb-extractor
#
import sys
import os
try:
    import simplejson as json
except ImportError:
    import json

VERSION = "0.3"

HEADING_TXT = ("\nRead a text file and create an ipynb file." \
            "\nText files (.txt) found in the current directory:")

HEADING_PY =  ("\nRead a python file and create an ipynb file." \
            "\nPython files (.py) found in the current directory:")

def query_user_bool(prompt="Proceed?", default=True,):
    # Submit a boolean query to the User. Return True or False
    # No need for a while loop
    yes_tuple = ("y", "t", "1")
    no_tuple = ("n", "f", "0")
    # Build the prompt as [Y/n] or [N/y]
    if default:
        prompt = prompt + " [Y/n]: " 
        response = input(prompt)
        if response == "": response = "y"
        if response.lower()[0] in yes_tuple:
            return True
        else:
            return False
    else:
        prompt = prompt + " [N/y]: "
        response = input(prompt)
        if response == "": response = "n"
        if response.lower()[0] in no_tuple:
            return False
        else:
            return True


def get_text_file_list(extension):
    # In the current working directory get and display a list of all files.
    cwd = os.getcwd()
    file_list = sorted(os.listdir(cwd))
    # print(len(file_list))
    text_list = []
    for index, file_name in enumerate(file_list):
        if file_name.split(".")[-1] == extension: #"txt":
            # print(file_name)
            text_list.append(file_name)
    return text_list


def query_user_menu(menu_list, prompt=None, default=1):
    # User selects from a list. Return an index into the list
    if len(menu_list) == 0:
        return -1
    print()
    for index, item in enumerate(menu_list):
        print("{:>3}. {}".format(index + 1, item))
    if prompt == None:
        prompt = ("\nEnter the number of the item [{}]: "
                .format(default))
    else:
        prompt = ("\n{} [{}]: ".format(prompt, default))

    while True:     
        response = input(prompt)
        if response == "": response = default
        try:
            response = int(response)
            if response < 1 or response > len(menu_list):
                print("Invalid.  Requires a value between {} and {}"
                    .format(1, len(menu_list)))
                continue
            else:
                return response - 1
        except ValueError as e:
            print("Value Error. Requires a value between {} and {}"
                    .format(1, len(menu_list)))
            continue


def select_files(extension):
    # Select which ipynb files to modify
    text_list = get_text_file_list(extension)

    prompt = "Select the file for creating the ipynb file"
    index = query_user_menu(text_list, prompt)
    # If no files with extension type were found then -1 is returned
    if index == -1:
        sys.exit("No files with extension of .{} were found. Exiting"
                .format(extension))
    return text_list[index]


def get_ipynb_filename(file_text):
    filename = file_text.split(".")[0]
    filename = filename + ".ipynb"    
    return filename


def create_ipynb_template(ipynb_filename):
    with open (ipynb_filename, "w") as fout:
        fout.write(TEMPLATE)


def change_cell_0_heading(ipynb_filename):
    # Import file containing template using json module
    # Change cell 0 heading from "template" to the filename
    with open(ipynb_filename, "r+") as f:  
        data = json.load(f)        
        info_list = ipynb_filename.split(".")
        #info = "# " + info_list[0] + "\n\nCreated from a python file."
        info = ("# {}\n\nCreated from the python file: {}.py"
                    .format(info_list[0], info_list[0]))
        # print(info)        
        data["cells"][0]["source"] = ["{}".format(info)]
        f.seek(0)
        json.dump(data, f, indent=1)
        f.truncate()


def json_add_markdown(data, text):
    # Add a markdown cell to the json data
    """
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [
        "# hello_world_1\n",
        "\n",
        "Created from a text file."
       ]
      }
    """
    cell_dict = {}
    cell_dict.update({
            "cell_type": "markdown", 
            "metadata": {}, 
            "source":[text]}) 
  
    data["cells"].append(cell_dict)
    return data


def json_add_code(data, text):
    # Add a code cell to the json data
    """
      {
       "cell_type": "code",
       "execution_count": null,
       "metadata": {},
       "outputs": [],
       "source": [
        "print(\"hello world\")\n",
        "print(1+2)"
       ]
      }
    """
    cell_dict = {}
    cell_dict.update({
            "cell_type": "code",
            "execution_count": None, 
            "metadata": {}, 
            "outputs": [],
            "source":[text]}) 

    data["cells"].append(cell_dict)
    return data


def add_cell_raw(data, text):
    # TODO: Provide for raw. Probably need to pass metadata?
    """
    {
      "cell_type" : "raw",
      "metadata" : {
        # the mime-type of the target nbconvert format.
        # nbconvert to formats other than this will exclude this cell.
        "format" : "mime/type"
      },
      "source" : ["some nbformat mime-type data"]
    }
    """
    pass


def json_pop_cell_0(ipynb_filename):
    # Pop the template cell0
    with open(ipynb_filename, "r+") as f:  
        data = json.load(f)    
        data["cells"].pop(0)
        cell_total = len(data["cells"]) 
        print("Total cells in ipynb file: {}".format(cell_total))
        f.seek(0)
        json.dump(data, f, indent=1)
        f.truncate() 
    return data


def add_cell(ipynb_filename, cell_type, text):
    with open(ipynb_filename, "r+") as f:  
        data = json.load(f)    
        cell_total = len(data["cells"]) 
        #print(cell_total)
        if cell_type == "markdown":
            json_add_markdown(data, text)
        if cell_type == "code":
            json_add_code(data, text)
        if cell_type == "raw":
            #json_add_code(data, text)
            pass
        f.seek(0)
        json.dump(data, f, indent=1)
        f.truncate()  


def process_text_file(text_file):
    # Process the text file and returns two lists:
    # cell_type_list - "metadata", "code" "raw"
    # cell_source_list - the text of each cell
    # <comment> can be in a file. Ignore.
    cell_type_list = []
    cell_source_list = []
    data_line = []
    first_cell_detected = False
    temp_list = []
    temp_string = ""
    with open(text_file, "r") as fin:
        for line in fin.readlines():

            if len(line) > 0 and line.startswith("<"):
                line = line.strip()  # Get rid of newline and rhs spaces
                line = line[1:-1]  # Get rid of <, > which should be at the ends
                line = line.strip() # get rid of stray spaces
                line_list = line.split() # Might be comment with keyword
                if line_list[0] == "comment":
                    continue

                if line_list[0] in ("markdown", "code", "raw"):
                    #print("|" + line + "|")
                    cell_type_list.append(line_list[0])
                    first_cell_detected = True
                  
                    temp_list.append(temp_string)
                    cell_source_list.append(temp_list)
                    temp_list = []
                    temp_string = ""
                    continue

            else:
                if not first_cell_detected:
                    continue
                else:
                    temp_string = temp_string + line                    

    # Enter last data
    temp_list.append(temp_string)
    cell_source_list.append(temp_list) 

    # If there were blank lines at the beginning of the txt file clear the list.
    if cell_source_list[0] == ['']:
        cell_source_list.pop(0)

    #print(len(cell_type_list), cell_type_list)
    #print(len(cell_source_list), cell_source_list)

    return cell_type_list, cell_source_list

def process_py_file(py_file):
    # Read the python file and return as text string:
    with open(py_file, "r") as fin:
        py_text = fin.read()
    return py_text

def main_txt_files():
    print(HEADING_TXT)

    extension = "txt"
    text_file = select_files(extension)
    print("Text file to be used to create ipynb file is: {}".format(text_file))

    ipynb_filename = get_ipynb_filename(text_file)
    print("ipynb file created: {}".format(ipynb_filename))
 
    create_ipynb_template(ipynb_filename)

    # Optional. json_pop_cell_0() will remove this cell so change not necessary
    change_cell_0_heading(ipynb_filename)

    # Retrieve two lists from interrogating the txt file 
    cell_type_list, cell_source_list = process_text_file(text_file)

    # Add all the cells
    for index, cell_type in enumerate(cell_type_list):
        # print(cell_type, cell_source_list[index][0])
        add_cell(ipynb_filename, cell_type, cell_source_list[index][0])

    # Remove the template cell 0
    json_pop_cell_0(ipynb_filename)

def main_py_files():
    # Use a python program to create a Jupyter notebook
    # Options cell0 can be a markdown with python program name (and comments?)
    print(HEADING_PY)

    extension = "py"
    py_file = select_files(extension)
    print("Python file to be used to create ipynb file is: {}".format(py_file))

    ipynb_filename = get_ipynb_filename(py_file)
    print("ipynb file created: {}".format(ipynb_filename))

    create_ipynb_template(ipynb_filename)

    # Optional. json_pop_cell_0() will remove this cell so change not necessary
    change_cell_0_heading(ipynb_filename)

    # Retrieve two lists from interrogating the txt file 
    #cell_type_list, cell_source_list = process_py_file(py_file)    
    py_text = process_py_file(py_file)
    
    #for index, cell_type in enumerate(cell_type_list):
        # print(cell_type, cell_source_list[index][0])
    add_cell(ipynb_filename, "code", py_text)


def main_with_files(file_list):
    #print("List of files is:\n{}".format(file_list))
    # Files must have .txt or .py extensions
    for file_name in file_list:
        if file_name.split(".")[-1] == "txt" or file_name.split(".")[-1] == "py":
            #print(file_name)
            pass
        else:
            sys.exit("Must be a .txt or .py file. File {} is not valid."
                    .format(file_name))        

    # file_list has checked out as OK. Proceed with processing each file on list.
    for file_name in file_list: 
        if file_name.split(".")[-1] == "txt":
            # Process a txt file to ipynb file.
            ipynb_filename = get_ipynb_filename(file_name)
            print("ipynb file created: {}".format(ipynb_filename))
            create_ipynb_template(ipynb_filename)
            # Optional. json_pop_cell_0() will remove this cell so change not necessary
            change_cell_0_heading(ipynb_filename)
            # Retrieve two lists from interrogating the txt file 
            cell_type_list, cell_source_list = process_text_file(file_name)
            # Add all the cells
            for index, cell_type in enumerate(cell_type_list):
                # print(cell_type, cell_source_list[index][0])
                add_cell(ipynb_filename, cell_type, cell_source_list[index][0])
            # Remove the template cell 0
            json_pop_cell_0(ipynb_filename)

  
        else:
            # Process a py file to ipynb file
            ipynb_filename = get_ipynb_filename(file_name)
            print("ipynb file created: {}".format(ipynb_filename))
            create_ipynb_template(ipynb_filename)
            change_cell_0_heading(ipynb_filename) 
            py_text = process_py_file(file_name)            
            add_cell(ipynb_filename, "code", py_text)


def display_help():
    # Print either the brief or the full help and exit
    if sys.argv[1] == "-h":
        print(HELP_BRIEF)
    else:
        print(HELP_FULL)
    sys.exit()


def start_interactive():
    # No arguments werew passed with the commmand line so use menu driven.
    # Converting python programs or text file specifically for notebook
    prompt = "\nMove the contents of a python file to Jupyter notebook?"
    default = True
    response = query_user_bool(prompt, default,)
    if response:
        main_py_files()
    else:
        main_txt_files()

def main():
    # Check for args
    if len(sys.argv) == 1:
        # go to start interactive
        start_interactive()

    if len(sys.argv) > 1:
        if sys.argv[1].startswith("-h") or sys.argv[1].startswith("--h"):
            display_help()
            sys.exit()

    if len(sys.argv) == 2:
        # sys.argv may be a single file or a list of files comma seperated.
        # Don't promote comma separation. Promote space based seperation.
        # Does not accept wildcarded comma seperated. E.g.: *.txt,*.py
        #print("Goto: if len(sys.argv) == 2:")
        #print(sys.argv[1])
        file_list = sys.argv[1].split(",")
        #print(file_list)
        # Test for existance of files in this directory
        cur_dir = os.getcwd()
        folder_list = os.listdir(cur_dir)
        for file_name in file_list:
            if file_name in folder_list:
                #print("{} exists in: {} ".format(file_name, cur_dir))
                continue
            else:          
                sys.exit("{} not in directory {}.".format(file_name, cur_dir))      
        # call function and pass file_list as valid list of files in cur_dir
        main_with_files(file_list)

    if len(sys.argv) > 2:
        # sys.argv may be list of space seperated filename arguments.
        # $ python3 sysarg.py file.py file1.txt
        # Or may have been space seperated wildcarding. E.g.: *.txt *.py.
        #print(len(sys.argv), sys.argv)
        #print("Goto: if len(sys.argv) > 2")
        file_list = []
        for i in range(1, len(sys.argv)):
            #print(sys.argv[i])
            file_list.append(sys.argv[i])
        #print(file_list)
        cur_dir = os.getcwd()
        folder_list = os.listdir(cur_dir)
        for file_name in file_list:
            if file_name in folder_list:
                #print("{} exists in: {} ".format(file_name, cur_dir))
                continue
            else:          
                sys.exit("{} not in directory {}.".format(file_name, cur_dir))
        # call function and pass file_list as valid list of files in cur_dir
        main_with_files(file_list)


if __name__ == "__main__":

    if sys.version_info[0] != 3:
        sys.exit("Please use python version 3. Exiting...")

    print("\nipynb-extractor version: {}".format(VERSION))

# Put the Constants with lots of text at the end. 
# Makes the main code above easier to read.

# WARNING: Don't edit this template - Editing will corrupt json layout.
TEMPLATE = """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "template"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}"""
# WARNING: Do not accidently edit the above template.

# Put the Constants with lots of text at the end. Makes the code easier to read.

HELP_FULL = """Usage: ipynb-extractor [OPTION]... [FILE]...

Create Jupyter notebook ipynb file(s) upon having been supplied python (.py) or 
text (.txt) file(s)

[OPTION]...
Options and arguments:
   -h       print a brief help message and exits. 
   --help   print this full help message and exits.

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
$ ipynb-extractor *.py
All .py files in current directory have a Jupyter notebook ipynb file created.
$ ipynb-extractor *.py *.txt
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
o A delimiter may be surrounded by spaces. E.g. <   code         > 
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

Author: Ian Stewart - 7 August 2019.
"""

HELP_BRIEF = """Usage: ipynb-extractor [OPTION]... [FILE]...
Create Jupyter notebook ipynb file(s) upon having been supplied python (.py) or 
text (.txt) file(s)

[OPTION]...
Options and arguments:
   -h       print this brief help message and exit. 
   --help   print the full help message which includes an example then exit.

[FILE]...
If no files are provided as argruments then the program will run in a menu 
driven mode. 

Any file with the .py or .txt extensions in the current working directory may 
be provided as an argument. A list of space separated files may be provided 
for which one Jupyter ipynb file will be created for each file in the list.

The files may be selected by wildcarding with *, or *.py or *.txt.

Author: Ian Stewart - 7 August 2019.
"""
# Continue by calling the main() function routine
main()

