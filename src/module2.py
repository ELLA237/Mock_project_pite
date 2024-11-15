import logging
import threading
import time
from module1 import DataFetcher

class DataService:
    def __init__(self, config):
        self.fetcher = DataFetcher(config)
        self.polling_interval = config['polling_interval']
        self.latest_data = None
        self.data_lock = threading.Lock()  # Lock to synchronize data access
        self.stop_event = threading.Event()

    def start_service(self):
        #Starts the background thread for continuous data fetching.
        logging.info("Starting data service...")
        self.thread = threading.Thread(target=self._fetch_data_continuously)
        self.thread.start()
    
    def _fetch_data_continuously(self):
     #Continuously fetches data in the background with error handling.
     retry_count = 0  # To keep track of retries
    
     while not self.stop_event.is_set():
        try:
            data = self.fetcher.fetch_data()  # Attempt to fetch data
            if data:
                with self.data_lock:  # Lock before updating shared data
                    self.latest_data = data
                    logging.info("Latest data updated.")
                retry_count = 0  # Reset retry count after successful fetch
            
            time.sleep(self.polling_interval)  # Wait before the next fetch

        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            

    def stop_service(self):
        #Stops the data fetching thread.
        logging.info("Stopping data service...")
        self.stop_event.set()
        self.thread.join()

    def get_latest_data(self):
        #Returns the most recent data fetched with thread-safe access.
        with self.data_lock:  # Lock while reading shared data
            return self.latest_data


class Client:
    def __init__(self, data_service):
        self.data_service = data_service
        self.stop_event = threading.Event()
        self.thread = None

    def request_weather_update(self):
        #Fetches the latest weather data from the service.
        data = self.data_service.get_latest_data()
        if data:
            logging.info(f"Client received weather data: {data}")
        else:
            logging.info("Client: No data available yet.")

    def start(self, interval):
        #Starts the client in a separate thread.
        self.thread = threading.Thread(target=self._run, args=(interval,))
        self.thread.start()
        logging.info("Client thread started.")

    def _run(self, interval):
        #The thread function for periodically requesting weather updates.
        while not self.stop_event.is_set():
            try:
                self.request_weather_update()
            except Exception as e:
                logging.error(f"Error in client thread: {e}")
            self.stop_event.wait(interval)  # Wait for 'interval' seconds or stop signal

    def stop(self):
        #Stops the client thread.
        logging.info("Stopping client thread...")
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        logging.info("Client thread stopped.")
