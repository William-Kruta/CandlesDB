import yfinance as yf


def download(ticker, period: str = "max", interval: str = "1d"):
    allowed_max = ["1d", "5d"]
    col_order = ["date", "symbol", "open", "high", "low", "close", "volume"]
    if interval.lower() not in allowed_max and period.lower() == "max":
        period = "5d"
    if isinstance(ticker, str):
        # Multiple tickers passed in a single string, seperated by commas.
        if "," in ticker:
            ticker = ticker.split(",")
            ticker = _clean_tickers(ticker)
            df = yf.download(
                ticker, period=period, interval=interval, multi_level_index=True
            )
            df = (
                df.stack(level=1, future_stack=True)
                .reset_index()
                .rename(columns={"level_1": "symbol"})
            )
        else:
            # Single ticker passed
            ticker = _clean_tickers(ticker)
            df = yf.download(
                ticker, period=period, interval=interval, multi_level_index=False
            )
            df["symbol"] = ticker
    elif isinstance(ticker, list):
        ticker = _clean_tickers(ticker)

        if len(ticker) == 1:
            df = yf.download(
                ticker, period=period, interval=interval, multi_level_index=False
            )
            df["symbol"] = ticker[0]
        else:
            df = yf.download(
                ticker, period=period, interval=interval, multi_level_index=True
            )
            df = (
                df.stack(level=1, future_stack=True)
                .reset_index()
                .rename(columns={"level_1": "symbol"})
            )

    if "Adj Close" in df.columns:
        df = df.drop("Adj Close", axis=1)
    df.columns = [c.lower() for c in df.columns]
    if "ticker" in df.columns:
        df = df.rename({"ticker": "symbol"}, axis=1)
    df = df[col_order]
    return df


def _clean_tickers(tickers):
    if isinstance(tickers, str):
        tickers = [tickers]
    new_tickers = [t.replace(".", "-") for t in tickers]
    new_tickers = [t.replace("/", "-") for t in new_tickers]
    new_tickers = [t.strip() for t in new_tickers]
    # new_tickers = [t for t in new_tickers if t not in INVALID_TICKERS]
    if len(new_tickers) == 1:
        return new_tickers[0]
    return new_tickers
