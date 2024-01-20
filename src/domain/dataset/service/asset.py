from typing import List

from domain.dataset.model.asset import Asset
from domain.dataset.repository.asset import AssetRepository


def get_sector_spdr_fund(rp: AssetRepository) -> List[Asset]:
    """
    ステートストリートのセクターETF一覧を取得する
    """
    name = 'Sector SPDR Fund'
    return rp.fetch_assets_by_name(name)
