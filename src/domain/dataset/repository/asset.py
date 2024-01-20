import json
import os
from typing import List

from domain.dataset.model.asset import Asset


def to_asset(data: dict) -> Asset:
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


class AssetRepository:
    """
    本来はAPI経由でAsset情報を取得する必要があるが、
    現在はテスト用にローカルファイルから取得する仮実装形式をとる。
    """

    def fetch_assets(self, tradable: bool = True) -> List[Asset]:
        """
        全てのAsset情報を取得
        """
        if tradable:
            return [to_asset(d) for d in self._fetch_raw_assets() if d['tradable']]
        return [to_asset(d) for d in self._fetch_raw_assets()]

    def fetch_assets_by_name(self, name: str) -> List[Asset]:
        """
        nameに部分一致するAsset情報を取得
        """
        assets = self.fetch_assets()
        return [a for a in assets if name in a.name]

    def _fetch_raw_assets(self) -> dict:
        """
        全てのAsset情報をdictの生形式で取得する
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, '../data/asset.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
