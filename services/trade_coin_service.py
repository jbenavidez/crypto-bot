import statistics
import concurrent.futures 
from numpy import average
from models.trade import Trade
from services.utility import  UtilityService
from crypto_api import get_coins, get_coin_price_history , submit_order
from typing import Any, List
import traceback


class TradeCoinService:
    """
    This service is used to cal av for each coin and 
    submit order if requirements are meet
    """
    coins = get_coins()
    logger = UtilityService.get_logger(__name__)
    
    @classmethod
    def cal_avg_price(cls, coin_obj: dict) -> Any:
        # This function calculate the avg prices 
        try:
            coin_id = coin_obj['id']
            cls.logger.info(f"calculate_avg_price {coin_id}")
            current_price = coin_obj['current_price']
            coin_history = get_coin_price_history(coin_id)
            coins_price = [x[1] for x in coin_history]
            avg_price =  statistics.mean(coins_price)
            coin_obj = {
                        "id":coin_id,
                        "symbol":coin_obj['symbol'],
                        "current_price":current_price,
                        "is_valid_to_buy": False,
                        "avg_price":avg_price
                        }
            # check if place order is needed
            cls.logger.info(f"Checking price for {coin_id}")
            if current_price < avg_price:
                tem_gain  = avg_price - current_price
                cls.logger.info(f"Possible_gain ${round(tem_gain,3)} if we buy {coin_id}")
                coin_obj["is_valid_to_buy"] = True
            return coin_obj
        except Exception as e:
            # this could fail because for some reason the bit coin API was faling, maybe too many call
            cls.logger.error(f"trade could not be store. Error {e}, Error line {traceback.format_exc()}")
            return 


    @classmethod
    def place_order(cls, coin: dict) -> dict:
        # this is used to place orde
        try:
            coin_id = coin["id"]
            cls.logger.info("placing order")
            order = submit_order(coin["id"], 1, coin['current_price'])
            coin["order_info"] = order # add trade info
            coin["quantity"] = 1 # add quentity
            cls.logger.info(f"order was place for {coin_id}")
        except Exception as e:
            cls.logger.error(f"Placing order {coin_id} failed. Error {e} , Error line {traceback.format_exc()}")
        return coin
         
    @classmethod
    def compare_place_coins_price_process(cls) -> str:
        with  concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(cls.cal_avg_price, cls.coins)
            for item in result: # access to event loop
                if item is not None: # # I added 'is not None' condition because the coins api was failing, maybe too many calls
                    if item.get("is_valid_to_buy"):
                        # place order 
                        order = cls.place_order(item)
                        # save record in our db
                        Trade.create(order)

        # create log file 

        return("process completed") 
