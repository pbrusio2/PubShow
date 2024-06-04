"""
This module monitors temperature using a DHT22 sensor and alerts via Webex if the temperature is out of the desired range.
"""

from board import D4
import adafruit_dht
import time
import requests
import logging

# Configuration
SENSOR_PIN = D4
WEBEX_URL = "https://webexapis.com/v1/messages"
WEBEX_ROOM_ID = "Your Room ID Here"
WEBEX_AUTH_KEY = "Bearer Your Auth Key Here"
TEMP_RANGE = (18, 25)
SLEEP_DURATION = 30

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize the sensor
d = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)

def post_message_to_webex(message):
    """
    Posts a message to a Webex room.
    """
    payload = {
        "roomId": WEBEX_ROOM_ID,
        "text": message
    }
    headers = {
        'Authorization': WEBEX_AUTH_KEY,
        'Content-Type': 'application/json',
    }
    response = requests.post(WEBEX_URL, json=payload, headers=headers)
    logging.info(response.text)

def check_temperature():
    """
    Checks the temperature and posts to Webex if it's out of the defined range.
    """
    try:
        d.measure()
        temp = d.temperature
        logging.info(f'Got temperature: {temp}')

        if TEMP_RANGE[0] <= temp <= TEMP_RANGE[1]:
            logging.info("Lab Temp is within normal range")
        else:
            logging.info("Lab Temp outside normal range")
            post_message_to_webex("Lab Temp outside normal range")

    except RuntimeError as e:
        logging.error(f'Failed to get temperature: {e}')

    time.sleep(SLEEP_DURATION)

def main():
    """
    Continuously checks the temperature at set intervals.
    """
    while True:
        check_temperature()

if __name__ == "__main__":
    main()
