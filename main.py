import json
from pygments import highlight, lexers, formatters
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from iota_wallet import StrongholdSecretManager, IotaWallet

##### Constants #####
SHIMMER_COIN_TYPE = 4219 #id of shimmer coin type

SHIMMER_CLIENT_OPTIONS = {
    'nodes': ['https://api.testnet.shimmer.network'],
}
DEFAULT_DATABASE_FILENAME = './my_iota_db'
DEFAULT_SECRET_FILENAME = 'stronghold'

wallet: IotaWallet = None

def pretty_print(input) -> None:
    output_json = json.dumps(input, sort_keys=True, indent=4)
    colored_json = highlight(output_json,lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colored_json)

def create_secret_manager(secret_filename:str, secret_password:str) -> StrongholdSecretManager:
    return StrongholdSecretManager(secret_filename, secret_password)

def create_new_wallet(mnemonic:str, database_filename:str, secret_manager:StrongholdSecretManager, coin_type:int, options:dict) -> IotaWallet:
    wallet :IotaWallet = initialize_wallet(database_filename, secret_manager, coin_type, options)
    wallet.store_mnemonic(mnemonic)
    return wallet

def initialize_wallet(database_filename:str, secret_manager:StrongholdSecretManager, coin_type:int, options:dict) -> IotaWallet :
    wallet :IotaWallet = IotaWallet(database_filename, options, coin_type, secret_manager)
    return wallet

def continue_prompt() -> None:
    input("Press Enter to continue...")

def check_wallet_initialized_status() -> bool:
    global wallet
    if wallet is None:
        print("No wallet found. Create or initialize a wallet first.")
        return False
    
    return True

def handle_create_new_wallet() -> None:

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
    
    global wallet 
    wallet = create_new_wallet(mnemonic, DEFAULT_DATABASE_FILENAME, secret_manager, SHIMMER_COIN_TYPE, SHIMMER_CLIENT_OPTIONS)

def handle_check_balance() -> None:
    if check_wallet_initialized_status() is False:
        return
    
    accounts = wallet.get_accounts()
    
    pretty_print(accounts)

    continue_prompt()

def handle_load_wallet() -> None:
    password = input("Enter password: \n")
    
    secret_manager = create_secret_manager(DEFAULT_SECRET_FILENAME, password)
    
    global wallet
    wallet = initialize_wallet(DEFAULT_DATABASE_FILENAME, secret_manager, SHIMMER_COIN_TYPE, SHIMMER_CLIENT_OPTIONS)

    print("Welcome back! Wallet has been initialized...")

    continue_prompt()


def handle_create_new_account() -> None:
    if check_wallet_initialized_status() is False:
        return
    
    #TODO create alias and create account
    name = input("Enter the username for this account:\n")

    response = wallet.create_account(alias=name)

    pretty_print(response)

    continue_prompt()

    
"""
Creates the Menu to prompt users to run an action.
"""
def create_menu() -> ConsoleMenu:
    MAIN_MENU_TITLE = "SHIMMER WALLET"
    MAIN_MENU_SUBTITLE = "Shimmer is the incentivized testnet for IOTA"
    NEW_WALLET_TITLE = "Create a new Shimmer Wallet."
    INITIALIZE_WALLET_TITLE = "Load an existing Shimmer Wallet"
    CHECK_BALANCE_TITLE = "Check Balance"
    CREATE_ACCOUNT_TITLE = "Create new Account in Shimmer Wallet"

    main_menu = ConsoleMenu(MAIN_MENU_TITLE, MAIN_MENU_SUBTITLE)

    new_wallet_item = FunctionItem(NEW_WALLET_TITLE, handle_create_new_wallet)
    load_wallet_item = FunctionItem(INITIALIZE_WALLET_TITLE, handle_load_wallet)
    balance_item = FunctionItem(CHECK_BALANCE_TITLE, handle_check_balance)
    new_account_item = FunctionItem(CREATE_ACCOUNT_TITLE, handle_create_new_account)

    main_menu.append_item(new_wallet_item)
    main_menu.append_item(load_wallet_item)
    main_menu.append_item(balance_item)
    main_menu.append_item(new_account_item)

    return main_menu
    
def main() -> None:
    main_menu:ConsoleMenu = create_menu()
    main_menu.show()


if __name__ == '__main__':
    main()