import yaml
import logging
from module2 import DataService
from module2 import Client
from module1 import DataFetcher
import threading,time

# Load configuration from the YAML file
def load_config():
    with open('../config/config.yaml', 'r') as file:
        conf = yaml.safe_load(file) 
    return conf

#config = load_config()  # Call the function to load the configuration

#setup logging and logging storage
def setup_logging():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8',
                        handlers=[
                            logging.FileHandler("../logs/app.log",mode ='a', encoding='utf-8'),  # Logs to a file
                            logging.StreamHandler()  # Logs to the console
                        ])

setup_logging()  # Calls the function to set up logging
logging.info("Logging is set up.")
time.sleep(300)

def client_thread_function(client):
    while True:
        client.request_weather_update()
        time.sleep(300)  # Wait for 5 minutes
    

def main():
    
    config = load_config()

    # Initialize classes
    fetcher = DataFetcher(config)
    data = fetcher.fetch_data()
    if data:
        logging.info(f"Fetched data: {data}")
    else:
        logging.error("Failed to fetch data.")

    data_service = DataService(config)
    data_service.start_service()

    client = Client(data_service)
    client_thread = threading.Thread(target = client_thread_function,args = (client,))
    client_thread.start()

    try:
        client_thread.join()
    finally:
        data_service.stop_service()

if __name__ == "__main__":
    main()
