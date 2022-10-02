from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from kkmnow.models import MetaJson, KKMNowJSON
from kkmnow.utils import dashboard_builder
from kkmnow.utils import triggers

import os
from os import listdir
from os.path import isfile, join
import json

def rebuild_dashboard_meta(operation) :
    triggers.send_telegram("META JSON " + operation + " IS BEING PERFORMED")
    if operation == 'REBUILD' : 
        MetaJson.objects.all().delete()

    # META_DIR = os.path.dirname(os.path.realpath(__file__)) + '/META_JSON/'
    META_DIR = os.path.join(os.getcwd(), 'kkmnow/management/commands/META_JSON/')
    meta_files = []
    meta_files = [f for f in listdir(META_DIR) if isfile(join(META_DIR, f))]

    # get_or_create
    for meta in meta_files : 
        f_meta = META_DIR + meta
        f = open(f_meta)
        data = json.load(f)
        dbd_name = meta.replace(".json", "")
        record_exists = MetaJson.objects.filter(dashboard_name=dbd_name).count()
        
        if record_exists : 
            cur_record = MetaJson.objects.get(dashboard_name=dbd_name) # Get last record here
            cur_record.dashboard_meta = data
            cur_record.save()                
        else : 
            new_record = MetaJson.objects.create(dashboard_name=dbd_name,dashboard_meta=data)
            new_record.save()

        # cache.set('META_' + dbd_name, data)

def rebuild_dashboard_charts(operation) :
    triggers.send_telegram("CHART " + operation + " ARE BEING PERFORMED")
    if operation == 'REBUILD' : 
        KKMNowJSON.objects.all().delete()
    
    meta_json_list = MetaJson.objects.values()

    for meta in meta_json_list : 
        dbd_meta = meta['dashboard_meta']
        dbd_name = meta['dashboard_name']
        chart_list = dbd_meta['charts']

        for k, v in chart_list.items() :
            chart_name = k
            chart_type = chart_list[k]['chart_type']
            c_data = {}
            c_data['variables'] = chart_list[k]['variables']
            c_data['input'] = chart_list[k]['chart_source']
            api_type = chart_list[k]['api_type']
            try:
                res = dashboard_builder.build_chart(chart_list[k]['chart_type'], c_data)
                if len(res) > 0 : # If the dict isnt empty
                    record_exists = KKMNowJSON.objects.filter(dashboard_name=dbd_name, chart_name=k).count()
                    if record_exists : # If the record exists, update
                        cur_record = KKMNowJSON.objects.get(dashboard_name=dbd_name, chart_name=k)
                        cur_record.chart_data = res
                        cur_record.save()
                    else : # If the record does not exist, insert
                        p = KKMNowJSON.objects.create(dashboard_name=dbd_name, chart_name=k, chart_type=chart_type,api_type=api_type, chart_data=res)
                        p.save()
                    # cache.set(dbd_name + "_" + k, res)    
                    # print("SUCCESS : " + chart_name + ", Dashboard : " + dbd_name)
            except Exception as e:
                triggers.send_telegram("! FAILED : " + chart_name + ", Dashboard : " + dbd_name + ", Reason : " + e)