import os
import json
import requests
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

MOJANG_API_URL = "https://api.mojang.com/users/profiles/minecraft/"
STEVE_UUID = "8fed65b5c5fa4798b7255baa7bf61b83"

def clear(): os.system("cls" if os.name == "nt" else "clear")
def get_pc_name(): return os.getlogin()
def get_new_minecraft_name(): return input(Fore.WHITE + "\n  [" + Fore.BLUE + "+" + Fore.WHITE + "] Enter the new Minecraft name: " + Fore.LIGHTBLUE_EX)
def get_accounts_file_path(pc_name): return f"C:\\Users\\{pc_name}\\.lunarclient\\settings\\game\\accounts.json"

def load_accounts_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"\n{Fore.LIGHTRED_EX}  Error: Incorrect PC name or path not found.")
        return None

def list_accounts(accounts_data):
    accounts = accounts_data.get('accounts', {})
    print(Fore.WHITE + "\n  [" + Fore.BLUE + "+" + Fore.WHITE + "] Choose one of the following: \n")
    for i, (account_id, info) in enumerate(accounts.items(), start=1):
        print(Fore.WHITE + f"  [{Fore.BLUE}{i}{Fore.WHITE}] {info['minecraftProfile']['name']}")
    print(Fore.WHITE + f"  [{Fore.BLUE}{len(accounts) + 1}{Fore.WHITE}] Add new account")
    return {i: account_id for i, account_id in enumerate(accounts, start=1)}

def select_account_or_add_new(account_choices):
    choice = input(Fore.WHITE + "\n  [" + Fore.BLUE + "+" + Fore.WHITE + "] Select an option or add a new account: " + Fore.LIGHTBLUE_EX)
    is_add_new = choice.isdigit() and (1 <= (choice := int(choice)) <= len(account_choices) + 1)
    return (account_choices.get(choice), choice == len(account_choices) + 1) if is_add_new else (None, False)

def fetch_minecraft_uuid(username):
    response = requests.get(f"{MOJANG_API_URL}{username}")
    if response.status_code == 200:
        return response.json().get('id', STEVE_UUID)
    print(Fore.WHITE + "\n  [" + Fore.RED + "+" + Fore.WHITE + "] " + Fore.LIGHTRED_EX + "This username is not cracked, you will not be able to use it on any cracked servers.")
    return STEVE_UUID

def add_new_account(accounts_data, new_name):
    new_uuid = fetch_minecraft_uuid(new_name)
    accounts_data['accounts'][new_uuid] = {
        "accessToken": "new_uuid", "accessTokenExpiresAt": "3000-01-01T00:00:00.000000000Z",
        "eligibleForMigration": False, "hasMultipleProfiles": False, "legacy": False,
        "persistent": True, "userProperties": [], "localId": new_uuid,
        "minecraftProfile": {"id": new_uuid, "name": new_name}, "remoteId": new_uuid, "type": "Xbox", "username": new_name
    }

def save_accounts_json(file_path, accounts_data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(accounts_data, file, indent=4, ensure_ascii=False)

def main():
    while True:
        clear()
        pc_name = get_pc_name()
        accounts_data = load_accounts_json(get_accounts_file_path(pc_name))
        if accounts_data is None: return

        account_choices = list_accounts(accounts_data)
        if not account_choices: return

        selected_account_id, add_new = None, False
        while selected_account_id is None and not add_new:
            selected_account_id, add_new = select_account_or_add_new(account_choices)

        if add_new:
            new_minecraft_name = get_new_minecraft_name()
            add_new_account(accounts_data, new_minecraft_name)
            save_accounts_json(get_accounts_file_path(pc_name), accounts_data)
            send_confirm(accounts_data, get_accounts_file_path(pc_name))
        else:
            print(f"{Fore.LIGHTRED_EX}  You chose an existing account. Please select the 'change' option if you want to update an existing account.")

        if input(Fore.WHITE + "\n  [" + Fore.BLUE + "+" + Fore.WHITE + "] Do you want to use this code again? (yes/no): " + Fore.LIGHTBLUE_EX).strip().lower() != 'yes':
            break

if __name__ == "__main__":
    os.system(f"title t.me/tools2larp")
    main()