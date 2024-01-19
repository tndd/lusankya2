class ApiQuery:
    """
    APIリクエストにパラメータを渡すための親クラス。
    これを継承することで、自身のフィールドの値を効率的にパラメータへ変換できる。
    """
    def to_params(self) -> dict:
        """
        Noneを除いた自身の要素を辞書化する
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}