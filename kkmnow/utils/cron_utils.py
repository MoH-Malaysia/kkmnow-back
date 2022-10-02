import os
from os import listdir
from os.path import isfile, join
from kkmnow.models import MetaJson, KKMNowJSON, GitHashData
from kkmnow.utils import triggers
from kkmnow.utils import data_utils
import requests
import zipfile

def create_directory(dir_name) :
    try: 
        os.mkdir(os.path.join(os.getcwd(), dir_name)) # KKMNOW_SRC
    except OSError as error: 
        print("Directory already exists, no need to create")

def fetch_from_git(zip_name, git_url, git_token) :
    file_name = os.path.join(os.getcwd(), zip_name)
    headers = {
        'Authorization': f'token {git_token}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    res = {}
    res['file_name'] = file_name
    res['data'] = requests.get(git_url, headers=headers)
    res['resp_code'] = res['data'].status_code
    return res

def write_as_binary(file_name, data) :
    try : 
        with open(file_name, 'wb') as f:
            f.write(data.content)
    except : 
        triggers.send_telegram("!! FILE ISSUES WRITING TO BINARY !!")

def extract_zip(file_name, dir_name) :
    try : 
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(os.getcwd(), dir_name))
    except : 
        triggers.send_telegram("!! ZIP FILE EXTRACTION ISSUE !!")

def get_latest_commit(git_token) : 
    url = "https://api.github.com/repos/MoH-Malaysia/kkmnow-data/commits/main"
    git_token = os.getenv('GITHUB_TOKEN', '-')
    headers = {
        'Authorization': f'token {git_token}',
        'Accept': 'application/vnd.github.VERSION.sha'
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200 : 
        return str(res.content, 'UTF-8')
    else :
        triggers.send_telegram("!! GIT FAILED TO PULL !!")

def get_latest_hash(latest_commit_hash) : 
    last_updated_hash = GitHashData.objects.last()
    if not last_updated_hash : 
        GitHashData.objects.create(git_hash = latest_commit_hash)

    return last_updated_hash if not last_updated_hash else last_updated_hash.git_hash


def update() :
    dir_name = 'KKMNOW_SRC'
    zip_name = 'repo.zip'
    git_url = 'https://github.com/MoH-Malaysia/kkmnow-data/archive/main.zip'
    git_token = os.getenv('GITHUB_TOKEN', '-')
    triggers.send_telegram("Checking for any updates...")

    last_commit_hash = get_latest_commit(git_token)
    last_updated_hash = get_latest_hash(last_commit_hash)

    if not last_updated_hash or (last_commit_hash != last_updated_hash) :
        create_directory(dir_name)
        res = fetch_from_git(zip_name, git_url, git_token)
        if 'resp_code' in res and res['resp_code'] == 200 : 
            write_as_binary(res['file_name'], res['data'])
            extract_zip(res['file_name'], dir_name)
            data_utils.rebuild_dashboard_meta('UPDATE')
            data_utils.rebuild_dashboard_charts('UPDATE')
            hash_data = GitHashData.objects.get(index='HASH_DATA')
            hash_data.git_hash = last_commit_hash
            hash_data.save()
        else : 
            print("Cant fetch data") # Trigger fail here
    else : 
        print("Git Hash remains same")