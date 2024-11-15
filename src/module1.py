import logging,requests


class DataFetcher:
    #Class to fetch data from a remote source.
    def __init__(self, config):
        self.api_key = config['api_key']
        self.url = config['service_url'].format(
            base_url=config['base_url'],lat=config['lat'], lon=config['lon'], api_key=config['api_key']
        )
        self.polling_interval = config['polling_interval']
        self.timeout = config['timeout'] 
        #logging.info("DataFetcher initialized with URL: %s", self.url)

    def fetch_data(self):
        try:
            logging.info("Fetching data from %s", self.url)
            response = requests.get(self.url, timeout= self.timeout)
            response.raise_for_status()
            data = response.json()
            logging.info("Data fetched successfully.")
            return data
        except requests.exceptions.Timeout:
            logging.error("Request timed out while fetching data.")
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching data: %s", e)
        return None