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
from .serializers import AdCreativeCreateSerializer, AdSerializer,  AdCreativeUpdateSerializer
from AdCampaign.models import AccountSecrets
from AdCampaign.enums import DATE_PRESET
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from django.http import Http404


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class AdCreativeList(APIView):

  def get(self,request, format=None):
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
      return Response(data = list(AdAccount(id).get_ad_creatives(fields=fields)))
    except:
      return Http404


  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdCreativeCreateSerializer(data=request.data)
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
  
class AdCreativeDetail(APIView):
  def get(self, request, pk, format=None):
    try:
      access_token, id = None, None
      if AccountSecrets.objects.first():
        access_token = AccountSecrets.objects.first().access_token
        id = AccountSecrets.objects.first().account_id
      
      FacebookAdsApi.init(access_token=access_token)
      fields = [
        'name',
        'image_url',
        'object_story_spec'
      ]
      print("ad preview>>>", Ad('120330001133661705').get_previews(params = {'ad_format': 'DESKTOP_FEED_STANDARD'}))
      return Response(data = AdCreative(pk).api_get(
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

    serializer = AdCreativeUpdateSerializer(data=request.data)
    if serializer.is_valid():
      print(request.data)
      adcreative = AdCreative(pk).api_get(fields= ['name', 'object_story_spec'])
      print("ad_creative>>",adcreative)
      if adcreative:
        params = {
        'name': adcreative['name'],
        'object_story_spec': adcreative['object_story_spec']
        }

        if request.data.get('name'):
          params['name'] = request.data['name']
        if request.data.get('image'):
          ad_image_path = os.path.join(BASE_DIR, "static","images",'ad_image.jpeg')
          image_64_decode = base64.b64decode(request.data['image']) 
          image_result = open(ad_image_path , 'wb') # create a writable image and write the decoding result
          image_result.write(image_64_decode)

          image = AdImage(parent_id=id)
          image[AdImage.Field.filename] = ad_image_path
          image.remote_create()

          imageHash = image[AdImage.Field.hash]
          params['object_story_spec']['link_data']['image_hash'] = imageHash

        if request.data.get('message'):
          params['object_story_spec']['link_data']['message'] = request.data['message']
        
        return Response(data = AdCreative(pk).api_update(
          fields= [],
          params=params,
        ))
      else:
        raise Http404
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    pass

class AdPreview(APIView):
  def get(self, request, pk, format=None):
    try:
      access_token, id = None, None
      if AccountSecrets.objects.first():
        access_token = AccountSecrets.objects.first().access_token
        id = AccountSecrets.objects.first().account_id
      
      FacebookAdsApi.init(access_token=access_token)
      return Response(data = list(Ad(pk).get_previews(params = {'ad_format': 'DESKTOP_FEED_STANDARD'}))[0])
    except:
      raise Http404

  def delete(self, request, pk, format=None):
    pass

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
      'adset_id',
      'campaign_id',
      'creative'
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
    print("ads>>>", ads)
    ads_list = []  
    for ad in ads:
      print("creative_id>>>",ad['creative']['id'])
      if ad['creative']:
        creative_id = ad['creative']['id']
        for adcreative in list(Ad(ad['id']).get_ad_creatives(fields=['name'])):
          if adcreative['id'] == creative_id :
            ad['adcreative_name'] = adcreative['name']
            break;
        
      ad['campaign_name'] = Campaign(ad['campaign_id']).api_get(fields=['name'])["name"]
      ad['adset_name'] = AdSet(ad['adset_id']).api_get(fields=['name'])['name']
      fields = ['reach', 'spend', 'frequency']
      print("ad>>",ad['id'])
      ad_insight = Ad(ad['id']).get_insights(fields=fields)
      print("ads_insights >>>", list(ad_insight))
      if ad_insight:
        ad['reach'] = ad_insight['reach']
        ad['frequency'] = ad_insight['frequency']
        ad['spend'] = ad_insight['spend']
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


