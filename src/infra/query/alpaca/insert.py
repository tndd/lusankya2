def get_query_insert_bar() -> str:
    return """
    INSERT INTO alpaca.bar (
        time_stamp,
        timeframe,
        symbol,
        open,
        high,
        low,
        close,
        trade_count,
        volume,
        vwap
    )
    VALUES (
        %(time_stamp)s,
        %(timeframe)s,
        %(symbol)s,
        %(open)s,
        %(high)s,
        %(low)s,
        %(close)s,
        %(trade_count)s,
        %(volume)s,
        %(vwap)s
    );
    """
