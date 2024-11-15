import yaml
import logging
from module2 import DataService, Client
import threading
import time


def load_config():
    with open('../config/config.yaml', 'r') as file:
        conf = yaml.safe_load(file)
    return conf


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        handlers=[
            logging.FileHandler("../logs/app.log", mode='a', encoding='utf-8'),
            logging.StreamHandler(),
        ],
    )

def main():
    setup_logging()
    logging.info("Logging is set up.")
    
    config = load_config()
    logging.info("Configuration loaded.")

    # Initialize DataService
    data_service = DataService(config)
    data_service.start_service()

    # Initialize Client
    client = Client(data_service)
    client.start(interval=120)  # Start client thread with 5-minute interval

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Stopping services...")
    finally:
        # Stop services and threads
        client.stop()
        data_service.stop_service()
        logging.info("All services stopped.")

 


if __name__ == "__main__":
    main()
