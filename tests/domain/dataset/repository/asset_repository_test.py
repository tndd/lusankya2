from typing import List


def test_fetch_assets(asset_repository):
    """
    アセットの取得が出来ているか
    """
    assets = asset_repository.fetch_assets()
    assert isinstance(assets, List)

def test_fetch_assets_by_name(asset_repository):
    """
    名前での絞り込み
    """
    assets = asset_repository.fetch_assets('iShares Core Total USD Bond Market ET')
    assert isinstance(assets, List)
    assert len(assets) == 1


def test_fetch_assets_ishares_core(asset_repository):
    """
    "iShares Core"の件数が合わないため調査
    """
    assets = asset_repository.fetch_assets(
        keyword='iShares Core',
        tradable=True,
        shortable=None
    )
    assert len(assets) == 26
