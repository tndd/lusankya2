from datetime import datetime

from domain.dataset.model.bar import Bar


def test_bar_from_json():
    """
    bodyの要素Barsの１要素が変換できていることを確認
    """
    data = {
        "c": 141.15,
        "h": 142.075,
        "l": 139.55,
        "n": 6395,
        "o": 139.63,
        "t": "2024-02-20T05:00:00Z",
        "v": 485786,
        "vw": 140.9291
    }
    bar = Bar.from_json(data)
    # 時間がきちんとpythonに則った形に変換されているかを確認(Z => +00:00)
    assert bar.ts == datetime.fromisoformat("2024-02-20T05:00:00+00:00")
    assert bar.open == 139.63
