from services.utility import UtilityService
from sqlalchemy import Column, Integer, String, DateTime, Float
from  database import Base
from database import db_session
import traceback

logger =  UtilityService.get_logger(__name__)
 

class Coin(Base):
    __tablename__ = 'coin'
    id = Column(Integer , primary_key=True)
    name = Column(String(120), unique=True)
    symbol = Column(String,  nullable = True)
    current_price = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    # last_updated = Column(DateTime)
    # atl_date = Column(DateTime)

    @classmethod
    def get_all_coins(cls) -> dict:
        # this function get all coin in our db
        coin_list = cls.query.all()
        temp = []
        for item in coin_list:
            temp.append(cls.entity_to_obj(item))
        return temp


    @classmethod
    def create(cls, coin_info:dict) -> dict:
        # this function save coin in our db
        coin_name = coin_info['name']
        # Check is coin exist: 
        coin_checker = cls.get_coin_by_symbol(coin_info['symbol'])
        if coin_checker is not None:
            logger.info(f"coin already exist {coin_name}")
            return coin_info
        
        try:
            logger.info(f"saving coin {coin_name}...")
            entry = cls(
                    name = coin_name,
                    symbol = coin_info['symbol'],
                    current_price = coin_info['current_price'],
                    high_24h = coin_info['high_24h'],
                    low_24h = coin_info['low_24h'],
                    # last_updated = coin_info['last_updated'],
                    # atl_date = coin_info['atl_date'],
                    )
            db_session.add(entry)
            db_session.commit()
            logger.info(f"coin {coin_name}  was saved.")
        except Exception as e:
            logger.error(f"coin could not be store {coin_name}. Error {e} .traceback: {traceback.format_exc()}")
            db_session.rollback()
        return coin_info

    @classmethod
    def get_coin_by_pk(cls, pk) -> dict:
        # get coin by pk
        coin = cls.query.filter(cls.id == pk).first()
        return cls.entity_to_obj(coin)


    @classmethod
    def get_coin_by_symbol(cls, symbol: str) -> dict:
        # get coin by symbol
        coin = cls.query.filter(cls.symbol == symbol).first()
        return coin

    @classmethod
    def entity_to_obj(cls, coin_entity) -> dict:
        """
        Im aware that we could use a serializer or use pydantic to do this, but i like to use this method just in case 
        if we can to do something else with the data before we send it do the user
        """
        result = {
                "id": coin_entity.id,
                "name": coin_entity.name,
                "symbol": coin_entity.symbol,
                "current_price": coin_entity.current_price,
                "high_24h": coin_entity.high_24h,
                "low_24h": coin_entity.low_24h,
                }
        return result