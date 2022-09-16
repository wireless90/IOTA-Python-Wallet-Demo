from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem


"""
Creates the Menu to prompt users to run an action.
"""
def create_menu() -> ConsoleMenu:
    MAIN_MENU_TITLE = "SHIMMER WALLET"
    MAIN_MENU_SUBTITLE = "Shimmer is the incentivized testnet for IOTA"
    NEW_ACCOUNT_TITLE = "Create a new Shimmer Account"

    main_menu = ConsoleMenu(MAIN_MENU_TITLE, MAIN_MENU_SUBTITLE)

    new_account_item = FunctionItem(NEW_ACCOUNT_TITLE, lambda : ())

    main_menu.append_item(new_account_item)

    return main_menu

def main() -> None:
    main_menu:ConsoleMenu = create_menu()
    main_menu.show()


if __name__ == '__main__':
    main()