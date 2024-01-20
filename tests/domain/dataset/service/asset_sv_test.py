from domain.dataset.repository.asset import AssetRepository
from domain.dataset.service.asset import get_sector_spdr_fund


def test_get_sector_spdr_fund():
    rp = AssetRepository()
    result = get_sector_spdr_fund(rp)
    assert len(result) == 11
