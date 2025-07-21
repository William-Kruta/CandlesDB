import sqlite3
import pandas as pd


class Database:
    def __init__(
        self, db_path: str, table_name: str = "daily_candles", log: bool = True
    ):
        self.db_path = db_path
        self.table_name = table_name
        self.log = log
        self.conn = None

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _create_table(self):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            date DATE,
            symbol TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def _insert_data(self, df: pd.DataFrame):
        if self.conn is None:
            self._connect()

        data_tuples = []
        for row in df.itertuples(index=False):
            # row_list = list(row)
            # row_list[0] = row_list[0].isoformat()
            # data_tuples.append(tuple(row_list))
            data_tuples.append(
                tuple(x.isoformat() if isinstance(x, pd.Timestamp) else x for x in row)
            )
        cols = df.columns.to_list()
        cols = [c.lower() for c in cols]
        col_holder = ", ".join(["?"] * len(cols))
        # col_holder = "?, " * len(cols)
        # col_holder = col_holder[:-2]
        print(f"Cols: {cols} Holder: {col_holder}")
        query = f"INSERT OR IGNORE INTO {self.table_name} ({', '.join(cols)}) VALUES ({col_holder});"
        # data_tuples = [tuple(x[1:]) for x in df.reset_index().to_numpy()]
        # print(f"Data: {data_tuples}")
        try:
            self.cursor.executemany(query, data_tuples)
            self.conn.commit()
        except sqlite3.OperationalError:
            self._create_table()
            self.cursor.executemany(query, data_tuples)
            self.conn.commit()
        if self.log:
            print(f"\n{self.cursor.rowcount} new records were added.")

    def read_candles_single(self, ticker: str, limit: int = -1):
        if self.conn is None:
            self._connect()
        if limit == -1:
            query = f"SELECT * FROM {self.table_name} WHERE symbol = '{ticker.upper()}'"
            df = pd.read_sql_query(query, self.conn)
        else:
            query = f"""
                SELECT *
                FROM {self.table_name}
                WHERE symbol = ?
                ORDER BY date DESC  
                LIMIT ?             
            """
            df = pd.read_sql_query(query, self.conn, params=(ticker, limit))
        return df

    def read_candles_multi(self, tickers: list, limit: int = -1):
        if self.conn is None:
            self._connect()
        if isinstance(tickers, str):
            tickers = [tickers]
        if limit == -1:
            placeholders = ", ".join(["?"] * len(tickers))
            sql = f"SELECT * FROM {self.table_name} WHERE symbol IN ({placeholders});"
            df_results = pd.read_sql_query(sql, self.conn, params=tickers)
        else:
            data = []
            for t in tickers:
                df = self.read_candles_single(t, limit)
                data.append(df)
            df_results = pd.concat(data, axis=0)
        return df_results

    def delete_record(self, ticker: str, date: str = ""):
        if self.conn is None:
            self._connect()

        if date != "" and "T" not in date:
            date += "T00:00:00"
        if date == "":
            query = f"DELETE FROM {self.table_name} WHERE symbol = ?"
            self.cursor.execute(query, (ticker,))
        else:
            # Use a parameterized query to prevent SQL injection
            query = f"DELETE FROM {self.table_name} WHERE symbol = ? AND date = ?"
            self.cursor.execute(query, (ticker, date))

        self.conn.commit()  # Commit the changes
        print(f"Record deleted successfully for symbol '{ticker}' and date '{date}'.")

    def _get_latest_record(self, ticker: str, column: str = "date"):
        if self.conn is None:
            self._connect()
        query = f"""
            SELECT *
            FROM {self.table_name}
            WHERE symbol = ?
            ORDER BY {column} DESC
            LIMIT 1
        """
        try:
            df = pd.read_sql_query(query, self.conn, params=[ticker])
        except pd.errors.DatabaseError:
            self._create_table()
            df = pd.read_sql_query(query, self.conn, params=[ticker])
        return df


# def _read_single_ticker(self, ticker: str):
