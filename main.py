from audioop import add
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

    wallet_menu :ConsoleMenu = create_wallet_menu()
    wallet_menu.show()
    


def handle_check_all_balance() -> None:
    if check_wallet_initialized_status() is False:
        return

    response = wallet.check_balance()
    pretty_print(response)
    continue_prompt()

def handle_check_balance() -> None:
    if check_wallet_initialized_status() is False:
        return

    response = wallet.check_balance(wallet.active_user)
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
    wallet.request_funds()
    print("\nShimmer has been requested. Give it a few seconds to be added to your account.\n\n")
    continue_prompt()

def handle_generate_mnemonic() -> None:
    mnemonic:str = ShimmerWallet.generate_mnemonic()
    pretty_print(mnemonic)
    print("\n\nCopy the mnemonic down. It wont be shown again.\n\n")
    continue_prompt()

def handle_list_usernames() -> None:
    usernames:list[str] = wallet.list_usernames()
    pretty_print(usernames)
    continue_prompt()

def handle_switch_account() -> None:
    username = input("Enter the username to switch to:\n")
    wallet.active_user = username

    account_menu :ConsoleMenu = create_account_menu()
    account_menu.show()

def handle_create_receive_address() -> None:
    address:str = wallet.get_a_receive_address()
    print("You address have been generated!\n\n")
    pretty_print(address)
    continue_prompt()

def handle_send_shimmer() -> None:
    amount:str = input("Enter amount to send:\n")
    address:str = input("Enter a receiving address to send to:\n")
    wallet.send_shimmer(amount, address)

    print("{0} glow has been sent successfully to address {1}.\n", amount, address)

"""
Creates the Menu to prompt users to run an action.
"""
def create_menu() -> ConsoleMenu:
    MAIN_MENU_TITLE = "SHIMMER Main Menu"
    MAIN_MENU_SUBTITLE = "Shimmer is the incentivized testnet for IOTA"
    main_menu = ConsoleMenu(MAIN_MENU_TITLE, MAIN_MENU_SUBTITLE)
    
    # Main
    GENERATE_MNEMONIC = "Generate new mnemonic"
    NEW_WALLET_TITLE = "Create a new Shimmer Wallet"
    LOAD_WALLET_TITLE = "Load an existing Shimmer Wallet"

    titles_and_handlers = [
        (GENERATE_MNEMONIC, handle_generate_mnemonic),
        (NEW_WALLET_TITLE, handle_create_new_wallet),
        (LOAD_WALLET_TITLE, handle_load_wallet),
    ]

    for title_and_handler in titles_and_handlers:
        add_new_item_to_console_menu(main_menu, title_and_handler[0], title_and_handler[1])
    

    return main_menu

def create_wallet_menu() -> ConsoleMenu:
    
    WALLET_MENU_TITLE = "SHIMMER WALLET"
    WALLET_MENU_SUBTITLE = "Access your wallet features here"
    wallet_menu = ConsoleMenu(WALLET_MENU_TITLE, WALLET_MENU_SUBTITLE)

    CREATE_ACCOUNT_TITLE = "Create new Account in Shimmer Wallet"
    LIST_USERNAMES = "List all usernames of accounts"
    CHECK_ALL_BALANCES_TITLE = "Check All Balances"
    SWITCH_TO_USER = "Switch to a user account"

    titles_and_handlers = [
        (CREATE_ACCOUNT_TITLE, handle_create_new_account),
        (CHECK_ALL_BALANCES_TITLE, handle_check_all_balance),
        (LIST_USERNAMES, handle_list_usernames),
        (SWITCH_TO_USER, handle_switch_account),
    ]

    for title_and_handler in titles_and_handlers:
        add_new_item_to_console_menu(wallet_menu, title_and_handler[0], title_and_handler[1])

    return wallet_menu

def create_account_menu() -> ConsoleMenu:
    WALLET_MENU_TITLE = "SHIMMER ACCOUNT"
    WALLET_MENU_SUBTITLE = "User: " + wallet.active_user

    # Accout
    CHECK_BALANCE_TITLE = "Check Balance"
    REQUEST_SHIMMER_FUNDS = "Request some Shimmer for testing purposes"
    CREATE_RECEIVE_ADDRESS = "Create a receive address"
    SEND_SHIMMER = "Send shimmer to another address"

    account_menu :ConsoleMenu = ConsoleMenu(WALLET_MENU_TITLE, WALLET_MENU_SUBTITLE)

    titles_and_handlers = [
        (CHECK_BALANCE_TITLE, handle_check_balance),
        (REQUEST_SHIMMER_FUNDS, handle_request_shimmer_funds),
        (CREATE_RECEIVE_ADDRESS, handle_create_receive_address),
        (SEND_SHIMMER, handle_send_shimmer),
    ]

    for title_and_handler in titles_and_handlers:
        add_new_item_to_console_menu(account_menu, title_and_handler[0], title_and_handler[1])
    
    return account_menu

def add_new_item_to_console_menu(menu:ConsoleMenu, title:str, handler) -> ConsoleMenu:
    menu_item = FunctionItem(title, handler)
    menu.append_item(menu_item)
    return menu

def main() -> None:
    main_menu:ConsoleMenu = create_menu()
    main_menu.show()


if __name__ == '__main__':
    main()
