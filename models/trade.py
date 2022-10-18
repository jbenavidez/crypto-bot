from services.utility import UtilityService
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from  database import Base
from database import db_session
import logging
import traceback
logger =  UtilityService.get_logger(__name__)
 

class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer , primary_key=True)
    #coin = relationship('coin', foreign_keys='coin.user_id')\ # uncomment if relationship is required
    coin_id = Column(String,  nullable = True)
    coin_symbol = Column(String,  nullable = True)
    quantity = Column(Float)
    cost = Column(Float)
    avg_cost = Column(Float)

    @classmethod
    def get_all_coins(cls) -> dict:
        # this function get all coin in our db
        coin_list = cls.query.all()
        temp = []
        # for item in coin_list:
        #     temp.append(cls.entity_to_obj(item))
        return temp

    @classmethod
    def create(cls, trade_info:dict) -> dict:
        # this function save trade record in our db
        coin_id = trade_info['id']
        logger.info(f"{coin_id}: saving trade info")
        try:
            entry = cls(
                    coin_id = coin_id,
                    coin_symbol = trade_info['symbol'],
                    quantity = trade_info['quantity'],
                    cost = trade_info['order_info'],
                    avg_cost = trade_info['avg_price'],
                    )
            db_session.add(entry)
            db_session.commit()
            logging.info(f"{coin_id}:trade info was saved.")
        except Exception as e:
            logger.error(f"trade could not be store. Error {e}, Error line {traceback.format_exc()}")
            db_session.rollback()
        return trade_info