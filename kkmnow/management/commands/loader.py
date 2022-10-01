from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import numpy as np
import pandas as pd
from datetime import datetime

from kkmnow.utils import dashboard_builder
from kkmnow.utils import cron_utils
from kkmnow.utils import data_utils

from django.core.cache import cache

from kkmnow.serializers import MetaSerializer, KKMSerializer, HashSerializer
from kkmnow.models import MetaJson, KKMNowJSON, GitHashData

import os
from os import listdir
from os.path import isfile, join
import environ
import json
import requests
import zipfile
from crontab import CronTab
from time import sleep
from apscheduler.schedulers.background import BlockingScheduler

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    def add_arguments(self , parser):
        parser.add_argument('operation' , nargs='+' , type=str, 
        help='States what the operation should be') 
    
    def handle(self, *args, **kwargs):
        event_ids =  kwargs['operation'][0]

        def update() :
            dir_name = 'KKMNOW_SRC'
            zip_name = 'repo.zip'
            git_url = 'https://github.com/MoH-Malaysia/kkmnow-data/archive/main.zip'
            git_token = os.getenv('GITHUB_TOKEN', '-')

            last_commit_hash = cron_utils.get_latest_commit(git_token)
            last_updated_hash = cron_utils.get_latest_hash(last_commit_hash)

            if not last_updated_hash or (last_commit_hash != last_updated_hash) :
                cron_utils.create_directory(dir_name)
                res = cron_utils.fetch_from_git(zip_name, git_url, git_token)
                if 'resp_code' in res and res['resp_code'] == 200 : 
                    cron_utils.write_as_binary(res['file_name'], res['data'])
                    cron_utils.extract_zip(res['file_name'], dir_name)
                    data_utils.rebuild_dashboard_meta('UPDATE')
                    data_utils.rebuild_dashboard_charts('UPDATE')
                    hash_data = GitHashData.objects.get(index='HASH_DATA')
                    hash_data.git_hash = last_commit_hash
                    hash_data.save()
                else : 
                    print("Cant fetch data") # Trigger fail here

        if event_ids == 'cron_update' : 
            update()
            sched = BlockingScheduler()
            sched.add_job(update,'interval', minutes=10)
            sched.start()
        # elif event_ids == 'update' : 
            # Manually update here