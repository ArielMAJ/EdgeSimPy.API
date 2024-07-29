# FastAPI Backend Template

A FastAPI backend template for a kickstart on new projects.

## Features

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **Swagger UI**: FastAPI automatically generates interactive API documentation.
- **SQLAlchemy**: Database toolkit and ORM for SQL databases.
- **Alembic**: Lightweight database migration tool for SQLAlchemy.
- **Pytest**: Testing framework.
- **Poetry**: Dependency management and packaging.
- **Pre-commit**: Framework for managing and maintaining multi-language pre-commit hooks.
- **Makefile**: Simplified commands for development tasks.
- **Docker Compose**: Containerized development environment for Postgres database.
- **.env**: Environment variables management.
- **GitHub Actions**: CI/CD workflows for automated testing.

## Installation and Setup

### Prerequisites

These can be installed using package managers like `apt`, `brew`, or `choco`. See the respective websites (or Google Search) for installation instructions.

- Python 3.9+ (required; use `pyenv` for managing Python versions);
- pyenv (optional, for managing Python versions);
- Docker Compose (optional, highly recommended, for easily running database locally);
- Poetry (optional, highly recommended, for dependency management);
- Makefile (optional, highly recommended, for simplified commands);
- Git (optional, for version control).

### Steps

See Makefile for a list of available commands and their descriptions. You can also run `make help` or, optionally just `make`, to see the available commands.

These steps assume you have `make` installed. If you don't have it, copy and run the commands in your terminal instead.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ArielMAJ/FastAPI-backend-template.git
   cd FastAPI-backend-template
   ```

2. **Set Up Environment Variables**

   Copy the example environment file and modify it as needed. If you use docker compose for running the database locally, you can keep the default database values. See [this link](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens) for more information on setting up JWT `SECRET_KEY`.

   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies**

   - Using Poetry:

     ```bash
     make install
     ```

   - Using pip:

     ```bash
     pip install -r requirements.txt
     ```

4. **Database Setup**

   Start the Postgres database using Docker Compose:

   ```bash
   make up-database
   ```

   Run migrations to set up the database:

   ```bash
   make migrate
   ```

5. **Run the Application**

   Start the FastAPI server:

   ```bash
   make run
   ```

   - The FastAPI server will be available at `http://localhost:3000`.
   - API documentation can be accessed at `http://localhost:3000/docs`.

## Testing

Running automated tests:

```bash
make test
```

## Writing your own code

You can use this repository as a template for your own projects. You can start by modifying the existing code or adding new files as needed, using the existing ones as example or reference of how to structure your code. Make sure to try to follow the same folder/file structure and conventions to keep the codebase clean and organized.

---

Pre-commit hooks are set up to run automatically before each commit. They will check for code formatting, linting, and other issues. You can also run them manually with:

```bash
make pre-commit
```

---

For changes to the database, you can follow these steps:

1. Make changes to the database models in `api/database/models`.
2. Make sure new models are imported in `api/database/__init__.py`.
3. Create a new revision:
   ```bash
   make revision
   ```
4. Check the new revision file created in `api/database/alembic/versions` and make sure it reflects the changes you expect.
5. Apply the migration to your database (the database needs to be running and available):
   ```bash
   make migrate
   ```

You can also undo the last migration with:

```bash
make downgrade
```

## Deployment

This template is set up to be easily deployed to Vercel. Vercel provides easy, free, deployment/hosting of web applications and databases. You can also setup the database with a couple click and it should be just a matter of just setting up the environment variables in the Vercel dashboard and deploying the application with a few clicks.

## Contributing

Feel free to contribute to this project. You can open issues for bugs or feature requests, and submit pull requests for improvements or fixes. Make sure to follow the existing code style and conventions. Also, make sure to run the pre-commit hooks before submitting a pull request. If you have any questions, feel free to ask.
