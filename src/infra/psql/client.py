from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any, List, Tuple

from psycopg2 import connect


@dataclass
class PsqlClient:
    url: str
    n_max_worker: int = 8

    def execute(self, query: str, params: Any = ()) -> Any:
        """
        単発のクエリを実行し、結果を取得する。

        Note:
            - 引数はあってもなくてもOK。
            - 結果を返さないタイプのクエリの場合はNoneを返す。

        Memo:
            トランザクション処理が不要な単発での実行が必要なクエリで使うことを想定している。
            例えばSELECT文など単発実行かつ結果がほしい場合など。
        """
        def _f(_cur, query):
            _cur.execute(query, params)
            if _cur.description is not None:
                # 結果を返すクエリの場合
                return _cur.fetchall()
            # 結果を返さないクエリの場合
            return None
        return self._transact(_f, query)


    def execute_queries(self, queries_with_params: List[Tuple[str, Any]]):
        """
        クエリとパラメータの複数ペアをトランザクション処理で一気に実行する。
        これはexecuteとは違い、結果を返さない。

        Note:
            1. パラメータを渡す必要がないクエリの場合は空のタプル()を渡すようにすること。
            2. パラメータはdictあるいはtupleとして渡す。

        Memo:
            クエリのみの場合、空のパラメータを渡すという運用方法が正しいのかは分からない。
            だが似たような関数を乱立させるというのも違う気がするので、
            この程度の複雑度であれば統合したほうが良いと判断した。
        """
        def _f(_cur, queries_with_params):
            for query, params in queries_with_params:
                _cur.execute(query, params)
        self._transact(_f, queries_with_params)


    def executemany(self, query: str, data: list):
        """
        単発のexecutemanyを実行。
        """
        def _f(_cur, query, data):
            _cur.executemany(query, data)
        self._transact(_f, query, data)


    ### Parallel Execution
    def parallel_executemany(self, query: str, data: list):
        """
        大量のデータによるexecutemanyを並列実行で高速に実行する。
        """
        n_process = self._calc_optimum_process_num(data)
        with ProcessPoolExecutor(max_workers=n_process) as executor:
            for i in range(n_process):
                chunk = data[i::n_process]
                executor.submit(self.executemany, query, chunk)


    ### Private Methods
    def _transact(self, f, *args, **kwargs):
        """
        トランザクション処理のラッパー関数。
        """
        conn = connect(self.url)
        cur = conn.cursor()
        try:
            result = f(cur, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()


    def _calc_optimum_process_num(self, tasks: list) -> int:
        """
        実行に最適なプロセス数を計算する。
        """
        return min(len(tasks), self.n_max_worker)