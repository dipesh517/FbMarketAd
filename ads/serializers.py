from rest_framework import serializers

class AdImageSerializer(serializers.Serializer):
  fileName = serializers.CharField()
  
class AdCreativeSerializer(serializers.Serializer):
  title = serializers.CharField()
  body = serializers.CharField()
  imageHash = serializers.CharField()
  
class AdSerializer(serializers.Serializer):
  name = serializers.CharField()
  adSetId = serializers.CharField()
  adCreativeId = serializers.CharField()