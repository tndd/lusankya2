from dataclasses import dataclass


@dataclass
class Asset:
    id_: str
    class_: str
    exchange: str
    symbol: str
    name: str
    status: str
    tradable: bool
    marginable: bool
    maintenance_margin_requirement: int
    shortable: bool
    easy_to_borrow: bool
    fractionable: bool
    attributes: list
