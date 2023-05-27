## PropertyManagement

# Getting Started

This is a property management system which enables users to manage properties by submitting theri documents

To run this code you just follow this procedures

# Installation

First clone the repository from GitHub and switch to the new directory:

    $ `git clone https://github.com/codertjay/PropertyManagement`
    $ `cd smsgpt`

Activate the virtualenv for your project.

$`python -m venv venv`

On Linux

$`source venv/bin/activate`

On Windows

$`venv\Scripts\activate.bat`

Install project dependencies:

    $ `pip install -r requirements.txt`

Set Up your .env Just use the .env--sample provided to create yours

Then simply apply the migrations:

    $ `python manage.py migrate`

You can now run the development server:

    $` python manage.py runserver`

##### And also the .env File will contain

`DEBUG=True`

`SECRET_KEY=SECRET_KEY
`

`POSTGRESDB_NAME=POSTGRESDB_NAME`

`POSTGRESDB_USER=POSTGRESDB_USER`

`POSTGRESDB_PASSWORD=POSTGRESDB_PASSWORD`

`POSTGRESDB_HOST=localhost`



