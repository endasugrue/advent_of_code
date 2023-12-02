from dataclasses import dataclass
import requests
import logging
import time

logger = logging.getLogger('advent_of_code')

@dataclass
class Secrets:
    aoc_session_token = str
    
    def __init__(self) -> None:
        self.aoc_session_token = "<SESSION TOKEN FROM ADVENT OF CODE WEBSITE COOKIES>"

