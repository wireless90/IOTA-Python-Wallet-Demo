from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from iota_wallet import StrongholdSecretManager, IotaWallet

##### Constants #####
SHIMMER_COIN_TYPE = 4219 #id of shimmer coin type

SHIMMER_CLIENT_OPTIONS = {
    'nodes': ['https://api.testnet.shimmer.network'],
}

wallet: IotaWallet = None

def create_secret_manager(secret_filename:str, secret_password:str) -> StrongholdSecretManager:
    return StrongholdSecretManager(secret_filename, secret_password)

def create_new_wallet(mnemonic:str, database_filename:str, secret_manager:StrongholdSecretManager, coin_type:int, options:dict) -> IotaWallet:
    wallet :IotaWallet = IotaWallet(database_filename, options, coin_type, secret_manager)
    wallet.store_mnemonic(mnemonic)
    return wallet

def handle_create_new_wallet() -> IotaWallet:
    DEFAULT_DATABASE_FILENAME = './my_iota_db'
    DEFAULT_SECRET_FILENAME = 'stronghold'

    # TODO Remove it for production
    DEFAULT_PASSWORD = "password"

    # TODO Remove it for production
    DEFAULT_MNEMONIC = "flame fever pig forward exact dash body idea link scrub tennis minute \
        surge unaware prosper over waste kitten ceiling human knife arch situate civil"

    mnemonic = input('Enter your 24 word mnemonic. Do write your mnemonic in a paper and store it away safely.\n')
    password = input('Enter a password\n')

    mnemonic = DEFAULT_MNEMONIC
    password = DEFAULT_PASSWORD

    secret_manager :StrongholdSecretManager = create_secret_manager(DEFAULT_SECRET_FILENAME, password)
    
    wallet :IotaWallet = create_new_wallet(mnemonic, DEFAULT_DATABASE_FILENAME, secret_manager, SHIMMER_COIN_TYPE, SHIMMER_CLIENT_OPTIONS)

    return wallet
"""
Creates the Menu to prompt users to run an action.
"""
def create_menu() -> ConsoleMenu:
    MAIN_MENU_TITLE = "SHIMMER WALLET"
    MAIN_MENU_SUBTITLE = "Shimmer is the incentivized testnet for IOTA"
    NEW_WALLET_TITLE = "Create a new Shimmer Wallet."

    main_menu = ConsoleMenu(MAIN_MENU_TITLE, MAIN_MENU_SUBTITLE)

    new_wallet_item = FunctionItem(NEW_WALLET_TITLE, handle_create_new_wallet)

    main_menu.append_item(new_wallet_item)

    return main_menu
    
def main() -> None:
    main_menu:ConsoleMenu = create_menu()
    main_menu.show()


if __name__ == '__main__':
    main()