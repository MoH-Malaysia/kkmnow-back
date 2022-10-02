import os
import environ
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from kkmnow.utils import cron_utils, triggers

from .models import KKMNowJSON, MetaJson

env = environ.Env()
environ.Env.read_env()

class KKMNOW(APIView):
    def post(self, request, format=None):
        if "Authorization" not in request.headers:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        secret = request.headers.get("Authorization")
        if secret != os.getenv("WORKFLOW_TOKEN"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cron_utils.data_operation('UPDATE')
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        param_list = dict(request.GET)
        params_req = ["dashboard"]

        if all(p in param_list for p in params_req):
            res = handle_request(param_list)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse({}, safe=False)

def handle_request(param_list):
    dbd_name = param_list["dashboard"][0]
    dbd_info = MetaJson.objects.filter(dashboard_name=dbd_name).values()

    params_req = []

    if len(dbd_info) > 0:
        dbd_info = dbd_info[0]
        dbd_info = dbd_info["dashboard_meta"]
        params_req = dbd_info["required_params"]

    res = {}
    if all(p in param_list for p in params_req):
        data = KKMNowJSON.objects.filter(dashboard_name=dbd_name).values()

        if len(data) > 0:
            for i in data:
                api_type = i["api_type"]
                api_params = dbd_info["charts"][i["chart_name"]]["api_params"]
                if api_type == "static":
                    res[i["chart_name"]] = i["chart_data"]
                else:
                    cur_chart_data = i["chart_data"]
                    if len(api_params) > 0:
                        cur_chart_data = get_nested_data(api_params, param_list, cur_chart_data)

                    if len(cur_chart_data) > 0:
                        res[i["chart_name"]] = cur_chart_data
    return res

def get_nested_data(api_params, param_list, data) :
    for a in api_params:
        if a in param_list:
            key = param_list[a][0] if "__FIXED__" not in a else a.replace("__FIXED__", "")
            if key in data:
                data = data[key]
        else:
            data = {}
            break
    
    return data
