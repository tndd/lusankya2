from os import getenv

HEADER = {
    "APCA-API-KEY-ID": getenv('APCA_KEY_ID'),
    "APCA-API-SECRET-KEY": getenv('APCA_SECRET')
}
