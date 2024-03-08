import json
import os
from typing import List, Optional

from domain.dataset.model.asset import Asset


class AssetRepository:
    """
    本来はAPI経由でAsset情報を取得する必要があるが、
    現在はテスト用にローカルファイルから取得する仮実装形式をとる。
    """

    def fetch_assets(
        self,
        keyword: Optional[str] = None,
        tradable: Optional[bool] = True,
        shortable: Optional[bool] = None
    ) -> List[Asset]:
        """
        全てのAsset情報を取得

        Note:
            - 絞り込み条件はAND形式
        """
        assets = [self.from_data(d) for d in self._fetch_raw_assets()]
        if keyword:
            # keywordに部分一致するAsset情報を絞り込み
            assets = [a for a in assets if keyword in a.name]
        if tradable is not None:
            # 取引可能なAsset情報を絞り込み
            assets = [a for a in assets if a.tradable == tradable]
        if shortable is not None:
            # 空売り可能なAsset情報を絞り込み
            assets = [a for a in assets if a.shortable == shortable]
        return assets

    def _fetch_raw_assets(self) -> dict:
        """
        全てのAsset情報をdictの生形式で取得する
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, '../data/asset.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data


    @staticmethod
    def from_data(data: dict) -> 'Asset':
        """
        dict形式のAsset情報をAssetモデルに変換
        """
        return Asset(
            id_=data['id'],
            class_=data['class'],
            exchange=data['exchange'],
            symbol=data['symbol'],
            name=data['name'],
            status=data['status'],
            tradable=data['tradable'],
            marginable=data['marginable'],
            maintenance_margin_requirement=data['maintenance_margin_requirement'],
            shortable=data['shortable'],
            easy_to_borrow=data['easy_to_borrow'],
            fractionable=data['fractionable'],
            attributes=data['attributes']
        )
