import logging

def setup_logging():
    logging.basicConfig(
        filename="activity.log",
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.getLogger().addHandler(logging.StreamHandler())
