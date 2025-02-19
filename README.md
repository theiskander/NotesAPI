# Notes API

A RESTful API for managing notes, designed as a portfolio project. It supports basic CRUD operations and additional features like authentication, tags, and search.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete notes.
- **SQLite Database**: Local storage for easy setup and portability.
- **Extendable Design**: Ready for future features like authentication, tags, and search.

## Technologies

- **Programming Language**: Python 3.10+
- **Framework**: Flask with Blueprints
- **Database**: SQLite

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/theiskander/NotesAPI.git
   cd notes-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask run
   ```