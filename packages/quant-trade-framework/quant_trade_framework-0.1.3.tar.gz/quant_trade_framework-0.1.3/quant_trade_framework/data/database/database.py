from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from quant_trade_framework.core import Interval, Exchange  # noqa
    from quant_trade_framework.core.object import BarData, TickData  # noqa


class Driver(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"


class BaseDatabaseManager(ABC):

    @abstractmethod
    def load_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval",
        start: datetime,
        end: datetime
    ) -> Sequence["BarData"]:
        pass

    @abstractmethod
    def load_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
        start: datetime,
        end: datetime
    ) -> Sequence["TickData"]:
        pass

    @abstractmethod
    def save_bar_data(
        self,
        symbol,
        datas: Sequence["BarData"],
        interval: str
    ):
        pass

    @abstractmethod
    def save_tick_data(
        self,
        symbol,
        datas: Sequence["TickData"],
        interval: str
    ):
        pass

    @abstractmethod
    def get_newest_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval"
    ) -> Optional["BarData"]:
        """
        If there is data in database, return the one with greatest datetime(newest one)
        otherwise, return None
        """
        pass

    @abstractmethod
    def get_newest_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
    ) -> Optional["TickData"]:
        """
        If there is data in database, return the one with greatest datetime(newest one)
        otherwise, return None
        """
        pass

    @abstractmethod
    def clean(self, symbol: str):
        """
        delete all records for a symbol
        """
        pass
