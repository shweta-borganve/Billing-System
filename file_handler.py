import json
import os

from logger_config import logger


DATA_FOLDER = "data"
PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")
BILLS_FILE = os.path.join(DATA_FOLDER, "bills.json")


def load_data(filename):
    try:
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        if not os.path.exists(filename):
            with open(filename, "w") as file:
                json.dump([], file, indent=4)

            return []

        with open(filename, "r") as file:
            data = json.load(file)

        logger.info(f"Data loaded successfully from {filename}")
        return data

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON data in {filename}")
        return []

    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return []


def save_data(filename, data):
    try:
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        logger.info(f"Data saved successfully to {filename}")

    except Exception as e:
        logger.error(f"Error saving {filename}: {e}") 