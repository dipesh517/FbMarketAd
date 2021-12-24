from rest_framework import serializers
  
class AdCreativeCreateSerializer(serializers.Serializer):
  pageId = serializers.CharField()
  name = serializers.CharField()
  message = serializers.CharField()
  image = serializers.CharField()

class AdCreativeUpdateSerializer(serializers.Serializer):
  name = serializers.CharField(required = False)
  message = serializers.CharField(required = False)
  image = serializers.CharField(required = False)

class AdSerializer(serializers.Serializer):
  name = serializers.CharField()
  adSetId = serializers.CharField()
  adCreativeId = serializers.CharField()