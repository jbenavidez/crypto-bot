from typing import Any
from validators.coin_schema import CoinValidator
from datetime import datetime, timedelta
import logging, secrets, json
import sys



class UtilityService:

    @staticmethod
    def validator(data:dict)-> dict:
        if isinstance(data, dict):
            record = CoinValidator(**data)
        else:
            record = CoinValidator(**data.dict())
        return data
        
    @staticmethod
    def get_logger(name) -> Any:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        file_handler = logging.FileHandler('storage/logs/app.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
        return logger