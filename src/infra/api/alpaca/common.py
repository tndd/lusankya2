from os import getenv

APCA_HEADER = {
    "APCA-API-KEY-ID": getenv('APCA_KEY_ID'),
    "APCA-API-SECRET-KEY": getenv('APCA_SECRET')
}


APCA_ENDPOINT = {
    'bar': 'https://data.alpaca.markets/v2/stocks/{symbol}/bars',
    'quote': 'https://data.alpaca.markets/v2/stocks/{symbol}/quotes'
}
