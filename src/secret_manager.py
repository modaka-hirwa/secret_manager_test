import logging
from logging import exception
import os
from pykeepass import PyKeePass, create_database
from src.log import setup_logging
from src.metadata import add_metadata
from src.config import SQLITE_FILE


#Set up logging to capture all levels of logs
setup_logging()

#Get logger instance
logger = logging.getLogger(__name__)

def create_database_kdbx(database_path, master_password):
    """Create a KeePass database if it does not exist. """
    try:
        kp = create_database(database_path, master_password)
        if kp:
            logger.info(f"KeePass database created at {database_path}")
        else:
            logger.error(f"Failed to create KeePass database at {database_path}")
    except Exception as e:
        logger.exception(f"error to creating KeePass database: {e}")

def add_secret(database_path, db_password, group_name, title, username, secret):
    """Add a new secret ( entry) to the KeePass database. """
    try:
        logger.info(f"adding secret '{title}' to KeePass database at {database_path}. ")
        kp = PyKeePass(database_path, db_password)

        group = kp.find_groups(kp.root_group, group_name)

        if not group:
            group = kp.add_group(kp.root_group, group_name)

        #add the entry (secret)
        entry = kp.add_entry(group, title, username, secret)

        if entry:
            logger.info(f"secret '{title}' successfully added to the KeePass database. ")

            add_metadata(
                name=title,
                secret_type='password',
                db_path=SQLITE_FILE,
                owner=username,
                storage_location=database_path,
                environment='prod',  # Can adjust if needed
                expiration_date=None,
                rotation_frequency=30,  # Set default or dynamic value
                compliance_tags='GDPR',
                associated_service='KeePass'
            )
        else:
            logger.error(f"Failed to add secret '{title}' to the KeePass database. ")
        kp.save()
    except Exception as e:
        logger.exception(f"error adding secret '{title}': {e}")

def retrieve_secret(database_path, db_password_maser, title):
    """Retrieve a secret (entry) from the KeePass database. """
    if not os.path.exists(database_path):
        logger.error(f"Database path {database_path} does not exits. ")
    try:
        kp = PyKeePass(database_path, db_password_maser)
        entry = kp.find_entries(title, first=True)
        if entry:
            logger.info(f"Retrieving secret '{title}' from KeePass database at {database_path}")
            logger.info(f"title: {title}, username: {entry.username}")
            return entry
        else:
            logger.warning(f"No entries found with the title '{title}'.")
            return None
    except Exception as e:
        logger.exception(f"Error retrieving secret '{title}': {e}")


def delete_secret(database_path, db_password_master, title):
    """Delete a secret (entry) from the KeePass database"""
    try:
        logger.info(f"Deleting secret '{title}' from KeePass database at {database_path}")
        kp = PyKeePass(database_path, db_password_master)

        #Find the entry by the title
        entry = kp.find_entries(title=title, first=True)
        if entry:
            # Delete the KeePass entry
            kp.delete_entry(entry)
            kp.save()

            logger.info(f"Secret '{title}' deleted successfully from KeePass database. ")
        else:
            logger.warning(f"secret '{title}' not found in KeePass database. ")
    except Exception as e:
        logger.exception(f"error deleting secret '{title}': {e}")


