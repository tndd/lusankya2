CREATE TABLE IF NOT EXISTS alpaca.bar (
    time_stamp TIMESTAMP WITH TIME ZONE NOT NULL,
    time_frame TEXT NOT NULL,
    symbol TEXT NOT NULL,
    adjustment TEXT NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    trade_count BIGINT,
    volume BIGINT,
    vwap DOUBLE PRECISION,
    PRIMARY KEY(time_stamp, time_frame, symbol, adjustment)
);

SELECT create_hypertable('alpaca.bar', 'time_stamp', if_not_exists => TRUE);