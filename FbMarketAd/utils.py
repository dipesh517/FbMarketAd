import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


def validate_credentials(access_token, account_id):
  try:
    url = 'https://graph.facebook.com/debug_token?input_token={}&access_token={}'.format(access_token,access_token)
    response = requests.get(url).json()
    if "error" in response:
      return False
    
    FacebookAdsApi.init(access_token=access_token)
    account = AdAccount(account_id)
    users = account.get_users()
    if users:
      return True
    return False
  except:
    return False
  
