from dataclasses import dataclass

from infra.api.value import ApiQuery


def test_api_query():
    """
    ApiQueryの変換メソッドが正常に動作しているかのテスト
    """
    @dataclass
    class TestApiQuery(ApiQuery):
        f1: int = 1
        f2: str = 'a'

    test_api_query = TestApiQuery()
    assert test_api_query.to_params() == {"f1": 1, "f2": "a"}
