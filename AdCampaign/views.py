from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from rest_framework import status
from .serializers import CampaignSerializer
from .enums import DATE_PRESET


access_token = 'EAAGJ5BKkyXMBAIqkPIVjRvuMxCCiViLrVZBWHxff5uXpukwoSH71i8zU3cycS3ABNilKi37GYcvZBZBLxz6WZCDCgsTrB7AzyOa1wZBISsMFqe6VuzuAvQzwW4zZAAtPkriKlgEROm3TQhJZBwwHZA6LZAHx4bON0E1kjkuUZAAWABQzEq9lYZC5jVtXpOcuZC7L3D4hHZBlmNxr7QfdoEjdoOx6U7udXMxt9jxFJDTZBrJGWX0AZDZD'
app_secret = '<APP_SECRET>'
app_id = '<APP_ID>'
id = 'act_3658962400798849'


class CampaignList(APIView):
  """
  List all campaigns, or create a new campaign.
  """
  def get(self, request, format=None):
    FacebookAdsApi.init(access_token=access_token)
    fields = [
      'name',
      'objective',
      'status'
    ]
    params = {
      'effective_status': ['ACTIVE','PAUSED'],
    }
    if request.query_params.__contains__('date_preset'):
      date_preset = request.query_params['date_preset']
      if DATE_PRESET.has_value(date_preset):
        params['date_preset'] = date_preset

    if request.query_params.__contains__('time_range'):
      params['time_range'] = request.query_params['time_range']

    return Response(data = list(AdAccount(id).get_campaigns(
      fields=fields,
      params=params,
    )))

  def post(self, request, format=None):
    serializer = CampaignSerializer(data=request.data)
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
      return Response(data = AdAccount(id).create_campaign(
        fields=fields,
        params=params,
      ))
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampaignDetail(APIView):
  """
  Retrieve, update or delete a campaign instance.
  """
  def get_object(self, pk):
    pass

  def get(self, request, pk, format=None):
    pass

  def put(self, request, pk, format=None):
    pass

  def delete(self, request, pk, format=None):
    pass
        