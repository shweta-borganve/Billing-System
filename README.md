# Billing System

A robust Python-based billing management system featuring automated testing, database management, user authentication with role-based access, and automated code quality tools.

---

## Features

- **Authentication & Roles**: Secure login with role-based permissions (`src/auth/`).
- **Database Operations**: Clean relational schema handling and operations (`src/database/`).
- **Automated Testing**: Comprehensive test coverage using `pytest` (`tests/`).
- **Code Quality & Linting**: Automated formatting and linting pipelines via **Black**, **Isort**, and **Ruff**.
- **CI/CD**: GitHub Actions workflow to validate code quality and run tests automatically on every push.

---

## Project Structure

```text
Billing-System/
├── .github/workflows/    # CI/CD pipelines
├── src/                  # Source code (auth, database, services, etc.)
├── tests/                # Automated pytest test suite
├── pyproject.toml        # Tool configurations (black, isort, ruff, pytest)
├── requirements.txt      # Project dependencies
└── README.md
```

> Generated files such as `__pycache__`, `.pyc` files, and log files are excluded from Git using `.gitignore`.

## Module Description

### main.py

Connects all modules and provides the main Billing System menu.

### auth.py

Handles admin authentication and login validation.

### product.py

Manages product operations such as:

* Add product
* View products
* Search product
* Update product
* Delete product

### billing.py

Generates bills, calculates total amounts, and updates product stock.

### history.py

Displays previously generated bills and their details.

### file_handler.py

Handles reading and writing product and billing data using JSON files.

### logger_config.py

Configures the application's logging system and records application events.

### test_main.py

Contains unit tests for testing the application's functionality using Python's built-in `unittest` framework.

### requirements.txt

Contains external Python packages used for development and Continuous Integration checks.

Current dependencies:

```text
black
ruff
```

## Login Details

For demonstration purposes:

```text
Username: admin
Password: 1234
```

> These credentials are for demonstration purposes only and should not be used in a production application.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/shweta-borganve/Billing-System.git
```

### 2. Open the project

```bash
cd Billing-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

## Application Menu

```text
===== Billing System Menu =====

1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Generate Bill
7. View Bill History
8. Exit
```

## Logging

The system uses Python's built-in `logging` module to record application activities.

The application uses different log levels:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

Example log messages:

```text
INFO - Billing System started.
INFO - Admin logged in successfully.
INFO - Product added: Rice
WARNING - Product not found.
INFO - Bill generated successfully.
ERROR - Error loading data.
```

The generated log file is stored locally at:

```text
logs/billing_system.log
```

Log files are excluded from Git using `.gitignore`.

## Unit Testing

The project includes `test_main.py` for unit testing.

Run the tests using:

```bash
python -m unittest test_main.py -v
```

The test results indicate whether the implemented functionality passes or fails.

## GitHub Actions

The project includes a GitHub Actions workflow located at:

```text
.github/workflows/python.yml
```

The workflow runs automatically whenever code is pushed to the `main` branch.

It can also be triggered manually using the `workflow_dispatch` option.

### CI Workflow

The workflow performs the following steps:

```text
Push code to main
        ↓
Checkout repository
        ↓
Set up Ubuntu
        ↓
Set up Python 3.12
        ↓
Check Python version
        ↓
Install dependencies
        ↓
Run Black
        ↓
Run Ruff
        ↓
Compile Python files
        ↓
Run unit tests
        ↓
PASS or FAIL
```

### Continuous Integration

GitHub Actions automates project checks whenever new code is pushed.

If all checks pass, the workflow completes successfully.

If any check fails, GitHub Actions reports the failure so the issue can be identified and fixed.

## Code Quality

### Black

Black is used to check Python code formatting.

Run locally:

```bash
black --check .
```

### Ruff

Ruff is used to check code quality and identify common Python coding issues.

Run locally:

```bash
ruff check .
```

## Requirements

The project uses a `requirements.txt` file to manage external Python packages required for development and CI.

```text
black
ruff
```

Install them using:

```bash
pip install -r requirements.txt
```

## JSON Data Storage

The application uses JSON files for simple data persistence.

### products.json

Stores product information such as:

* Product ID
* Product name
* Price
* Quantity/stock

### bills.json

Stores generated billing information and bill history.

Using JSON makes the project simple to understand and suitable for practicing file handling and data management in Python.

## Error Handling

The project uses exception handling to manage possible runtime problems such as:

* Invalid user input
* Invalid product information
* Missing JSON files
* Empty or corrupted JSON files
* Product not found
* Invalid menu choices
* File reading and writing errors

This helps prevent the application from terminating unexpectedly.

## Git and GitHub

Git is used for version control and GitHub is used to store and manage the project repository.

The project includes:

* Git version control
* GitHub repository
* Commit history
* `.gitignore`
* GitHub Actions
* Continuous Integration workflow

## .gitignore

The project uses `.gitignore` to prevent generated and unnecessary files from being tracked by Git.

Examples include:

```text
__pycache__/
*.pyc
logs/*.log
venv/
.venv/
.vscode/
```

This keeps the GitHub repository clean and prevents generated files from creating unnecessary merge conflicts.

## Future Improvements

The following features can be added in future versions:

* Customer management
* Customer registration and login
* Role-based authentication
* Invoice generation in PDF format
* Database integration using MySQL or SQLite
* Improved automated unit test coverage
* Customer receipt printing
* Graphical User Interface (GUI)
* Advanced billing reports
* Sales and revenue reports
* Product category management
* Low-stock notifications
* Date and time based bill reports
* Export bills to CSV or Excel
* Search and filter billing history
* Password hashing and improved security

## Learning Outcomes

Through this project, I practiced:

* Python programming
* Functions and modules
* Modular programming
* File handling
* JSON data storage
* Exception handling
* Logging
* Unit testing
* Git and GitHub
* Git commands
* GitHub Actions
* YAML workflow configuration
* Continuous Integration (CI)
* Black code formatting
* Ruff code quality checking
* Linux/Ubuntu commands
* Project structure and code organization

## Author

**Shweta Boraganve**

GitHub: https://github.com/shweta-borganve 