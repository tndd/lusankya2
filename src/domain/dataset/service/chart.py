def move_chart_data_from_broker_to_dataset():
    """
    databroker内に存在する未移動のchartデータをdatasetに移動する。

    工程:
        1. databrokerから対象かつ未移動のchartデータを取得
        2. 各データをapi生形式からdatasetの形式に変換
        3. datasetに保存
        4. 移動済みのdatabroker内のbodyデータを削除する
    """
    # TODO: 実装
    pass
