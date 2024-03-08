from typing import Optional


def get_query_select_bar(
        start: Optional[str],
        end: Optional[str]
    ) -> str:
    """
    barデータを取得するためのクエリ。
    startやendの指定があった場合、動的にクエリを生成する。
    """
    # 必須部分のクエリ
    query = """
        SELECT * FROM alpaca.bar
        WHERE symbol = %(symbol)s
        AND timeframe = %(timeframe)s
        AND adjustment = %(adjustment)s
    """
    # startやendの指定がある場合、WHERE句を追加
    if start:
        query += f" AND time_stamp >= '{start}'"
    if end:
        query += f" AND time_stamp <= '{end}'"
    query += ';'
    return query
