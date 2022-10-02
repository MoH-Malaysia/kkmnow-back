import os
from os import listdir
from os.path import isfile, join
from kkmnow.models import MetaJson, KKMNowJSON, GitHashData
from kkmnow.utils import triggers
from kkmnow.utils import data_utils
import requests
import zipfile

'''
Creates a directory
'''
def create_directory(dir_name) :
    try: 
        os.mkdir(os.path.join(os.getcwd(), dir_name)) # KKMNOW_SRC
    except OSError as error: 
        print("Directory already exists, no need to create")

'''
Fetches entire content from a git repo
'''
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

'''
Writes content as binary
'''
def write_as_binary(file_name, data) :
    try : 
        with open(file_name, 'wb') as f:
            f.write(data.content)
    except : 
        triggers.send_telegram("!! FILE ISSUES WRITING TO BINARY !!")

'''
Extracts zip file into desired directory
'''
def extract_zip(file_name, dir_name) :
    try : 
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(os.getcwd(), dir_name))
    except : 
        triggers.send_telegram("!! ZIP FILE EXTRACTION ISSUE !!")

'''
Performs data operations,
such as update or rebuild
'''
def data_operation(operation) :
    dir_name = 'KKMNOW_SRC'
    zip_name = 'repo.zip'
    git_url = 'https://github.com/MoH-Malaysia/kkmnow-data/archive/main.zip'
    git_token = os.getenv('GITHUB_TOKEN', '-')

    triggers.send_telegram("--- PERFORMING " + operation + " ---")

    create_directory(dir_name)
    res = fetch_from_git(zip_name, git_url, git_token)
    if 'resp_code' in res and res['resp_code'] == 200 : 
        write_as_binary(res['file_name'], res['data'])
        extract_zip(res['file_name'], dir_name)
        data_utils.rebuild_dashboard_meta(operation)
        data_utils.rebuild_dashboard_charts(operation)
    else : 
        triggers.send_telegram("FAILED TO GET DATA FROM")