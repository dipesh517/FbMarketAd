from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.api import FacebookAdsApi
from rest_framework import status
from .serializers import AdsetCreateSerializer, AdsetUpdateSerializer
from AdCampaign.models import AccountSecrets
from AdCampaign.enums import DATE_PRESET
# from facebookads.adobjects.adset import AdSet


class AdsetList(APIView):
  """
  List all adsets, or create a new adset.
  """
  def get(self,request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    FacebookAdsApi.init(access_token=access_token)
    fields = [
      'name',
      'campaign_id',
      'status',
      'effective_status',
      'daily_budget',
      'lifetime_budget',
      'optimization_goal',
      'bid_amount',
      'start_time',
      'end_time',
      'billing_event'
    ]
    params = {
      'effective_status': ['ACTIVE','PAUSED', 'CAMPAIGN_PAUSED', 'ARCHIVED', 'IN_PROCESS', 'WITH_ISSUES'],
    }
    if request.query_params.__contains__('date_preset'):
      date_preset = request.query_params['date_preset']
      if DATE_PRESET.has_value(date_preset):
        params['date_preset'] = date_preset

    if request.query_params.__contains__('time_range'):
      print(request.query_params['time_range'])
      params['time_range'] = request.query_params['time_range']

    account = AdAccount(id)
    adsets = account.get_ad_sets(fields=fields, params= params) 
    adset_list = []  
    for adset in adsets:
      adset["campaign_name"] = Campaign(adset['campaign_id']).api_get(fields=['name'])["name"]
      adset_list.append(adset) 
    print ("adsets_list",adset_list)
    return Response(data = adset_list)

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdsetCreateSerializer(data=request.data)
    if serializer.is_valid():
      print("serializer data>>>",request.data)
      fields = [
      ]
      params = {
        'name': request.data['name'],
        'billing_event': request.data['billing_event'],
        'optimization_goal': request.data['optimization_goal'],
        'campaign_id': request.data['campaign_id'],
        'status': "PAUSED",
        'targeting': {},
      }

      if request.data.get("daily_budget"):
        params['daily_budget'] = request.data['daily_budget']

      if request.data.get('lifetime_budget'):
        params['lifetime_budget'] = request.data['lifetime_budget']
      
      if request.data.get('end_time'):
        params['end_time'] = request.data['end_time']
      
      if request.data.get('start_time'):
        params['start_time'] = request.data['start_time']

      if request.data.get('bid_amount'):
        params['bid_amount'] = request.data['bid_amount']

      if request.data.get('device_platforms'):
        params['targeting']['device_platforms'] = request.data.get('device_platforms')
      
      if request.data.get('publisher_platforms'):
        params['targeting']['publisher_platforms'] = request.data.get('publisher_platforms')
      
      if request.data.get('age_min'):
        params['targeting']['age_min'] = request.data.get('age_min')

      if request.data.get('age_max'):
        params['targeting']['age_max'] = request.data.get('age_max')

      if request.data.get('countries'):
        params['targeting']['geo_locations'] = {"countries": request.data.get('countries')} 

      if request.data.get('genders'):
        params['targeting']['genders'] = request.data.get('genders')

      print("params>>>",params)
      return Response(data = AdAccount(id).create_ad_set(
        fields=fields,
        params=params,
      ))
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdsetDetail(APIView):
  """
  Retrieve, update or delete a adset instance.
  """
  # def get(self, request, pk, format=None):
  #   pass

  def get(self, request, pk, format=None):
    try:
  
      access_token, id = None, None
      if AccountSecrets.objects.first():
        access_token = AccountSecrets.objects.first().access_token
        id = AccountSecrets.objects.first().account_id
      
      FacebookAdsApi.init(access_token=access_token)
      fields = [
        'name',
        'campaign_id',
        'status',
        'daily_budget',
        'lifetime_budget',
        'optimization_goal',
        'bid_amount',
        'start_time',
        'end_time',
        'billing_event',
        'targeting'
      ]
      response = AdSet(pk).api_get(fields=fields, params=None)
      response["campaign_name"] = Campaign(response['campaign_id']).api_get(fields=['name'])["name"]
      return Response(data = response)
    except:
      raise Http404


  def put(self, request, pk, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdsetUpdateSerializer(data=request.data)
    if serializer.is_valid():
      print(request.data)
      fields = [
      ]
      params = {
        # 'name': request.data['name'],
        # 'billing_event': request.data['billing_event'],
        # 'optimization_goal': request.data['optimization_goal'],
        # 'campaign_id': request.data['campaign_id'],
        # 'status': "PAUSED",
        'targeting': {},
      }
      if request.data.get('name'):
        params['name'] = request.data['name']

      if request.data.get("daily_budget"):
        params['daily_budget'] = request.data['daily_budget']

      if request.data.get('billing_event'):
        params['billing_event'] = request.data['billing_event']

      if request.data.get('optimization_goal'):
        params['optimization_goal'] = request.data['optimization_goal']
      
      if request.data.get('status'):
        params['status'] = request.data['status']
        
      if request.data.get('lifetime_budget'):
        params['lifetime_budget'] = request.data['lifetime_budget']
      
      if request.data.get('end_time'):
        params['end_time'] = request.data['end_time']
      
      if request.data.get('start_time'):
        params['start_time'] = request.data['start_time']

      if request.data.get('bid_amount'):
        params['bid_amount'] = request.data['bid_amount']

      if request.data.get('device_platforms'):
        params['targeting']['device_platforms'] = request.data.get('device_platforms')
      
      if request.data.get('publisher_platforms'):
        params['targeting']['publisher_platforms'] = request.data.get('publisher_platforms')
      
      if request.data.get('age_min'):
        params['targeting']['age_min'] = request.data.get('age_min')

      if request.data.get('age_max'):
        params['targeting']['age_max'] = request.data.get('age_max')

      if request.data.get('countries'):
        params['targeting']['geo_locations'] = {"countries": request.data.get('countries')} 

      if request.data.get('genders'):
        params['targeting']['genders'] = request.data.get('genders')

      print("params>>",params)
      return Response(data = AdSet(pk).api_update(
        fields=fields,
        params=params,
      ))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    pass

class AdCreativesListByAdset(APIView):
  def get(self, request, pk, format=None):
    try:
      access_token, id = None, None
      if AccountSecrets.objects.first():
        access_token = AccountSecrets.objects.first().access_token
        id = AccountSecrets.objects.first().account_id
      FacebookAdsApi.init(access_token=access_token)
      fields = [
        'id',
        'name',
        'image_url',
        'object_story_spec'
      ]
      return Response(data = list(AdSet(pk).get_ad_creatives(fields=fields)))
    except:
      raise Http404
