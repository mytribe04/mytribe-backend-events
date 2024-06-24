# mytribe-backend
### Rules to be followed beafore pushing anything on this repo
```
1.] No direct push should be made unless very emergency case on the main, qa and dev branch
2.] Create ur own branch and push your changes with that branch and create pull request to dev branch

    Branch        | Info
    ------------- | -----------------------------
    main          | this is our production branch
    qa            | this is our testing branch
    dev           | this is our development branch

3.] Nothing should be direclty commited on these three branches as this will be live servers and changes made directly can result into failure if some buggy code is there
4.] Every PR made will be reviewed by each team member and then only PR will be approved and merged on 'dev' branch.
```
Please follow the above rule in order to maintain consistent code reviewing system and maintain proper flow of data in each branch

### Rules for Writing comments before pushing and before rasing PR
```
1.] When we commit chnages on our local branch "Mention what changes have u made in short" i.e comment should be one liner.
2.] When raising PR you need to follow,
        i.] What changes are made in detail
        ii.] State of code before changes were done
        iii.] Logic behind chnages made and code logic in brief
```
This will help code reviewers to manage and understand code easily and will maintain ur proof of work.
![alt text](https://blog.jetbrains.com/wp-content/uploads/2023/05/git-flow.png)
</br>
</br>

# A brief description of your Django project.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installing Prerequisites](#installing-prerequisites)
  - [Installing Development Tools](#installing-development-tools)
  - [Setting Up PostgreSQL Database](#setting-up-postgresql-database)
  - [Configuring Database Credentials](#configuring-database-credentials)
- [Django Project Setup](#django-project-setup)
- [Using Sourcetree](#using-dbeaver-and-sourcetree)
  - [Using Sourcetree for Version Control](#using-sourcetree-for-version-control)
- [Usage](#usage)


## Getting Started

Follow these steps to set up and configure your Django project environment.

### Installing Prerequisites

- Python (version 3.8.2)
- Django (version 4.2.2)
- pip (Python package manager)
- PostgreSQL (version 14.9.1)
- Git

### Installing Development Tools

1. Download and install [PyCharm](https://www.jetbrains.com/pycharm/).
2. Download and install [DBeaver](https://dbeaver.io/download/)
3. Install Git: Follow instructions for [Windows](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#_installing_on_windows), [macOS](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#_installing_on_macos), or [Linux](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#_installing_on_linux).
4. Download and install [Sourcetree](https://www.sourcetreeapp.com/)

### Setting Up PostgreSQL Database

1. **Launch DBeaver:**
   Open DBeaver after installation.

2. **Create a New Connection:**
   - Click on the "Database" menu.
   - Select "New Connection."

3. **Choose PostgreSQL Database:**
   - In the "Connection Type" dropdown, select "PostgreSQL."

4. **Configure Connection Settings:**
   - Fill in the connection details:
     - Host: [Hostname or IP address of the PostgreSQL server]
     - Port: [Port number, default is 5432]
     - Database: [Database name]
     - Username: [Your PostgreSQL username]
     - Password: [Your PostgreSQL password]

5. **Test Connection:**
   - Click the "Test Connection" button to verify the connection details.

6. **Save Connection:**
   - If the test is successful, click "Finish" to save the connection profile.

7. **Connect to the Database:**
   - In the DBeaver main interface, you should see your saved connection profile.
   - Double-click on the profile to connect to the PostgreSQL database.

8. **Exploring the Database:**
   - Once connected, you can navigate through the database structure.
   - The left panel shows the database explorer with schemas, tables, views, etc.

9. **Running SQL Queries:**
   - To run SQL queries, open a new SQL editor window.
   - Right-click on the desired schema, table, or database and select "SQL Editor."
   - Write your SQL query in the editor and click the "Execute" button (or press F5).

10. **Viewing Query Results:**
    - The results of your query will be displayed in the query results pane at the bottom.

11. **Managing Database Objects:**
    - Right-click on database objects (tables, views, etc.) in the explorer to manage them.

### Configuring Database Credentials

1. Open the `base.py` file in your Django project.
2. Locate the `DATABASES` section.
3. Update the configuration with your PostgreSQL database details:

   DATABASES = {

    "default": env.db(

        "DATABASE_URL",

        default="postgresql://localhost:5432/authtribe",

    ),

}

### Django Project Setup

1. Clone the repository:

   git clone -b master https://github.com/BynryGit/bx-backend.git

2. Go to the project directory:

   cd bx-backend

3. Create a virtual environment:

   python -m venv myenv

4. Activate the virtual environment:

   myenv\Scripts\activate

5. Install project dependencies:

   pip install -r requirements.txt

6. Set up the database:

   python manage.py migrate

7. Create a superuser for the Django admin:

   python manage.py createsuperuser

### Using Sourcetree

   Using Sourcetree for Version Control

1. Open Sourcetree and clone your Git repository.
2. Make changes to your code and commit them.
3. Push the changes to your remote repository.
4. Pull changes from the remote repository when needed.

### Usage

Explain how to run and use the project once it's set up. Include any relevant commands or steps.

   python manage.py runserver

Visit http://127.0.0.1:8000/admin/ in your browser to access the project.

