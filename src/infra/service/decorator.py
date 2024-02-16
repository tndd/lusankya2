from functools import wraps
from infra.db.psql import PsqlClient


def test_only(f):
    """
    関数をテストモード時のみ実行可能にするデコレータ
    """
    @wraps(f)
    def wrapper(db_cli: PsqlClient, *args, **kwargs):
        if not db_cli.is_test_mode():
            raise ValueError("この関数はテストモード時のみ実行可能です。")
        return f(db_cli, *args, **kwargs)
    return wrapper