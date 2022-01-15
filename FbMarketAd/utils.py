import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.api import FacebookAdsApi


def validate_credentials(access_token, account_id):
  try:
    # url = 'https://graph.facebook.com/debug_token?input_token={}&access_token={}'.format(access_token,access_token)
    # response = requests.get(url).json()
    # print(response, 'response')
    # if "error" in response:
    #   return False
    
    FacebookAdsApi.init(access_token=access_token)
    account = AdAccount(account_id)
    account.remote_read(fields=[AdAccount.Field.id, AdAccount.Field.account_id])
    if account:
      print("account>>>",account)
      return True
    return False
    # users = account.get_users()
    # print(users, 'users')
    # print(account, 'account')
    # if users:
    #   return True
    # return False
  except Exception as e:
    print(e)
    return False
  

def getAdIdFromCreativeId(creative_id, account_id, access_token):
  FacebookAdsApi.init(access_token=access_token)
  ad_account = AdAccount(account_id)
  ad_iter = list(ad_account.get_ads(fields=[Ad.Field.id,Ad.Field.name, Ad.Field.creative]))
  for ad in ad_iter:
    if int(ad['creative']['id']) == creative_id:
      return ad['id']
  




