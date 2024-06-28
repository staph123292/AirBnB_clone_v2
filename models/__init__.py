#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

# Check the value of HBNB_TYPE_STORAGE environment variable
HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

# Import the necessary storage class based on the environment variable
if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Load initial data (assuming reload() method loads data)
storage.reload()
