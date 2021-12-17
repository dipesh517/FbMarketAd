from django.http import Http404
from django.http.response import HttpResponse
from FbMarketAd.utils import validate_credentials
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from rest_framework import status
from .serializers import CampaignCreateSerializer, AccountSecretsSerializer, CampaignUpdateSerializer
from .enums import DATE_PRESET
from .models import AccountSecrets
from django.http import Http404


class CampaignList(APIView):
  """
  List all campaigns, or create a new campaign.
  """
  def get(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    FacebookAdsApi.init(access_token=access_token)
    fields = [
      'name',
      'objective',
      'status',
      'daily_budget',
      'bid_strategy',
      'lifetime_budget'
    ]
    params = {
      'effective_status': ['ACTIVE','PAUSED'],
    }
    if request.query_params.__contains__('date_preset'):
      date_preset = request.query_params['date_preset']
      if DATE_PRESET.has_value(date_preset):
        params['date_preset'] = date_preset

    if request.query_params.__contains__('time_range'):
      print(request.query_params['time_range'])
      params['time_range'] = request.query_params['time_range']

    return Response(data = list(AdAccount(id).get_campaigns(
      fields=fields,
      params=params,
    )))

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = CampaignCreateSerializer(data=request.data)
    if serializer.is_valid():
      print(request.data)
      fields = [
      ]
      params = {
        'name': request.data["name"],
        'objective': request.data["objective"],
        'status': "PAUSED",
        'special_ad_categories': request.data["special_ad_categories"],
      }

      if request.data.get('campaign_budget_optimization'):
        if request.data.get("daily_budget"):
          params['daily_budget'] = request.data['daily_budget']

        if request.data.get('lifetime_budget'):
          params['lifetime_budget'] = request.data['lifetime_budget']
        
        if request.data.get('bid_strategy'):
          params['bid_strategy'] = request.data['bid_strategy']
        else:
          params['bid_strategy'] = 'LOWEST_COST_WITHOUT_CAP'
      
      if request.data.get('spend_cap'):
        params['spend_cap'] = request.data['spend_cap']
        
      return Response(data = AdAccount(id).create_campaign(
        fields=fields,
        params=params,
      ))
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountSecretsView(APIView):
  # """
  # List all snippets, or create a new snippet.
  # """
  # def get(self, request, format=None):
  #     snippets = Snippet.objects.all()
  #     serializer = SnippetSerializer(snippets, many=True)
  #     return Response(serializer.data)

  def post(self, request, format=None):
    serializer = AccountSecretsSerializer(data=request.data)
    if serializer.is_valid():
      is_valid = validate_credentials(request.data["access_token"], request.data["account_id"])
      if is_valid:
        if AccountSecrets.objects.exists():
          a = AccountSecrets.objects.first()
          a.access_token = request.data["access_token"]
          a.account_id = request.data["account_id"]
          a.save()
        else:
          AccountSecrets.objects.create(access_token = request.data['access_token'], account_id = request.data['account_id'])
        return Response({"success": True})
      return Response({"success": False})
    return Response({"success": False})

class CampaignDetail(APIView):
  """
  Retrieve, update or delete a campaign instance.
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
        'objective',
        'status',
        'daily_budget',
        'bid_strategy',
        'lifetime_budget',
        'special_ad_categories',
        'spend_cap'
      ]
      return Response(data = Campaign(pk).api_get(
          fields=fields, params = None
      ))
    except:
      raise Http404


  def put(self, request, pk, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = CampaignUpdateSerializer(data=request.data)
    if serializer.is_valid():
      print(request.data)
      fields = [
      ]
      params = {
        'name': request.data["name"],
        'objective': request.data["objective"],
        'status': request.data["status"],
        'special_ad_categories': request.data["special_ad_categories"],
      }

      if request.data.get('campaign_budget_optimization'):
        if request.data.get("daily_budget"):
          params['daily_budget'] = request.data['daily_budget']

        if request.data.get('lifetime_budget'):
          params['lifetime_budget'] = request.data['lifetime_budget']
        
        if request.data.get('bid_strategy'):
          params['bid_strategy'] = request.data['bid_strategy']
        else:
          params['bid_strategy'] = 'LOWEST_COST_WITHOUT_CAP'
      
      if request.data.get('spend_cap'):
        params['spend_cap'] = request.data['spend_cap']
        
      return Response(data = Campaign(pk).api_update(
        fields=fields,
        params=params,
      ))
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    pass
        