
from cmath import log
from models.coin import Coin
from .utility import UtilityService
from crypto_api import get_coins
from typing import List
import logging
import traceback


class TopCoinsServices:
    """
    This service is used to store the 3 top coin from the api 
    in our system
    """
    unsave_coins = []
    coins = get_coins()
    logger = UtilityService.get_logger(__name__)

    @classmethod
    def get_top_three_coins(cls) -> List[dict]:
        # Get top 3 coins
        sorted_coins = sorted(cls.coins, key= lambda k:k['current_price'], reverse=True)
        return sorted_coins[:3] # return top 3 

    @classmethod
    def insert_on_db(cls, coins:List[dict]) -> bool:
        # This function store each on in our db
        for coin in coins:
            try:
                cls.logger.info(f"validating coinf info {coin['symbol']}")
                UtilityService.validator(coin) #valdiate data, TOTAL: Optional 
                Coin.create(coin)
            except Exception as e:
                cls.logger.error(f"error {e},Error line {traceback.format_exc()}")
                cls.unsave_coins.append(coin)
        return True
    

    @classmethod
    def save_top_three_coins_process(cls) -> str:
        # Get top 3 
        coins = cls.get_top_three_coins()
        save_coins =cls.insert_on_db(coins)
        return("process completed")



