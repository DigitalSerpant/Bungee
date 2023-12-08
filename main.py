import os
import requests
import time
import signal
import sys
import logging

url = 'https://57qnmp-25565.csb.app/'
restart_urls = ["https://codesb.lowlifeserver.repl.co/",
                "https://keepon.boody1234.repl.co/", "https://alwyson2.susdadyy.repl.co/"]

# Set up logging
logging.basicConfig(level=logging.INFO)


def restart_server():
    try:
        logging.info("Restarting server...")
        os.system('pkill java')
        os.system('pkill tmux')
        time.sleep(1)
        os.system(
            'tmux new -d -s bungee java -Xmx1999M -Xms1999M -jar bungee-dist.jar')
        time.sleep(4)
    except Exception as e:
        logging.error(f"Error in restart_server: {e}")


def shutdown(signal, frame):
    try:
        logging.info("Received shutdown signal, stopping...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error in shutdown: {e}")


# Register signal handlers
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

while True:
    try:
        response = requests.get(url, verify=True, timeout=60)

        for restart_url in restart_urls:
            try:
                requests.get(restart_url)
            except requests.exceptions.RequestException as re:
                logging.error(f"Error requesting {restart_url}: {re}")

        if '404 WebSocket Upgrade Failure' in response.text:
            logging.info('Success')
        else:
            restart_server()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error in main loop: {e}")
        print("CRASHED... RESTARTING")
        restart_server()
