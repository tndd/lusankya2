from domain.dataset.repository.asset import AssetRepository


def get_sector_spdr_fund(rp: AssetRepository):
    name = 'Sector SPDR Fund'
    return rp.fetch_assets_by_name(name)
