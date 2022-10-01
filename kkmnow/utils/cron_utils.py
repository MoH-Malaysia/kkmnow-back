import os
from os import listdir
from os.path import isfile, join
import requests
import zipfile

def create_directory(dir_name) :
    try: 
        os.mkdir(os.path.join(os.getcwd(), dir_name)) # KKMNOW_SRC
    except OSError as error: 
        print("Directory already exists, no need to create")

def fetch_from_git(zip_name, git_directory, git_token) :
    file_name = os.path.join(os.getcwd(), zip_name)
    url = 'https://github.com/MoH-Malaysia/kkmnow-data/archive/main.zip'
    git_token = os.getenv('GITHUB_TOKEN', '...')
    headers = {
        'Authorization': f'token {git_token}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    res = {}
    res['file_name'] = file_name
    res['data'] = requests.get(url, headers=headers)
    return res

def write_as_binary(file_name, data) :
    with open(file_name, 'wb') as f:
        f.write(data.content)

def extract_zip(file_name, dir_name) :
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd(), dir_name))