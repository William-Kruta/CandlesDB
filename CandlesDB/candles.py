import sqlite3
import pandas as pd

import yfinance as yf


from .web import download
from .database import Database
from .utils import is_stale

period_mapping = {
    "1d": 1,
    "5d": 5,
    "1mo": 22,
    "6mo": 144,
    "1y": 252,
}


class CandlesDB:
    def __init__(self, db_path: str):
        self.db = Database(db_path)

    def get_candles(
        self, tickers, period: str = "max", interval: str = "1d", limit: int = -1
    ):
        if isinstance(tickers, str):
            tickers = [tickers]
        tickers_state = self._determine_ticker_state(tickers)
        data = []
        if len(tickers_state["fresh"]) > 0:
            fresh_df = download(tickers_state["fresh"], period="max", interval="1d")
            data.append(fresh_df)
        if len(tickers_state["stale"]) > 0:
            stale_df = download(tickers_state["stale"], period="1mo", interval="1d")
            data.append(stale_df)

        if len(data) > 0:
            data_to_update = pd.concat(data, axis=0)
            self.db._insert_data(data_to_update)

        candles = self.db.read_candles_multi(tickers, limit)
        t = candles["symbol"].to_list()

        print(f"Candles: {candles}")

    def _determine_ticker_state(self, tickers):

        state = {"fresh": [], "stale": [], "valid": []}

        for t in tickers:
            record = self.db._get_latest_record(t)
            if record.empty:
                state["fresh"].append(t)
            else:
                date = record["date"].values[0]
                if "T" in date:
                    date = date.split("T")[0]

                stale = is_stale(date, 3)
                if stale:
                    state["stale"].append(t)
                else:
                    state["valid"].append(t)

        return state


###################################################################################################################################


if __name__ == "__main__":

    c = CandlesDB("data.db")

    tickers = ["RKLB", "ASTS", "RDW", "MSFT"]
    Candle = CandlesDB("test")
    Candle.get_candles(tickers, limit=30)
    # candles = Candle.get_candles(tickers)
    # print(f"DF: {candles}")
