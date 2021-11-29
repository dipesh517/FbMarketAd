from rest_framework import serializers

# create a tuple
CAMPAIGN_STATUS_CHOICES =( 
  ("ACTIVE", "ACTIVE"), 
  ("PAUSED", "PAUSED"), 
  ("DELETED", "DELETED"), 
  ("ARCHIVED", "ARCHIVED")
)

CAMPAIGN_OBJECTIVE_CHOICES = (
  ('APP_INSTALLS', 'APP_INSTALLS'), 
  ('BRAND_AWARENESS','BRAND_AWARENESS'), 
  ('CONVERSIONS','CONVERSIONS'), 
  ('EVENT_RESPONSES','CONVERSIONS'), 
  ('LEAD_GENERATION','LEAD_GENERATION'), 
  ('LINK_CLICKS','LINK_CLICKS'), 
  ('LOCAL_AWARENESS','LOCAL_AWARENESS'), 
  ('MESSAGES','MESSAGES'), 
  ('OFFER_CLAIMS','OFFER_CLAIMS'), 
  ('PAGE_LIKES','PAGE_LIKES'), 
  ('POST_ENGAGEMENT','POST_ENGAGEMENT'), 
  ('PRODUCT_CATALOG_SALES','PRODUCT_CATALOG_SALES'), 
  ('REACH','REACH'), 
  ('STORE_VISITS','STORE_VISITS'), 
  ('VIDEO_VIEWS','VIDEO_VIEWS')
)

SPECIAL_AD_CATEGORIES_CHOICES = (
  ('EMPLOYMENT','EMPLOYMENT'), 
  ('HOUSING','HOUSING'), 
  ('CREDIT','CREDIT'), 
  ('ISSUES_ELECTIONS_POLITICS','ISSUES_ELECTIONS_POLITICS'), 
  ('ONLINE_GAMBLING_AND_GAMING','ONLINE_GAMBLING_AND_GAMING')
)

class CampaignSerializer(serializers.Serializer):
  # initialize fields
  name = serializers.CharField()
  # status = serializers.ChoiceField(choices = CAMPAIGN_STATUS_CHOICES) 
  objective = serializers.ChoiceField(choices = CAMPAIGN_OBJECTIVE_CHOICES)
  special_ad_categories = serializers.MultipleChoiceField(
                        choices = SPECIAL_AD_CATEGORIES_CHOICES,allow_blank= True)