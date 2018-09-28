from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer, DateTime,Text
from datetime import datetime, timedelta
Base = declarative_base()


class Marquee(Base):
    __tablename__ = "marquee"
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id = Column(Integer, primary_key=True)
    paly_name = Column(String(128), doc=u"玩家姓名")
    money = Column(Integer, doc=u"金额")


class MarTimeCount(Base):
    __tablename__ = "martimecount"
    id = Column(Integer, primary_key=True)
    time = Column(String(128), doc="时间")
    count = Column(Integer, doc="数量")


class MarNameMoney(Base):
    __tablename__ = "marnamemoney"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), doc="姓名")
    small_money = Column(Integer, doc="money")
    max_money = Column(Integer, doc="money")


class ShiShiCai(Base):
    __tablename__ = "shishicai"
    id = Column(Integer, primary_key=True)
    UpdateTime = Column(String(32))
    PlanData = Column(Text())
    status = Column(Integer)  # 状态 0 关闭 1开启
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)