# Ingestion Django App

The **Ingestion** app within the **electricity_flow** project is a Django application
that allows you to import electricity meter reading files and store the data in an
SQLite database. The import process can be done either through a REST API or via a
Django management command that searches a specified directory for all files, parses
them, and saves them to the database.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
    - [1. REST API](#rest-api)
    - [2. Management Command](#management-command)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## Requirements

- Python 3.10
- Django 5.1.1
- SQLite

## Installation

1. Clone this repository:

   ```bash
   git clone git_url_here
   cd ingestion

## Pre requisites

* Valid python and django installation

## How to run

* Navigate to the `/kraken/electricity_flow/electricity_flow` directory
* In a new terminal tab, run  `python3 manage.py migrate` to build the database
* In a new terminal tab, run  `python3 manage.py runserver` to start the app
* Navigate to the Django admin panel to view the new tables http://127.0.0.1:8000/admin/
* With the app still running, run this command to import data from a specified
  file `python3 manage.py run_index FILENAME_HERE`

## Testing

* In a new terminal tab, run `python3 manage.py test` to run the tests

## Potential improvements

Filter for relevant filenames (e.g. “D0010” only)
Import files using REST via the web
Make use of the headers
Use a pep 8 linting tool to format
Validation class
Better logic for identifying duplicates
Add more logging as per requirements
Add a makefile for easy commands
Add tests for management command
Add tests for search and filter
Add negative test cases
Refactor management command to smaller functions
Add concise exception handling

## Project Owner

* **Owner:** Jaimin Chouhan
* **Email:** jaimin.chouhan@gmail.com
* **GitHub:** github.com/jaiminchouhan