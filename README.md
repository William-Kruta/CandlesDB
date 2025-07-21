# CandlesDB

CandlesDB is a Python library designed to efficiently download, store, and query financial OHLCV (Open, High, Low, Close, Volume) candle data. It uses yfinance to fetch data from Yahoo Finance and stores it in a local SQLite database for fast and persistent access.

The library is intelligent about data fetching: it only downloads new data for tickers it hasn't seen before and incrementally updates tickers whose data is stale, minimizing redundant API calls.

Key Features
Automated Data Fetching: Downloads historical stock data for any ticker available on Yahoo Finance.

Efficient Local Caching: Stores data in a local SQLite database, making subsequent queries instantaneous.

Intelligent Updates: Automatically detects if a ticker's data is missing or out-of-date and only fetches the necessary updates.

Simple API: A clean and simple interface to retrieve candle data for single or multiple tickers.

Pandas Integration: Returns data as a pandas.DataFrame for easy analysis and manipulation.

---

### Installation

To use this library in another project, it is recommended to install it in editable mode from a cloned repository.

Clone the repository:

git clone <https://github.com/William-Kruta/CandlesDB.git>
cd CandlesDB

---

### Create and activate a virtual environment (recommended):

python -m venv venv

# On Windows

venv\Scripts\activate

# On macOS/Linux

source venv/bin/activate

---

### Install the library:

The -e flag installs the package in "editable" mode, meaning any changes you make in the source code will be immediately available in your project.

pip install -e .

This will also automatically install dependencies like pandas and yfinance.

Quickstart Guide
Using CandlesDB is straightforward. Instantiate the main class with a path to your database file and call the get_candles method.

from CandlesDB import CandlesDB

# 1. Initialize the database.

# This will create 'my_stock_data.db' if it doesn't exist.

db = CandlesDB("my_stock_data.db")

# 2. Define the tickers you want to query.

tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]

# 3. Get the candle data.

# The library will automatically download and cache any missing data.

# The 'limit' parameter retrieves the last N candles for each ticker.

candle_df = db.get_candles(tickers, limit=90)

# The result is a pandas DataFrame ready for analysis.

print(candle_df)

How it Works
When you call get_candles():

State Check: The library checks the database to see if each ticker's data is present and up-to-date.

Fetch Fresh Data: For tickers never seen before, it performs a full historical download.

Update Stale Data: For tickers with outdated data, it fetches only the most recent candles to fill the gap.

Retrieve from DB: It queries the local database to return the requested data as a single DataFrame.

Dependencies
pandas

yfinance

These will be installed automatically when you run pip install -e ..

License
This project is licensed under the MIT License. See the LICENSE file for details.
