# BILLING SYSTEM 

A simple and modular **Billing System** developed using Python. The project manages products, generates bills, stores billing history, and maintains application logs using JSON files.

## Features

- Admin login authentication
- Add new products
- View all products
- Search products
- Update product details
- Delete products
- Generate customer bills
- Calculate bill totals
- Maintain bill history
- Store data using JSON files
- Application logging using Python's `logging` module
- Modular Python file structure
- GitHub Actions workflow for basic Continuous Integration (CI)

## Technologies Used

- Python
- JSON
- Python Logging
- Git
- GitHub
- GitHub Actions
- Ubuntu

## Project Structure

```text
Billing-System/
│
├── .github/
│   └── workflows/
│       └── python.yml
│
├── data/
│   ├── products.json
│   └── bills.json
│
├── logs/
│   └── billing_system.log
│
├── auth.py
├── billing.py
├── file_handler.py
├── history.py
├── logger_config.py
├── main.py
├── product.py
└── README.md 

Module Description
main.py

Connects all modules and provides the main Billing System menu.

auth.py

Handles admin authentication and login validation.

product.py

Manages product operations such as:

Add product
View products
Search product
Update product
Delete product
billing.py

Generates bills, calculates total amounts, and updates product stock.

history.py

Displays previously generated bills and their details.

file_handler.py

Handles reading and writing data to JSON files.

logger_config.py

Configures the application logging system.

products.json

Stores product information.

bills.json

Stores generated bill information.

billing_system.log

Stores application events such as successful operations, warnings, and errors.

Login Details

For demonstration purposes:

Username: admin
Password: 1234
How to Run
1. Clone the repository
git clone https://github.com/shweta-borganve/Billing-System.git
2. Open the project
cd Billing-System
3. Run the application
python main.py
Application Menu
===== Billing System Menu =====

1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Generate Bill
7. View Bill History
8. Exit
Logging

The system uses Python's built-in logging module to record application activities.

Example log messages:

INFO - Admin logged in successfully.
INFO - Product added: Rice
WARNING - Product not found.
INFO - Bill generated successfully.
ERROR - Error loading data.

The log file is stored at:

logs/billing_system.log
GitHub Actions

This project includes a GitHub Actions workflow located at:

.github/workflows/python.yml

The workflow automatically runs when code is pushed to the main branch.

It performs basic checks such as:

Setting up Ubuntu
Setting up Python
Checking the Python version
Compiling Python files

This helps practice Continuous Integration (CI) and ensures that the Python files can be compiled successfully.

Future Improvements
Add customer management
Add invoice generation in PDF format
Add database integration using MySQL or SQLite
Add automated unit testing
Add Black and Ruff code-quality checks
Add customer receipt printing
Add graphical user interface
Learning Outcomes

Through this project, I practiced:

Python programming
Functions and modules
File handling
JSON data storage
Exception handling
Logging
Git and GitHub
GitHub Actions
Basic CI/CD concepts
Author

Shweta Boraganve

GitHub: https://github.com/shweta-borganve


After pasting and saving `README.md`, run:

```bash
git add README.md
git commit -m "Add professional README"
git push origin main 