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


class AdCreative(APIView):

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdCreativeSerializer(data=request.data)
    if serializer.is_valid():
      creative = AdCreative(parent_id=id)
      creative[AdCreative.Field.title] = request.data['title']
      creative[AdCreative.Field.body] = request.data['body']
      creative[AdCreative.Field.image_hash] = request.data['imageHash']
      creative.remote_create()

      response = {
        "success": True,
        "id": creative[AdCreative.Field.id]
      }
      return Response(data = response)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdImage(APIView):

  def post(self, request, format=None):
    access_token, id = None, None
    if AccountSecrets.objects.first():
      access_token = AccountSecrets.objects.first().access_token
      id = AccountSecrets.objects.first().account_id
    
    FacebookAdsApi.init(access_token=access_token)

    serializer = AdImageSerializer(data=request.data)
    if serializer.is_valid():
      image = AdImage(parent_id=id)
      image[AdImage.Field.filename] = request.data['fileName']
      image.remote_create()

      response = {
        "success": True,
        "imageHash": image[AdImage.Field.hash]
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

