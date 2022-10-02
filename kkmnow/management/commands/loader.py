from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import sched, time

import numpy as np
import pandas as pd
from datetime import datetime

from kkmnow.utils import dashboard_builder
from kkmnow.utils import cron_utils
from kkmnow.utils import data_utils
from kkmnow.utils import triggers

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
        operation =  kwargs['operation'][0]

        '''
        OPERATIONS : 
        1. UPDATE
            - Updates the db, by updating values of pre-existing records
        
        2. REBUILD
            - Rebuilds the db, by clearing existing values, and inputting new ones
        '''

        cron_utils.data_operation(operation)
