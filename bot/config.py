from os import environ


token = environ.get('TOKEN')
db_uri = environ.get('DB_URI')
debug = environ.get('DEBUG') == '1'

sber_explorer_api = "https://explorer.sbercoin.com/api"
sber_explorer_url = "https://explorer.sbercoin.com"

if token is None:
    raise ValueError('Environment variable `TOKEN` was not specified.')

if sber_explorer_api is None:
    raise ValueError('Environment variable `SBER_EXPLORER_API` was not specified.')

if db_uri is None:
    raise ValueError('Environment variable `DB_URI` was not specified.')
