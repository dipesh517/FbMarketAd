import os
import base64
from pathlib import Path
from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from rest_framework import status
from .serializers import AdCreativeSerializer, AdSerializer
from AdCampaign.models import AccountSecrets
from AdCampaign.enums import DATE_PRESET
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class AdCreative(APIView):

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdCreativeSerializer(data=request.data)
    if serializer.is_valid():
      
      ad_image_path = os.path.join(BASE_DIR, "static","images",'ad_image.jpeg')
      image_64_decode = base64.b64decode(request.data['image']) 
      image_result = open(ad_image_path , 'wb') # create a writable image and write the decoding result
      image_result.write(image_64_decode)

      image = AdImage(parent_id=id)
      image[AdImage.Field.filename] = ad_image_path
      image.remote_create()

      imageHash = image[AdImage.Field.hash]

      fields = [
      ]
      params = {
      'name': request.data['name'],
      'object_story_spec': {
        'page_id': request.data['pageId'],
        'link_data':{
          'image_hash':imageHash,
          'link':'https://www.facebook.com/' + request.data['pageId'],
          'message':request.data['message']
          }
        },
      }

      return Response(data = AdAccount(id).create_ad_creative(
        fields=fields,
        params=params,
      ))
          
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdsList(APIView):

  def get(self,request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    FacebookAdsApi.init(access_token=access_token)
    fields = [
      'id',
      'name',
      'created_time',
      'updated_time',
      'status',
      'effective_status',
      'bid_amount',
    ]
    params = {
    }
    if request.query_params.__contains__('date_preset'):
      date_preset = request.query_params['date_preset']
      if DATE_PRESET.has_value(date_preset):
        params['date_preset'] = date_preset

    if request.query_params.__contains__('time_range'):
      print(request.query_params['time_range'])
      params['time_range'] = request.query_params['time_range']

    account = AdAccount(id)
    ads = account.get_ads(fields=fields, params = params)
    ads_list = []  
    for ad in ads:
      # ad["adcreative_name"] = Campaign(adset['campaign_id']).api_get(fields=['name'])["name"]
      fields = ['reach', 'spend', 'frequency', 'adset_name']
      ad_insight = Ad(ad['id']).get_insights(fields = fields)
      ad['reach'] = ad_insight['reach']
      ad['frequency'] = ad_insight['frequency']
      ad['spend'] = ad_insight['spend']
      ad['adset_name'] = ad_insight['adset_name']
      ads_list.append(ad) 
    print ("ads_list",ads_list)
    return Response(data = ads_list)

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdSerializer(data=request.data)
    if serializer.is_valid():
      fields = [
      ]
      params = {
        'name': request.data['name'],
        'adset_id': request.data['adSetId'],
        'creative': {'creative_id':request.data['adCreativeId']},
        'status': 'PAUSED'
      }
      return Response(data = AdAccount(id).create_ad(
        fields=fields,
        params=params,
      ))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

