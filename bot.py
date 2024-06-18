import os
import sys
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime
from colorama import *
from urllib.parse import unquote

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
putih = Fore.LIGHTWHITE_EX

class Data:
    def __init__(self, init_data, userid, username, secret):
        self.init_data = init_data
        self.userid = userid
        self.username = username
        self.secret = secret

class PixelTod:
    def __init__(self):
        self.DEFAULT_COUNTDOWN = 180 * 60  # 5 minutes
        self.INTERVAL_DELAY = 0  # seconds
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,en-US;q=0.9",
            "Host": "api-clicker.pixelverse.xyz",
            "X-Requested-With": "org.telegram.messenger",
            'origin': 'https://sexyzbot.pxlvrs.io/',
            'referer': 'https://sexyzbot.pxlvrs.io/',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

    def get_secret(self, userid):
        rawr = "adwawdasfajfklasjglrejnoierjboivrevioreboidwa"
        secret = hmac.new(rawr.encode("utf-8"), str(userid).encode("utf-8"), hashlib.sha256).hexdigest()
        return secret

    def data_parsing(self, data):
        return {key: value for key, value in (i.split('=') for i in unquote(data).split('&'))}

    def main(self):
        banner = f"""
        {hijau}AUTO CLAIM PIXELTAP BY {biru}PIXELVERSE

        {putih}Original Source by : {hijau}t.me/AkasakaID
        {putih}Recoded by : {hijau}t.me/naufal48
        {hijau}Github : {putih}@AkasakaID | {putih}@NaufalJCT48 
        {kuning}Need Daily Combo ID ? {biru}https://github.com/naufaljct48/pixelverse?tab=readme-ov-file#pet-list
        """
        if "noclear" not in sys.argv:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)

        with open("initdata.txt", "r") as file:
            datas = file.read().splitlines()

        self.log(f'{hijau}Account Detected : {len(datas)}')
        if not datas:
            self.log(f'{kuning}Please fill / input your data to initdata.txt')
            sys.exit()


        auto_buy_pet = input("Auto Buy Pet? (y/n): ").strip().lower() == 'y'
        auto_upgrade_pet = input("Auto Upgrade Pet? (y/n): ").strip().lower() == 'y'
        daily_combo = input("Daily Combo? (y/n): ").strip().lower() == 'y'
        id_pets = []

        if daily_combo:
            id_pets = input("Input ID Pet Daily Combo: (ex: 0a6306e5-cc33-401a-9664-a872e3eb2b71,78e0146f-0dfb-4af8-a48d-4033d3efdd39,8074e9c5-f6c2-4012-bfa2-bcc98ceb5175,dc5236dc-06be-456b-a311-cccedbd213ca)\n").strip().split(',')

        print('~' * 50)
        while True:
            for no, data in enumerate(datas):
                self.log(f'{hijau}Account Number : {putih}{no + 1}')
                data_parse = self.data_parsing(data)
                user = json.loads(data_parse['user'])
                userid = str(user['id'])
                first_name = user.get('first_name')
                last_name = user.get('last_name')
                username = user.get('username')

                self.log(f'{hijau}Login as : {putih}{first_name} {last_name}')
                secret = self.get_secret(userid)
                new_data = Data(data, userid, username, secret)
                self.process_account(new_data, auto_buy_pet, auto_upgrade_pet, daily_combo, id_pets)
                print('~' * 50)
                self.countdown(self.INTERVAL_DELAY)
            self.countdown(self.DEFAULT_COUNTDOWN)

    def process_account(self, data, auto_buy_pet, auto_upgrade_pet, daily_combo, id_pets):
        self.get_me(data)
        self.daily_reward(data)
        self.get_mining_proccess(data)
        if auto_buy_pet:
            self.auto_buy_pet(data)
        if auto_upgrade_pet:
            self.auto_upgrade_pet(data)
        if daily_combo:
            self.daily_combo(data, id_pets)

    def countdown(self, t):
        while t:
            jam, sisa = divmod(t, 3600)
            menit, detik = divmod(sisa, 60)
            print(f"{putih}Waiting until {jam:02}:{menit:02}:{detik:02} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def api_call(self, url, data=None, headers=None, method='GET'):
        while True:
            try:
                if method == 'GET':
                    res = requests.get(url, headers=headers)
                elif method == 'POST':
                    res = requests.post(url, headers=headers, data=data)
                else:
                    raise ValueError(f'Unsupported method: {method}')
                
                if res.status_code == 401:
                    self.log(f'{merah}{res.text}')

                open('.http.log', 'a', encoding='utf-8').write(f'{res.text}\n')
                return res
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout):
                self.log(f'{merah}Connection error / connection timeout !')
                continue

    def get_me(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/users'
        headers = self.prepare_headers(data)
        res = self.api_call(url, None, headers)
        
        if not res.text:
            self.log(f'{merah}Empty response from get_me API.')
            return
        
        try:
            response_json = res.json()
            balance = response_json.get('clicksCount', 'N/A')
            self.log(f'{hijau}Total Balance : {putih}{balance}')
        except json.JSONDecodeError:
            self.log(f'{merah}Failed to decode JSON response from get_me API. Response: {res.text}')

    def daily_reward(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/daily-rewards'
        headers = self.prepare_headers(data)
        res = self.api_call(url, None, headers)
        
        if not res.text:
            self.log(f'{merah}Empty response from daily reward API.')
            return

        try:
            response_json = res.json()
        except json.JSONDecodeError:
            self.log(f'{merah}Failed to decode JSON response from daily reward API. Response: {res.text}')
            return
        
        if response_json.get('todaysRewardAvailable'):
            url_claim = 'https://api-clicker.pixelverse.xyz/api/daily-rewards/claim'
            res = self.api_call(url_claim, '', headers, method='POST')
            
            if not res.text:
                self.log(f'{merah}Empty response from daily reward claim API.')
                return
            
            try:
                claim_response = res.json()
                amount = claim_response.get('amount', 'N/A')
                self.log(f'{hijau}Success claim today reward : {putih}{amount}')
            except json.JSONDecodeError:
                self.log(f'{merah}Failed to decode JSON response from daily reward claim API. Response: {res.text}')
        else:
            self.log(f'{kuning}Already claim today reward !')

    def get_mining_proccess(self, data: Data):
        url = "https://api-clicker.pixelverse.xyz/api/mining/progress"
        headers = self.prepare_headers(data)
        res = self.api_call(url, None, headers)
        
        if not res.text:
            self.log(f'{merah}Empty response from mining progress API.')
            return

        try:
            response_json = res.json()
        except json.JSONDecodeError:
            self.log(f'{merah}Failed to decode JSON response from mining progress API. Response: {res.text}')
            return
        
        available = response_json.get('currentlyAvailable', 0)
        min_claim = response_json.get('minAmountForClaim', float('inf'))
        self.log(f'{putih}Amount available : {hijau}{available}')
        
        if available > min_claim:
            url_claim = 'https://api-clicker.pixelverse.xyz/api/mining/claim'
            res = self.api_call(url_claim, '', headers, method='POST')
            
            if not res.text:
                self.log(f'{merah}Empty response from claim API.')
                return
            
            try:
                claim_response = res.json()
                claim_amount = claim_response.get('claimedAmount', 'N/A')
                self.log(f'{hijau}Claim amount : {putih}{claim_amount}')
            except json.JSONDecodeError:
                self.log(f'{merah}Failed to decode JSON response from claim API. Response: {res.text}')
        else:
            self.log(f'{kuning}Amount too small to make claim !')

    def auto_buy_pet(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/pets/buy?tg-id={self.tg_id}&secret={self.secret}'
        headers = self.prepare_headers(data)
        res_buy_pet = self.api_call(url, data=json.dumps({}), headers=headers, method='POST')
        if res_buy_pet.status_code == 200 or res_buy_pet.status_code == 201:
            try:
                buy_pet_data = res_buy_pet.json()
                pet_name = buy_pet_data.get('pet', {}).get('name', 'Unknown')
                self.log(f'{hijau}Successfully buy a new pet! You got {kuning}{pet_name}!')
            except json.JSONDecodeError:
                self.log(f'{merah}Failed to decode JSON response from buy pet API.')
        else:
            self.log(f'{merah}Not yet time to buy another pet or Insufficient points')


    def auto_upgrade_pet(self, data: Data):
        url = 'https://api-clicker.pixelverse.xyz/api/pets'
        headers = self.prepare_headers(data)
        res = self.api_call(url, None, headers)
        pets = res.json().get('data', [])
        if pets:
            pets_info = ', '.join([f'{pet["name"].strip()} Lv.{pet["userPet"]["level"]}' for pet in pets])
            self.log(f'{hijau}Success Getting Pet List: {pets_info}')
            for pet in pets:
                pet_name = pet["name"].strip()
                pet_level = pet["userPet"]["level"]
                pet_id = pet['userPet']['id']
                self.log(f'{putih}Selecting Pet ID: {hijau}{pet_id} ({pet_name} Lv.{pet_level})')
                url_upgrade = f'https://api-clicker.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up'
                res_upgrade = self.api_call(url_upgrade, '', headers, method='POST')
                if res_upgrade.status_code == 200 or res_upgrade.status_code == 201:
                    self.log(f'{hijau}Success Upgrading Pet! Pet ID: {putih}{pet_id} ({pet_name})')
                else:
                    error_message = res_upgrade.json().get('message', 'Unknown error')
                    self.log(f'{merah}Failed to Upgrade Pet! Pet ID: {putih}{pet_id}, {merah}Error: {error_message}')
        else:
            self.log(f'{kuning}No Pets Available for Upgrade')

    def daily_combo(self, data: Data, id_pets):
        url_current_game = "https://api-clicker.pixelverse.xyz/api/cypher-games/current"
        headers = self.prepare_headers(data)
        res_current_game = self.api_call(url_current_game, None, headers)
        
        if res_current_game.status_code == 200 and res_current_game.text:
            try:
                game_data = res_current_game.json()
            except json.JSONDecodeError:
                self.log(f'{merah}Failed to decode JSON response from current game API.')
                return

            if game_data['status'] == "ACTIVE":
                game_id = game_data.get('id')
                available_options = game_data.get('options', [])
                pet_id_index_map = {option["optionId"]: len(available_options) - option["order"] - 1 for option in available_options}

                id_pets = [pet_id.strip() for pet_id in id_pets]
                payload = {pet_id: len(id_pets) - id_pets.index(pet_id) - 1 for pet_id in id_pets}

                url_answer = f"https://api-clicker.pixelverse.xyz/api/cypher-games/{game_id}/answer"
                headers['Content-Type'] = 'application/json'
                res_answer = self.api_call(url_answer, data=json.dumps(payload), headers=headers, method='POST')

                if res_answer.status_code == 200 or res_answer.status_code == 201:
                    try:
                        answer_data = res_answer.json()
                        reward_amount = answer_data.get('rewardAmount', 'N/A')
                        self.log(f'{hijau}Successfully submitted the daily combo! Reward Amount: {reward_amount}')
                    except json.JSONDecodeError:
                        self.log(f'{merah}Failed to decode JSON response from answer API.')
                else:
                    self.log(f'{merah}Failed to submit the daily combo. {res_answer.text}')
            else:
                self.log(f'{kuning}Daily Combo already claimed!')
        else:
            self.log(f'{merah}Daily Combo Already Claimed!')

    def prepare_headers(self, data: Data):
        headers = self.base_headers.copy()
        headers.update({
            'initData': data.init_data,
            'secret': data.secret,
            'tg-id': data.userid
        })
        if data.username:
            headers['username'] = data.username
        return headers

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

if __name__ == "__main__":
    try:
        app = PixelTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
