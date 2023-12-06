from dataclasses import dataclass
import requests
import logging
import time

logger = logging.getLogger('advent_of_code')

@dataclass
class Secrets:
    aoc_session_token = str
    
    def __init__(self) -> None:
        self.aoc_session_token = get_secret("aoc_session_token").get('password')


def get_secret(bw_name):
    logger.debug(f'Get secret {bw_name}')
    try:
        requests.post("http://127.0.0.1:8087/sync")
        secret_details = requests.get(f'http://127.0.0.1:8087/object/item/{bw_name}')
        if secret_details.status_code == 200 and secret_details.json().get("success"):
            secret_details_json = secret_details.json()
            uname = secret_details_json["data"]["login"]["username"]
            pw = secret_details_json["data"]["login"]["password"]
            uname_password = {"username": uname, "password":pw}
            return uname_password
        else:
            logger.error(f"Not successful getting secret {bw_name} - {secret_details}")
    except Exception as e:
        logger.error(f"Error getting secret {bw_name} - {e}")
