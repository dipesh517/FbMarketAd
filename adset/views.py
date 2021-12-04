from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from rest_framework import status
from .serializers import AdsetSerializer
from AdCampaign.models import AccountSecrets
from AdCampaign.enums import DATE_PRESET

class AdsetList(APIView):
  """
  List all adsets, or create a new adset.
  """
  def get(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    FacebookAdsApi.init(access_token=access_token)
    fields = [
      'name',
      'campaign',
      'campaign_id',
      'status',
      'daily_budget',
      'lifetime_budget',
      'optimization_goal',
      'bid_amount',
      'start_time',
      'end_time',
      'billing_event'
    ]
    params = {
      # 'effective_status': ['ACTIVE','PAUSED'],
    }
    if request.query_params.__contains__('date_preset'):
      date_preset = request.query_params['date_preset']
      if DATE_PRESET.has_value(date_preset):
        params['date_preset'] = date_preset

    if request.query_params.__contains__('time_range'):
      print(request.query_params['time_range'])
      params['time_range'] = request.query_params['time_range']

    ad_sets = Response(data = list(AdAccount(id).get_ad_sets(
      fields=fields,
      params=params,
    )))
    print(ad_sets)
    return ad_sets

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdsetSerializer(data=request.data)
    if serializer.is_valid():
      print(request.data)
      fields = [
      ]
      params = {
        'name': request.data['name'],
        'billing_event': request.data['billing_event'],
        'optimization_goal': request.data['optimization_goal'],
        'campaign_id': request.data['campaign_id'],
        'status': "PAUSED",
        'targeting': {'device_platforms':['mobile'],'facebook_positions':['feed'],'geo_locations':{'countries':['US']},'publisher_platforms':['facebook','audience_network'],'user_os':['IOS']},
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

      print(params)
      return Response(data = AdAccount(id).create_ad_set(
        fields=fields,
        params=params,
      ))
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

