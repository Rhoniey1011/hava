import requests
import json
import os
import urllib.parse
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class HavaCoin:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'tma.havacoin.xyz',
            'Origin': 'https://tma.havacoin.xyz',
            'Pragma': 'no-cache',
            'Referer': 'https://tma.havacoin.xyz/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Hava Coin - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            user = user_data['first_name']
            return user
        else:
            raise ValueError("User data not found in query.")
        
    def user_info(self, query: str):
        url = 'https://tma.havacoin.xyz/api/miniapp/user/info'
        self.headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json',
            'Content-Length': '0'
        })

        response = self.session.post(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if result:
            return result['user']
        else:
            return None
        
    def claim_tapping(self, query: str):
        url = 'https://tma.havacoin.xyz/api/miniapp/tapping/claim'
        self.headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json',
            'Content-Length': '0'
        })

        response = self.session.post(url, headers=self.headers)
        result = response.json()
        if result:
            return result
        else:
            return None
        
    def complete_tasks(self, query: str, task_name: str):
        url = f'https://tma.havacoin.xyz/api/miniapp/tasks/{task_name}'
        self.headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json',
            'Content-Length': '0'
        })

        response = self.session.post(url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        if result:
            return result
        else:
            return None
    
    def process_query(self, query: str):

        name = self.load_data(query)
        user = self.user_info(query)

        if user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {name} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['balance']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}Bones ]{Style.RESET_ALL}"
            )

            available_tap = user['tapping']['available']
            if available_tap >= 100:
                claim = self.claim_tapping(query)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {claim['reward']['balance']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}Bones ]{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Balance Now{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {claim['user']['balance']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}Bones ] [ Available Tap{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {claim['user']['tapping']['available']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} is Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Reached Maximum Limit {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

            skip_tasks = ['frens_1', 'frens_5']
            tasks = user['tasks']['available']
            for task_key, task_details in tasks.items():
                if task_key in skip_tasks:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {task_details['title']} {Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT}Skipped{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                    continue
                task_name = task_key
                if task_name:
                    complete_tasks = self.complete_tasks(query, task_name)
                    if complete_tasks:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task_details['title']} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task_details['reward']} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task_details['title']} {Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Failed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(f"{Fore.YELLOW+Style.BRIGHT}[ No available task to complete ]{Style.RESET_ALL}")

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                seconds = 5
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Hava Coin - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    havacoin = HavaCoin()
    havacoin.main()