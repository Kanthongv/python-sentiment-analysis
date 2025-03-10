import logging

# Configure logging
logging.basicConfig(
    filename='log/app.log',  # Log file name
    level=logging.DEBUG,   # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

logger = logging.getLogger(__name__)  # Create a logger object 