from __future__ import annotations
from unittest.mock import DEFAULT
from iota_wallet import StrongholdSecretManager, IotaWallet, Account

class ShimmerWallet:

    DEFAULT_SHIMMER_COIN_TYPE = 4219 #id of shimmer coin type
    DEFAULT_SHIMMER_CLIENT_OPTIONS = {
        'nodes': ['https://api.testnet.shimmer.network'],
    }
    DEFAULT_DATABASE_FILENAME = './my_iota_db'
    DEFAULT_SECRET_FILENAME = 'stronghold'

    # TODO Remove it for production
    DEFAULT_PASSWORD = "password"

    # TODO Remove it for production
    DEFAULT_MNEMONIC = "flame fever pig forward exact dash body idea link scrub tennis minute surge unaware prosper over waste kitten ceiling human knife arch situate civil"

    """
    Creates a new Shimmer wallet
    """
    @staticmethod
    def create(mnemonic:str=DEFAULT_MNEMONIC, password:str=DEFAULT_PASSWORD) -> ShimmerWallet:
        secret_manager : StrongholdSecretManager = ShimmerWallet._create_secret_manager(ShimmerWallet.DEFAULT_SECRET_FILENAME, password)
        
        wallet_instance :IotaWallet = ShimmerWallet._initialize_wallet(ShimmerWallet.DEFAULT_DATABASE_FILENAME, secret_manager, ShimmerWallet.DEFAULT_SHIMMER_COIN_TYPE, ShimmerWallet.DEFAULT_SHIMMER_CLIENT_OPTIONS)
        wallet_instance.store_mnemonic(mnemonic)
        wallet_instance= None
        secret_manager=None
        return ShimmerWallet(password)
   
    @staticmethod
    def _create_secret_manager(secret_filename:str, secret_password:str) -> StrongholdSecretManager:
        return StrongholdSecretManager(secret_filename, secret_password)

    def __init__(self, password :str=DEFAULT_PASSWORD):
        self.secret_manager :StrongholdSecretManager = ShimmerWallet._create_secret_manager(ShimmerWallet.DEFAULT_SECRET_FILENAME, password) 
        self.instance = None
        
        if not self._wallet_exists():
            raise Exception("Wallet not found. Create a wallet first.")
            
    def _wallet_exists(self) -> bool:
        try:
            self.instance = ShimmerWallet._initialize_wallet(ShimmerWallet.DEFAULT_DATABASE_FILENAME, self.secret_manager, ShimmerWallet.DEFAULT_SHIMMER_COIN_TYPE, ShimmerWallet.DEFAULT_SHIMMER_CLIENT_OPTIONS)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _initialize_wallet(database_filename:str, secret_manager:StrongholdSecretManager, coin_type:int, options:dict) -> IotaWallet :
        wallet :IotaWallet = IotaWallet(database_filename, options, coin_type, secret_manager)
        return wallet