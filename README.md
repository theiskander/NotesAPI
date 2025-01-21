# Notes API

A RESTful API for managing notes, designed as a portfolio project. It supports basic CRUD operations and additional features like authentication, tags, and search.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete notes.
- **SQLite Database**: Local storage for easy setup and portability.
- **Interactive Documentation**: Swagger UI for API exploration.
- **Extendable Design**: Ready for additional functionality like authentication and tags.

## Technologies

- **Programming Language**: Python 3.10+
- **Framework**: Flask or FastAPI
- **Database**: SQLite
- **Documentation Tools**: Swagger

## Project Structure

```
NotesAPI/
├── app.py
├── models.py
├── routes/
│   ├── __init__.py
│   ├── notes.py
├── templates/
├── static/
├── migrations/
├── tests/
├──.gitignore
├── requirements.txt
└── README.md
```

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

## Usage

- Access the API at `http://127.0.0.1:5000`.
- Interactive API documentation is available at `/docs`.

## To Do

- Add user authentication and authorization.
- Implement tags and categories for notes.
- Add search and filtering functionality.
- Deploy the application on a cloud platform.