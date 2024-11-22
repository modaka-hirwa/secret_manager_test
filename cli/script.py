import argparse
import logging
from getpass import getpass
from src.secret_manager import add_secret, retrieve_secret, delete_secret
from src.metadata import retrieve_data
from src.log import setup_logging

from dotenv import load_dotenv, set_key

setup_logging()

def write_to_dotenv(key, value):
    """Write a key-value pair to the .env file"""

    load_dotenv()
    dotenv_path = '.env'
    set_key(dotenv_path, key, value)

def parse_arguments():
    """Parse command-line arguments and return them. """
    parser = argparse.ArgumentParser(description="Secret Manager CLI")

    #Add subcommands
    subparsers =parser.add_subparsers(dest="command", help="Available commands")

    #metada subcommand
    metadata_parser = subparsers.add_parser("metadata", help="Metadata operations")
    metadata_parser.add_argument("action", choice=['get'], help="Action to perform on metadata")
    metadata_parser.add_argument("--db", type=str, required=True, help="Database name")
    metadata_parser.add_argument("--query", type=str, required=True, help="Metadata query")

    # secret subcommand
    secret_parser = subparsers.add_parser("secret", help="Secret operations")
    secret_parser.add_argument("action", choices=["add", "get", "delete"], help="Action to perform on secrets")
    secret_parser.add_argument("--db", type=str, required=True, help="Database name")
    secret_parser.add_argument("--password", type=str, help="Database password (prompted if not provided)")
    secret_parser.add_argument("--group", type=str, help="Group name (for add)")
    secret_parser.add_argument("--title", type=str, help="Secret title")
    secret_parser.add_argument("--username", type=str, help="Username for secret (for add)")
    secret_parser.add_argument("--secret_password", type=str, help="Secret password (for add)")
    secret_parser.add_argument("--delete", type=str, help="Title of secret to delete")

    # Parse arguments and return them
    return parser.parse_args()

def handle_metadata_get(args):
    """Handle the 'get' action for metadata. """
    logging.info(f"Fetching metadata from database: {args.db} with query: {args.query}")

    try:
        retrieve_data(args.db, args.query)
        logging.info("Metadata retrieval successfully")
    except Exception as e:
        logging.error(f"Error retrieving metadata: {str(e)}")

def handle_secret_add(args):
    """Handle adding a secret. """
    if not args.password:
        args.password = getpass("Enter database password: ")

    logging.info(f"Adding secret to database {args.db} for group {args.group} with title {args.title}")
    try:
        add_secret(args.db, args.password, args.group, args.title, args.username, args.secret_password)
        logging.info("Secret added successfully. ")

    except Exception as e:
        logging.error(f"Error adding secret: {str(e)}")

def handle_secret_get(args):
    """Handle retrieving a secret. """
    if not args.password:
        args.password = getpass("Enter database password: ")
    logging.info("Secret retrieval successfully. ")

    try:
        data = retrieve_secret(args.db, args.password, args.title)
        logging.info("Secret retrieval successfully. ")
        write_to_dotenv(f"SECRET_{args.title}", str(data.password))
    except Exception as e:
        logging.error(f"Error retrieving secret: {str(e)}")

def handle_secret_delete(args):
    """Handle deleting a secret. """
    if not args.password:
        args.password = getpass("Enter database password: ")
    logging.info(f"Deleting secret from database {args.db}")
    try:
        delete_secret(args.db, args.password, args.delete)
        logging.info("Secret deleted successfully. ")

    except Exception as e:
        logging.error (f"Error deleting secret: {str(e)}")


def main():
    args = parse_arguments()

    # Log the command executed
    logging.info(f"Started execution with command: {args.command}")

    try:
        # Handle each command with the corresponding function
        if args.command == "metadata" and args.action == "get":
            handle_metadata_get(args)

        elif args.command == "secret":
            if args.action == "add":
                handle_secret_add(args)
            elif args.action == "get":
                handle_secret_get(args)
            elif args.action == "delete":
                handle_secret_delete(args)

    except Exception as e:
        logging.critical(f"Critical error occurred: {str(e)}")

    logging.info("Program execution finished")

if __name__ == "__main__":
    main()
