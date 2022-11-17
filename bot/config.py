from os import environ


token = environ.get('TOKEN')
db_uri = environ.get('DB_URI')
debug = environ.get('DEBUG') == '1'
etherscan_api_key = environ.get('ETHERSCAN_API_KEY')

if token is None:
    raise ValueError('Environment variable `TOKEN` was not specified.')

if db_uri is None:
    raise ValueError('Environment variable `DB_URI` was not specified.')
