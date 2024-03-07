from domain.dataset.model.bar import Adjustment, Bar, Chart, Timeframe


def factory_chart() -> Chart:
    bar_data = [
        {"c": 141.15, "h": 142.075, "l": 139.55, "n": 6395, "o": 139.63, "t": "2024-02-20T05:00:00Z", "v": 485786, "vw": 140.9291},
        {"c": 142.54, "h": 142.68, "l": 140.7, "n": 5835, "o": 141.37, "t": "2024-02-21T05:00:00Z", "v": 386976, "vw": 141.990892},
        {"c": 144.02, "h": 145, "l": 142.8, "n": 6183, "o": 144.96, "t": "2024-02-22T05:00:00Z", "v": 538093, "vw": 143.926125}
    ]
    return Chart(
        symbol='AAPL',
        timeframe=Timeframe.DAY,
        adjustment=Adjustment.RAW,
        bars=[Bar.from_json(data) for data in bar_data]
    )
