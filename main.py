import json
from pygments import highlight, lexers, formatters
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from wallet import ShimmerWallet
from iota_wallet import IotaWallet, Account

wallet: ShimmerWallet = None

def pretty_print(input) -> None:
    output_json = json.dumps(input, sort_keys=True, indent=4)
    colored_json = highlight(output_json,lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colored_json)

def continue_prompt() -> None:
    input("Press Enter to continue...")
    
def check_wallet_initialized_status() -> bool:
    global wallet
    if wallet is None:
        print("No wallet found. Create or initialize a wallet first.")
        return False
    
    return True

def handle_create_new_wallet() -> None:

    mnemonic = input('Enter your 24 word mnemonic. Do write your mnemonic in a paper and store it away safely.\n')
    password = input('Enter a password\n')

    #TODO remove in production
    mnemonic = ShimmerWallet.DEFAULT_MNEMONIC
    
    #TODO remove in production
    password = ShimmerWallet.DEFAULT_PASSWORD

    global wallet 
    wallet = ShimmerWallet.create(mnemonic, password)

    print("\nYour new wallet has been created successfully!\n")
    continue_prompt()


def handle_load_wallet() -> None:
    global wallet
    wallet = None
    password = input("Enter password: \n")
    
    
    try:
        #TODO remove in production
        password = ShimmerWallet.DEFAULT_PASSWORD
        wallet = ShimmerWallet(password)
        print("\nWallet loaded successfully!\n")
    except:
        print("\nError loading wallet... \n\nEither create a new wallet or delete the stronghold file, if present, and create a new wallet with the same mnemonic.\n\n")
        

    continue_prompt()
    


def handle_check_all_balance() -> None:
    if check_wallet_initialized_status() is False:
        return

    response = wallet.check_balance()
    pretty_print(response)
    continue_prompt()

def handle_check_balance() -> None:
    if check_wallet_initialized_status() is False:
        return

    username = input("Enter your account's username:\n")
    response = wallet.check_balance(username)
    pretty_print(response)
    continue_prompt()

def handle_create_new_account() -> None:
    if check_wallet_initialized_status() is False:
        return
    
    username = input("Enter the username for this account:\n")

    instance:IotaWallet = wallet.instance
    response = instance.create_account(alias=username)

    pretty_print(response)
    print("\n\nSuccessfully created new account with username ", username)
    continue_prompt()

def handle_request_shimmer_funds() -> None:
    pass

def handle_generate_mnemonic() -> None:
    ShimmerWallet.generate_mnemonic()
    continue_prompt()


"""
Creates the Menu to prompt users to run an action.
"""
def create_menu() -> ConsoleMenu:
    MAIN_MENU_TITLE = "SHIMMER WALLET"
    MAIN_MENU_SUBTITLE = "Shimmer is the incentivized testnet for IOTA"
    main_menu = ConsoleMenu(MAIN_MENU_TITLE, MAIN_MENU_SUBTITLE)

    GENERATE_MNEMONIC = "Generate new mnemonic"
    NEW_WALLET_TITLE = "Create a new Shimmer Wallet"
    LOAD_WALLET_TITLE = "Load an existing Shimmer Wallet"
    CHECK_ALL_BALANCES_TITLE = "Check All Balances"
    CHECK_BALANCE_TITLE = "Check Balance"
    CREATE_ACCOUNT_TITLE = "Create new Account in Shimmer Wallet"
    REQUEST_SHIMMER_FUNDS = "Request some Shimmer for testing purposes"

    titles_and_handlers = [
        (GENERATE_MNEMONIC, handle_generate_mnemonic),
        (NEW_WALLET_TITLE, handle_create_new_wallet),
        (LOAD_WALLET_TITLE, handle_load_wallet),
        (CREATE_ACCOUNT_TITLE, handle_create_new_account),
        (CHECK_ALL_BALANCES_TITLE, handle_check_all_balance),
        (CHECK_BALANCE_TITLE, handle_check_balance),
        (REQUEST_SHIMMER_FUNDS, handle_request_shimmer_funds),
    ]

    for title_and_handler in titles_and_handlers:
        add_new_item_to_console_menu(main_menu, title_and_handler[0], title_and_handler[1])
    

    return main_menu
def add_new_item_to_console_menu(menu:ConsoleMenu, title:str, handler) -> ConsoleMenu:
    menu_item = FunctionItem(title, handler)
    menu.append_item(menu_item)
    return menu

def main() -> None:
    main_menu:ConsoleMenu = create_menu()
    main_menu.show()


if __name__ == '__main__':
    main()
