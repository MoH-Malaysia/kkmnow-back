from django.core.management.base import BaseCommand, CommandError

import numpy as np
import pandas as pd
from datetime import datetime

from kkmnow.utils import dashboard_builder
from kkmnow.utils import cron_utils

from django.core.cache import cache

from kkmnow.serializers import MetaSerializer, KKMSerializer
from kkmnow.models import MetaJson, KKMNowJSON

import os
import environ
import json
from os import listdir
from os.path import isfile, join
import requests
import zipfile

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Delete all

        dir_name = 'KKMNOW_SRC'
        zip_name = 'repo.zip'
        git_directory = 'https://github.com/MoH-Malaysia/kkmnow-data/archive/main.zip'
        git_token = os.getenv('GITHUB_TOKEN', '...')

        cron_utils.create_directory(dir_name)
        res = cron_utils.fetch_from_git(zip_name, git_directory, git_token)
        print(res)
        cron_utils.write_as_binary(res['file_name'], res['data'])
        cron_utils.extract_zip(res['file_name'], dir_name)

        # KKMNowJSON.objects.all().delete()
        # MetaJson.objects.all().delete()
        # META_DIR = os.path.dirname(os.path.realpath(__file__)) + '/META_JSON/'
        # meta_files = [f for f in listdir(META_DIR) if isfile(join(META_DIR, f))]

        # for meta in meta_files : 
        #     f_meta = META_DIR + meta
        #     f = open(f_meta)
        #     data = json.load(f)
        #     dbd_name = meta.replace(".json", "")
        #     p = MetaJson.objects.create(dashboard_name=dbd_name,dashboard_meta=data)

        # meta_json_list = MetaJson.objects.values() # If empty, read from file

        # for meta in meta_json_list : 
        #     dbd_meta = meta['dashboard_meta']
        #     dbd_name = meta['dashboard_name']
        #     chart_list = dbd_meta['charts']

        #     for k, v in chart_list.items() :
        #         chart_name = k
        #         chart_type = chart_list[k]['chart_type']
        #         c_data = {}
        #         c_data['variables'] = chart_list[k]['variables']
        #         c_data['input'] = chart_list[k]['chart_source']
        #         api_type = chart_list[k]['api_type']
        #         try:
        #             res = dashboard_builder.build_chart(chart_list[k]['chart_type'], c_data)
        #             if len(res) > 0 : # If the dict isnt empty
        #                 record_exists = KKMNowJSON.objects.filter(dashboard_name=dbd_name, chart_name=k).count()
        #                 if record_exists : # If the record exists, update
        #                     cur_record = KKMNowJSON.objects.get(dashboard_name=dbd_name, chart_name=k)
        #                     cur_record.chart_data = res
        #                     cur_record.save()
        #                 else : # If the record does not exist, insert
        #                     p = KKMNowJSON.objects.create(dashboard_name=dbd_name, chart_name=k, chart_type=chart_type,api_type=api_type, chart_data=res)
        #                     p.save()
        #                 print("SUCCESS : " + chart_name + ", Dashboard : " + dbd_name)
        #         except:
        #             print("FAILED : " + chart_name + ", Dashboard : " + dbd_name)