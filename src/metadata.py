import sqlite3
import logging
import os
from src.log import setup_logging
from datetime import datetime

# Configure basic logging setup
setup_logging()

# Create log instance
logger = logging.getLogger(__name__)

def init_db(db_path):
    """Create database if it does not exist for metadata"""
    logger.debug(f"Checking if the database exists at {db_path}")
    if not os.path.exists(db_path):
        logger.info(f"Database does not exist. Creating metadata database at {db_path}")
        try:
            conn = sqlite3.connect(db_path)
            with open("schema.sql", "r") as schema_file:
                logger.debug("Reading schema from schema.sql")
                conn.execute(schema_file.read())
            conn.commit()
            conn.close()
            logger.info(f"Database created successfully at {db_path}")
        except Exception as e:
            logger.error(f"Failed to create the database at {db_path}: {e}")
    else:
        logger.info(f"Database already exists at {db_path}")

def add_metadata(name, secret_type, db_path, owner=None, storage_location=None,
                 environment=None, expiration_date=None, rotation_frequency=None,
                 compliance_tags=None, associated_service=None, is_encrypted=1):
    """Add metadata into the database"""
    logger.debug(f"Preparing to insert metadata for {name} into the database at {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        time = datetime.now()
        current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(
            """
            INSERT INTO secrets (name, type, created_at, last_accessed_at, last_updated_at, 
                                 owner, storage_location, environment, expiration_date, 
                                 rotation_frequency, compliance_tags, associated_service, is_encrypted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, secret_type, current_timestamp, None, current_timestamp,
             owner, storage_location, environment, expiration_date,
             rotation_frequency, compliance_tags, associated_service, is_encrypted)
        )
        conn.commit()
        conn.close()
        logger.info(f"Metadata for {name} added successfully to the database.")
    except sqlite3.Error as e:
        logger.error(f"Error occurred while adding metadata for {name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while adding metadata for {name}: {e}")

def retrieve_data(db_name, query, params=()):
    """Retrieve data from the database"""
    logger.debug(f"Executing query to retrieve data from {db_name} with params {params}")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()

        logger.debug(f"Query executed successfully, retrieved {len(results)} rows")
        return results
    except sqlite3.Error as e:
        logger.error(f"Error occurred while retrieving data from {db_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred while retrieving data: {e}")
    finally:
        conn.close()

def delete_data(db_name, query, params=()):
    """Delete data from the database"""
    logger.debug(f"Executing query to delete data from {db_name} with params {params}")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        logger.info(f"Rows deleted: {cursor.rowcount}")
    except sqlite3.Error as e:
        logger.error(f"Error occurred while deleting data from {db_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting data: {e}")
    finally:
        conn.close()

