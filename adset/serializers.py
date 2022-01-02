from rest_framework import serializers

# create a tuple
ADSET_STATUS_CHOICES =( 
  ("ACTIVE", "ACTIVE"), 
  ("PAUSED", "PAUSED"), 
  ("DELETED", "DELETED"), 
  ("ARCHIVED", "ARCHIVED")
)

DEVICE_PLATFORM_CHOICES =( 
  ("desktop", "desktop"), 
  ("mobile", "mobile")
)

PUBLISHER_PLATFORM_CHOICES = (
  ("facebook","facebook"),
  ("audience_network","audience_network"),
  ("instagram","instagram"),
  ("messenger","messenger")
)

GENDER_CHOICES = (
  (0,0),
  (1,1),
  (2,2)
)
OPTIMIZATION_GOAL_CHOICES =( 
  ("NONE", "NONE"), 
  ("APP_INSTALLS","APP_INSTALLS"), 
  ("AD_RECALL_LIFT","AD_RECALL_LIFT"), 
  ("ENGAGED_USERS","ENGAGED_USERS"), 
  ("EVENT_RESPONSES","EVENT_RESPONSES"), 
  ("IMPRESSIONS","IMPRESSIONS"), 
  ("LEAD_GENERATION","LEAD_GENERATION"), 
  ("QUALITY_LEAD","QUALITY_LEAD"), 
  ("LINK_CLICKS","LINK_CLICKS"), 
  ("OFFSITE_CONVERSIONS","OFFSITE_CONVERSIONS"), 
  ("PAGE_LIKES","PAGE_LIKES"), 
  ("POST_ENGAGEMENT","POST_ENGAGEMENT"), 
  ("QUALITY_CALL","QUALITY_CALL"), 
  ("REACH","REACH"), 
  ("LANDING_PAGE_VIEWS","LANDING_PAGE_VIEWS"), 
  ("VISIT_INSTAGRAM_PROFILE","VISIT_INSTAGRAM_PROFILE"), 
  ("VALUE","VALUE"), 
  ("THRUPLAY","THRUPLAY"), 
  ("DERIVED_EVENTS","DERIVED_EVENTS"), 
  ("APP_INSTALLS_AND_OFFSITE_CONVERSIONS","APP_INSTALLS_AND_OFFSITE_CONVERSIONS"), 
  ("CONVERSATIONS","CONVERSATIONS"), 
  ("IN_APP_VALUE","IN_APP_VALUE")
)

BILLING_EVENT_CHOICES = (
  ('APP_INSTALLS', 'APP_INSTALLS'), 
  ('CONVERSIONS','CONVERSIONS'), 
  ('LINK_CLICKS','LINK_CLICKS'), 
  ('OFFER_CLAIMS','OFFER_CLAIMS'), 
  ('PAGE_LIKES','PAGE_LIKES'), 
  ('POST_ENGAGEMENT','POST_ENGAGEMENT'), 
  ("CLICKS","CLICKS"),
  ("IMPRESSIONS","IMPRESSIONS"),
  ("THRUPLAY","THRUPLAY"),
  ("PURCHASE","PURCHASE"),
  ("LISTING_INTERACTION","LISTING_INTERACTION")
)

DISTANCE_UNIT_CHOICES = (
  ('kilometer', 'kilometer'),
  ('mile', 'mile')
)

class AdsetTargetingByGeoLocationSerializer(serializers.Serializer):
  latitude = serializers.DecimalField(max_digits=10, decimal_places=5, required = True)
  longitude = serializers.DecimalField(max_digits=10, decimal_places=5, required = True)
  radius = serializers.DecimalField(max_digits=10, decimal_places=5, required = True)
  distance_unit = serializers.ChoiceField(choices = DISTANCE_UNIT_CHOICES, default = 'mile')
class AdsetCreateSerializer(serializers.Serializer):
  name = serializers.CharField()
  campaign_id = serializers.IntegerField(required = True)
  # status = serializers.ChoiceField(choices = ADSET_STATUS_CHOICES, required = False) 
  optimization_goal = serializers.ChoiceField(choices = OPTIMIZATION_GOAL_CHOICES) 
  billing_event = serializers.ChoiceField(choices = BILLING_EVENT_CHOICES) 
  daily_budget = serializers.IntegerField(required = False)
  lifetime_budget = serializers.IntegerField(required = False)
  bid_amount = serializers.IntegerField(required = False)
  is_dynamic_creative = serializers.BooleanField(default = False)
  start_time = serializers.CharField(required = False)
  end_time = serializers.CharField(required = False)
  countries = serializers.ListField(     
    child = serializers.CharField(max_length = 2), allow_empty = True
  )
  age_max = serializers.IntegerField(required = False)
  age_min = serializers.IntegerField(required = False)
  genders = serializers.MultipleChoiceField(choices = GENDER_CHOICES, required = False)
  device_platforms = serializers.MultipleChoiceField(
                        choices = DEVICE_PLATFORM_CHOICES,allow_blank = True, required = False)
  publisher_platforms = serializers.MultipleChoiceField(
                        choices = DEVICE_PLATFORM_CHOICES,allow_blank = True, required = False)
  # custom_locations = serializers.BooleanField(default = False)
  custom_locations = serializers.ListField(
   child= AdsetTargetingByGeoLocationSerializer(), allow_empty = True, required = False
  )

class AdsetUpdateSerializer(serializers.Serializer):
  name = serializers.CharField()
  # campaign_id = serializers.IntegerField(required = True)
  status = serializers.ChoiceField(choices = ADSET_STATUS_CHOICES, required = False) 
  optimization_goal = serializers.ChoiceField(choices = OPTIMIZATION_GOAL_CHOICES, required = False) 
  billing_event = serializers.ChoiceField(choices = BILLING_EVENT_CHOICES, required = False) 
  daily_budget = serializers.IntegerField(required = False)
  lifetime_budget = serializers.IntegerField(required = False)
  bid_amount = serializers.IntegerField(required = False)
  is_dynamic_creative = serializers.BooleanField(default = False)
  start_time = serializers.CharField(required = False)
  end_time = serializers.CharField(required = False)
  countries = serializers.ListField(     
    child = serializers.CharField(max_length = 2), allow_empty = True, required = False
  )
  age_max = serializers.IntegerField(required = False)
  age_min = serializers.IntegerField(required = False)
  genders = serializers.MultipleChoiceField(choices = GENDER_CHOICES, required = False)
  device_platforms = serializers.MultipleChoiceField(
                        choices = DEVICE_PLATFORM_CHOICES,allow_blank = True, required = False)
  publisher_platforms = serializers.MultipleChoiceField(
                        choices = DEVICE_PLATFORM_CHOICES,allow_blank = True, required = False)
  # custom_locations = serializers.BooleanField(default = False)
  custom_locations = serializers.ListField(
   child= AdsetTargetingByGeoLocationSerializer(), allow_empty = True, required = False
  )




