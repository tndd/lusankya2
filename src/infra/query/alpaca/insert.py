def insert_bar() -> str:
    return """
    INSERT INTO alpaca.bar (
        time_stamp,
        time_frame,
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
        %(t)s,
        %(time_frame)s,
        %(symbol)s,
        %(o)s,
        %(h)s,
        %(l)s,
        %(c)s,
        %(n)s,
        %(v)s,
        %(vw)s
    );
    """
