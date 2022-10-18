from database import db_session, init_db
from services.top_coins_service import TopCoinsServices
from services.trade_coin_service import TradeCoinService
from dotenv import find_dotenv, load_dotenv
import os

import crypto_api

load_dotenv(find_dotenv(raise_error_if_not_found=True))

# You can access the environment variables as such, and any variables from the .env file will be loaded in for you to use.
# os.getenv("DB_HOST")

# Start Here

if __name__ =="__main__":
    init_db() # init db
    TopCoinsServices.save_top_three_coins_process() # Store top 3 coins
    TradeCoinService.compare_place_coins_price_process() # buy and log coins
 
 
     