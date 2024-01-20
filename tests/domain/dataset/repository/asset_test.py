from typing import List

import pytest

from domain.dataset.repository.asset import AssetRepository


@pytest.fixture
def asset_repo():
    return AssetRepository()

def test_fetch_assets(asset_repo):
    assets = asset_repo.fetch_assets()
    assert isinstance(assets, List)

def test_fetch_asset_by_name(asset_repo):
    assets = asset_repo.fetch_assets_by_name('iShares Core')
    assert isinstance(assets, List)
    assert len(assets) == 31


if __name__ == "__main__":
    """
    "iShares Core"の件数が合わないため調査
    """
    rp = AssetRepository()
    assets = rp.fetch_assets_by_name('iShares Core')
    for asset in assets:
        print(asset.name)
