from bot.blockchain.bitcoin import BitcoinBlockchain
from bot.blockchain.sbercoin import SbercoinBlockchain
from bot.blockchain.ethereum import EthereumBlockchain
from bot.blockchain.tron import TronBlockchain


choice = {
   'Bitcoin': BitcoinBlockchain(),
   'Sbercoin': SbercoinBlockchain(),
   'Ethereum': EthereumBlockchain(),
   'Tron': TronBlockchain()
}
