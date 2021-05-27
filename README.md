

A backend template for developing modern web application. Using FastAPI, SQLite as database, automatic HTTPS and more.

# Configure

   modify lines in app/core/config.py

# Install dependencies

    poetry install

# Initialize SQLite database

    poetry run python create_database.py
    poetry run python start_database.py

# Run backend app

    poetry run uvicorn main:app --reload

# API docs
    http://127.0.0.1:8000/docs

Have fun!