from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from .serializers import MetaSerializer, KKMSerializer
from .models import MetaJson, KKMNowJSON

import json

class KKMNOW(APIView) :
    def get(self, request, format=None):
        param_list = dict(request.GET)
        params_req = ['dashboard']
        
        if all (p in param_list for p in params_req) :
            res = handle_request(param_list)
            return JsonResponse(res, safe=False)
        else :
            return JsonResponse({}, safe=False)

def handle_request(param_list) :
    dbd_name = param_list['dashboard'][0]
    dbd_info = MetaJson.objects.filter(dashboard_name=dbd_name).values()

    params_req = []

    if len(dbd_info) > 0 :
        dbd_info = dbd_info[0]
        dbd_info = dbd_info['dashboard_meta']

        params_req = dbd_info['required_params']
        params_opt = dbd_info['optional_params']

    res = {}
    if all (p in param_list for p in params_req) :
        data = KKMNowJSON.objects.filter(dashboard_name=dbd_name).values()

        if len(data) > 0 : 
            for i in data :
                api_type = i['api_type']
                api_params = dbd_info['charts'][ i['chart_name'] ]['api_params']
                if api_type == 'static':
                    res[ i['chart_name'] ] = i['chart_data']
                else :
                    if len(api_params) > 0 : 
                        temp = i['chart_data']
                        for a in api_params :
                            if a in param_list : 
                                key = param_list[a][0] if '__FIXED__' not in a else a.replace("__FIXED__", "")
                                if key in temp :
                                    temp = temp[ key ]
                            else :
                                temp = {}
                                break
                        if len(temp) > 0 : 
                            res[ i['chart_name'] ] = temp
                    else :
                        res[ i['chart_name'] ] = i['chart_data']
    return res

def slice_json_by_params(chart_params, url_params, data) :
    r_data = data

    for i in chart_params : 
        param_val = url_params[i][0]
        if param_val in data : 
            r_data = data[param_val]
        else : 
            break

    return r_data

def required_params(param_list, dict) : 
    for i in param_list : 
        if i not in dict : 
            return False
    
    return True

def default_params(param, dict, default) :
    if param not in dict :
        return default
    else :
        return dict[param][0]