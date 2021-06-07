# Student Result Management System
The Student Result Management System is a desktop application that aims to provide a fast and secure automated system in order to maintain student data and publish internal assessment results along with final average marks for the same.

The system has been designed mainly focusing on colleges and universities.

## Sections
- [Software Requirements](#software-requirements)
- [Imported Modules](#imported-modules)
- [Main Functions](#main-functions)
- [Database](#database)
- [System Setup](#system-setup)
- [Procedure](#procedure)
- [Contributors](#contributors)

---
## Software Requirements

### Software Configurations
1. Operating System : Windows(Linux/MacOS)
2. Front End : Python 3.8, Tkinter
3. Back End : MySQL
4. File to executable converter : cx_Freeze module
5. Software used for programming:
    - Windows 10
    - Visual Studio Code/Python IDLE(3.8)
    - MySQL server
---
## Imported Modules

### Tkinter 
    - Tkinter is a Python binding to the Tk GUI toolkit. It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI.
on command prompt :
> **pip** install tkinter  

import statement :
> **import** tkinter



### MySQL connector
    - MySQL Connector/Python enables Python programs to access MySQL databases, using an API that is compliant with the Python Database API Specification v2.0 (PEP 249).
    - MySQL Connector/Python includes support for almost all features provided by MySQL Server up to and including MySQL Server version 8.0.

on command prompt :
> **pip** install mysql-connector-python

### cx_Freeze module
    - cx_Freeze creates standalone executables from Python scripts, with the same performance, is cross-platform and works on any platform that Python itself works on.

on command prompt :
> **pip** install cx_Freeze  

import statement :
> **import** cx_Freeze


### Python sys module
    - sys module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import statement :
> **import** sys

### Python time module
    - time module provides various time-related functions.
import statement :
> **import** time

### Python re module
    - Python has a built-in package called re, which can be used to work with Regular Expressions.

import statement :
> **import** re
---
## Main Functions
```python
def submitdb(): #connect to database if login credentials are correct

def checklogin(): #verify admin login credentials and display admin window

def submitadd(): #add student if all details are correct

def delete(): #delete student if all details are correct

def attend(): #update attendance if all details are correct

def marks(): #update marks if all details are correct

def showdata(): #display of assessment results if all details are correct

def exitwindow(): #exit application pop-up
```

---
## Database

### The database in use for the system is called _'studentresultsystem'_
It contains the following tables :
- department 
- course
- semester
- student
- attendance
- marks
- studentcount
---
## System Setup
1. Convert the setup file with .py extension to .exe installer.
```
 python studentsetup.py bdist_msi
 ```
 2. Double click on installer and choose path on which the application is to be stored.
 
 3. A desktop shortcut of the application will be created and it will be ready to run.
 
---
## Procedure
- On opening application, first connect to the database.
- Provide required login credentials to connect to the respective MySQL server(host,user and password details)
- To use Admin login, click on Admin Login button :
    - Provide Admin login details.
    Defaults set to :

        Username : **admin** 
        Password : **123**
    - Click on desired option :

        Add student

        Delete student

        Update attendance

        Update marks
        - The student details to be inserted/deleted must be of a specific format.
        - Name : Cannot be blank. Eg: Abcd
        - USN : Eg. 1CR18CS001
        - Email ID  Eg. abcd18cs@gmail.com
        - DOB : yyyy-mm-dd Eg. 2000-01-01
        - Gender : Eg. M/m/Male/F/f/Female/O/o/Other
        - Department ID : As specified in the respective database Eg. **2** for CSE
        - Phone number : Any 10 digit number starting with 9/8/7/6

    - Click on Go Back button to return to main window.
- To view student result, click on Student Result button.
    - Enter the required details to view result on the display frame placed on the right side of main window.
- To exit application, click on Exit button.
---
## Contributors

__Publishers of the application :__

- _Sourita Poddar (SP)_

- _Sraddha Challagundla (SC)_


---