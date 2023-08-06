from colorama import init, Fore
from cryptography.fernet import Fernet

init(autoreset=True)
key_path = 'key.txt'

def generate_new_key():
    """Generate a new encryption key"""
    key = Fernet.generate_key()
    key = bytearray(key)
    key = key.decode()
    print(f'\nEncryption key:{Fore.LIGHTYELLOW_EX+(key)}\n')
    save_key_to_file(key)

def save_key_to_file(key):
    """Save generated key to file"""
    while True:
        save_file = input("Save key to file? This will erase any existed key!"
                          "(y/n)\t")
        if save_file.lower() == 'y':
            with open(key_path,'w') as key_object:
                key_object.write(key)
                print(f'\nThe encryption key has been saved to '
                      f'{Fore.LIGHTYELLOW_EX+key_path}\n')
                break
        elif save_file.lower() == 'n':
            break
        else:
            print(Fore.LIGHTRED_EX+'Please enter a valid option!\n')
            continue

def get_key():
    """Read key from file"""
    with open(key_path,'r') as key_object:
        key = key_object.read()
        return key

def enter_key():
    """Input key from user"""
    key = input('Enter encryption key:')
    return key

