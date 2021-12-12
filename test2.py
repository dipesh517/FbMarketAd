
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adcreative import AdCreative

access_token = 'EAAGJ5BKkyXMBACEL1rzaGqd63rjL1jTdzPbnBEEQBZBIHmGxumvFPwQXyZALWHN5ZB2vRmWZBVCjEXJry5qtMdy5chSCynUYMjXbKedGoVWs4Nn53lnSkgn9ZAZC4EZCsgRAJ9uiUFk7nVUmxt6Lsfz1QbcljZAY7ZB5TaZADWW7bnn7MADI4qd6xLVFpeC9GFWZBebB1s9bpgg9h1jiZAi5ADiEJPuQKEqZBflgZD'
app_secret = '<APP_SECRET>'
app_id = '<APP_ID>'
id = 'act_3658962400798849'
FacebookAdsApi.init(access_token=access_token)


fields = [
]
params = {
  'name': 'Sample Creative',
  'object_story_spec': {'page_id':'103619158129352','link_data':{'image_hash':'1645566ca45be953d3ef28b2f76f0ac2','link':'https://www.facebook.com/' + '103619158129352','message':'try it out'}},
}
print(AdAccount(id).create_ad_creative(
  fields=fields,
  params=params,
))

