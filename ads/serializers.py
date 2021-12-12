from rest_framework import serializers
  
class AdCreativeSerializer(serializers.Serializer):
  pageId = serializers.CharField()
  name = serializers.CharField()
  message = serializers.CharField()
  image = serializers.CharField()
  
class AdSerializer(serializers.Serializer):
  name = serializers.CharField()
  adSetId = serializers.CharField()
  adCreativeId = serializers.CharField()