# configure

   modify lines in app/core/config.py

# install dependencies

    poetry install

# initialize SQLite database

    poetry run python create_database.py
    poetry run python start_database.py

# run backend app

    poetry run uvicorn main:app --reload

# API docs
    http://127.0.0.1:8000/docs

Have fun!