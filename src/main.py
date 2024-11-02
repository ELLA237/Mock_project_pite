import yaml
import logging

# Load configuration from the YAML file
def load_config():
    with open('../config/config.yaml', 'r') as file:
        conf = yaml.safe_load(file)  # Reads the YAML file and parses it into a Python dictionary
    return conf

config = load_config()  # Call the function to load the configuration

#setup logging and logging storage
def setup_logging():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("../logs/app.log",mode ='a'),  # Logs to a file
                            logging.StreamHandler()  # Logs to the console
                        ])

setup_logging()  # Calls the function to set up logging
logging.info("Logging is set up.")
