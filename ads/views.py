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
from .serializers import AdImageSerializer, AdCreativeSerializer, AdSerializer
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
      
      creative = AdCreative(parent_id=id)
      creative[AdCreative.Field.title] = request.data['title']
      creative[AdCreative.Field.body] = request.data['body']
      creative[AdCreative.Field.image_hash] = imageHash
      creative.remote_create()

      response = {
        "success": True,
        "id": creative[AdCreative.Field.id]
      }
      return Response(data = response)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdsList(APIView):

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

