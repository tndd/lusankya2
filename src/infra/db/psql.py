from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any

from psycopg2 import connect
from psycopg2.extras import DictCursor


@dataclass
class PsqlClient:
    url: str
    n_max_worker: int = 8

    def execute(self, query: str, param: Any = ()) -> Any:
        """
        単発のクエリを実行し、結果を取得する。

        戻り値の型:
            None | List[DictRow]

        Note:
            - 引数はあってもなくてもOK。
            - 結果を返さないタイプのクエリの場合はNoneを返す。

        Memo:
            トランザクション処理が不要な単発での実行が必要なクエリで使うことを想定している。
            例えばSELECT文など単発実行かつ結果がほしい場合など。
        """
        def _f(_cur, query):
            _cur.execute(query, param)
            if _cur.description is not None:
                # 結果を返すクエリの場合
                return _cur.fetchall()
            # 結果を返さないクエリの場合
            return None
        return self._transact(_f, query)

    def execute_queries(self, queries: list):
        """
        クエリとパラメータの複数ペアをトランザクション処理で一気に実行する。
        これはexecuteとは違い、結果を返さない。

        引数のパターン:
            List[str | Tuple[str, Any]]

            1. 単純な文字列のリスト
                テーブルの作成などの引数を伴わないクエリの実行を想定。
            2. (str, Any)のタプルのリスト
                insertやselectなどの引数を伴う複雑なクエリの実行を想定。

        引数の形式について
            - 渡す引数の形式は単純なリストあるいはタプルリストいずれかの純粋な形でなければならない。
            - もし両方の形式を同時に渡したいのであれば、呼び出し側でタプルリストの方に統一すること。

        Memo:
            型注釈をList[str | Tuple[str, Any]]と書くと警告文が出まくる。
            どうやっても解消法が見つからないので、不本意だがlistとゆるい型になった。
        """
        def _f(_cur, queries_with_params):
            for query, params in queries_with_params:
                _cur.execute(query, params)

        # 引数の要素が単純なstrであった場合、要素を空のタプルリストに変換する
        queries = [(q, ()) if isinstance(q, str) else q for q in queries]
        # 実行
        self._transact(_f, queries)

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
        並列でexecutemanyを高速に実行する。

        Note:
            あまりに投入データが大量でパフォーマンス上の問題が起こった場合、
            executemanyの代わりにこちらを使用する。
        """
        n_process = self._calc_optimum_process_num(data)
        with ProcessPoolExecutor(max_workers=n_process) as executor:
            for i in range(n_process):
                chunk = data[i::n_process]
                executor.submit(self.executemany, query, chunk)

    ### Utils ###
    def is_test_mode(self) -> bool:
        """
        テストモードかどうかを判定する。
        削除などの危険な操作を行う際に使用されることが想定される。
        """
        return self.url.endswith("_test")

    ### Private Methods
    def _transact(self, f, *args, **kwargs):
        """
        トランザクション処理のラッパー関数。
        """
        conn = connect(self.url)
        cur = conn.cursor(cursor_factory=DictCursor)
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