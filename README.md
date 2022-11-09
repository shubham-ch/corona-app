# README for # CoronaArchive

## About the Project

The purpose of this project is to build a web service for Corona disease management which
enables digital tracking of citizens which enter certain places and keeping the records in case of a
Covid infection spread.

## File Structure

```
\--se-sprint01-team-33
    \--corona_archive
        |--forms.py
        |--models.py
        |--routes.py
        |--__init__.py
        |--database.db
        \--static
            \--                       # All the CSS Files
        \--templates
            \--                       # Main HTML files
        \--tests
            |--test_sprint_01.py      # Main Testing file
    |--run.py                         # program starts from here
    |--.gitignore                     #to ignore some files to git
    |--README.md
    |--requirements.txt
```

## Getting Started

### Prerequisites

- [python](https://www.python.org/downloads/)

## Installation Guide

1. Clone repository :

```
$ git clone https://github.com/Magrawal17/se-02-team-33.git
```

2. Install `virtualenv`:

```
$ pip install virtualenv
```

3. Open a terminal in the project dir and run following command to create separate env for the project. This make sure your project files are isolated to other installed libraries :

```
$ virtualenv env
```

4. Then run the command,

```
#if u are using windows
$ ./env/Scripts/activate
#Or if u are using linux or macOS
$ source env/bin/activate
```

5. Then install the dependencies:

```
$ pip install -r requirements.txt
```

6. Run the sql file under sql/ on your mysql server to initialise database.
   Preloaded agent credentials: 'agent@gmail.com', 'hello@12'
   Preloaded hospital credentials: 'legithospital@gmail.com', 'hello@12'

7. Finally start the web server using flask (though it can be run using python interpreter directly, it is recommended to run using flask):

```
$ (env) python run.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

# Run tests

Run this code once you are entire the environment

```sh
$ python corona_archive/test/test_sprint_01.py
```

## Sprint 1 Changes done

✅ Created html templates for pages "/", "/visitor", "/visitor/sign_up" and other pages

✅ Created routes for different url's

✅ Created models for storage for datas of different users

✅ Created forms using flask_wtf and wtforms

✅ Linked form with html

✅ Added authentication(login, logout, registration) using flask_login library

✅ Created tests for different functions and requests

✅ Created some users for testing purpose

✅ Added QR code for location owner

## Sprint 2 Changes

✅ Corrected some README commands which had errors

✅

## Sprint 3 Changes

✅ Fixed the bug of the location owner page

✅ Fixed the bug of the visitor login page

✅ Added a visitor and a hospital button to the agent dashboard so that he can display the list of any of them

✅ Added a form to the hospital dashboard so that he can add the details of each visitor and mark it as infected or uninfected

- Migration of database into mysql from sqlalchemy

- Creation of new templates to fascilitate new mysql based routes. Plese refer to the commit changes for more details

- Addition of QR code scanning using camera permissions from the website itself

- Migration of login to databse based query checking and flask sessions

## Sprint 4 Changes done

✅ Created Remember Me feature by using Cookies.

✅ Created routes for changing infected status bu Hospitals.

✅ Created routes for accepting Hospitals bu Agents

✅ Created system to change the infected status.

✅ Feature where Agent can see the hospital data and confirm.

✅ Feature for sending email when infected is added.

✅ Created new tests and changed few.

✅ Created some users for testing purpose.

✅ Fixed QR code for Linux systems.

✅ Changed and Updated Readme.

✅ Fixed everything for final push of project according to docs.
