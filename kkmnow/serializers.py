from rest_framework import serializers
from .models import MetaJson, KKMNowJSON, GitHashData

class MetaSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = MetaJson
        fields = ['dashboard_name', 'dashboard_meta']

class KKMSerializer(serializers.ModelSerializer) :
    class KKM : 
        model = KKMNowJSON
        fields = ['dashboard_name', 'chart_name', 'chart_type', 'chart_data']

class HashSerializer(serializers.ModelSerializer) :
    class GitHash : 
        model = GitHashData
        fields = ['last_update', 'git_hash']