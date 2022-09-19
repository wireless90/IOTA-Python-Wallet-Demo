from __future__ import annotations
from iota_wallet import StrongholdSecretManager, IotaWallet, Account
import requests
import json
from pygments import highlight, lexers, formatters

class ShimmerWallet:
    # region Constants

    DEFAULT_SHIMMER_COIN_TYPE = 4219 #id of shimmer coin type
    DEFAULT_SHIMMER_CLIENT_OPTIONS = {
        'nodes': ['https://api.testnet.shimmer.network'],
    }
    DEFAULT_DATABASE_FILENAME = './my_iota_db'
    DEFAULT_SECRET_FILENAME = 'stronghold'
    DEFAULT_FAUCET_URL = 'https://faucet.testnet.shimmer.network/api/enqueue'
    '''
    {address: "rms1qz9f7vecqscfynnxacyzefwvpza0wz3r0lnnwrc8r7qhx65s5x7rx2fln5q"}
    '''
    # TODO Remove it for production
    DEFAULT_PASSWORD = "password"

    # TODO Remove it for production
    DEFAULT_MNEMONIC = "sail symbol venture people general equal sight pencil slight muscle sausage faculty retreat decorate library all humor metal place mandate cake door disease dwarf"
    #endregion

    # region static methods

    @staticmethod
    def generate_mnemonic() -> str:
        dummy_wallet :IotaWallet = IotaWallet('./mnemonic_generation', coin_type=ShimmerWallet.DEFAULT_SHIMMER_COIN_TYPE, client_options={'offline':True}, secret_manager="Placeholder")
        mnemonic = dummy_wallet.generate_mnemonic()
        return mnemonic
        
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

    @staticmethod
    def pretty_print(input) -> None:
        output_json = json.dumps(input, sort_keys=True, indent=4)
        colored_json = highlight(output_json,lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colored_json)

    #endregion


    def __init__(self, password :str=DEFAULT_PASSWORD):
        self.secret_manager :StrongholdSecretManager = ShimmerWallet._create_secret_manager(ShimmerWallet.DEFAULT_SECRET_FILENAME, password) 
        self.instance = None
        
        if not self._wallet_exists():
            raise Exception("Wallet not found. Create a wallet first.")
    

    def check_balance(self, username:str=None) -> list:
        return self._check_balance_of_all_accounts() if username is None else self._check_balance_of_account(username)
    
    def list_usernames(self) -> list[str]:
        accounts_data = self.instance.get_accounts()
        usernames = [data["alias"] for data in accounts_data]
        return usernames

    def _check_balance_of_account(self, username:str) -> list:
        account:Account = self.instance.get_account(username)
        account.sync_account()
        balance = account.get_balance()
        # ShimmerWallet.pretty_print(balance)
        return [{"username": username, "shimmer": balance["baseCoin"]}]

    def _check_balance_of_all_accounts(self) -> list:
        usernames :list[str]= self.list_usernames()
        response = [self._check_balance_of_account(username)[0] for username in usernames]
        
        return response

            
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