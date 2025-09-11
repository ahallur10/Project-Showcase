#!/usr/bin/env python3

import json, hmac, hashlib, time, requests
from requests.auth import AuthBase

# Wallet/Sign-in REST API
API_URL = 'https://api.coinbase.com/v2/'
API_KEY = 'FkBd60wJkzRfojZJ'
API_SECRET = 'M0CWV288oW8EVin7djlmKjhTTNF4FGwf'

# Commerce REST API
COMMERCE_API_URL = 'https://api.commerce.coinbase.com/'
COMMERCE_API_KEY = '8a02a628-6f97-43fa-99d2-5284e23a9ace'


# Other settings
PAYMENT_REDIRECT_URL = 'https://apple.com' # page user sees after making payment



# Create custom authentication for Coinbase Wallet/Sign-in API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        
    def __call__(self, request):
        timestamp = str(int(time.time()))
        
        if request.body is None:
            body = ''
        else:
            body = request.body.decode('utf-8')
        
        message = timestamp + request.method + request.path_url + body
        secret = self.api_secret
        
        if not isinstance(message, bytes):
            message = message.encode()
        if not isinstance(secret, bytes):
            secret = secret.encode()
            
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request



# Creates a payment request for user and returns the checkout page URL
# Coinbase's Wallet/Sign-in api is broken as shit, so are their docs. requesting money is now done via Commerce REST API, not the Wallet/Sign-in one
def requestFundsFromUser(amount):
    payload = {
        'name': 'NuSkill',
        'description': 'Training bounty! If you complete your training, you will get this back.',
        'pricing_type': 'fixed_price',
        'local_price': {'amount': amount, 'currency': 'USD'}, #they claim $2 is min, but doesnt work. $3 did
        'redirect_url': PAYMENT_REDIRECT_URL #take them to a page saying "waiting for funds to transfer and to check back later. then have webhook run another function that updates their status in db
    }
    
    r = requests.post(COMMERCE_API_URL + 'charges', json=payload, headers={'X-CC-Api-Key': COMMERCE_API_KEY})
    res = r.json()
    #print(res)
    #print(json.dumps(res, indent=4)) #print it out all pretty
    
    redirect_url = res['data']['hosted_url']
    
    return redirect_url


# Return/send funds to user
def returnFundsToUser(to, amount):
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
    r = requests.get(API_URL + 'user', auth=auth)
    #print(r.json())
    
    payload = {
        'type': 'send',
        'to': to, # can also be bitcoin wallet address
        'amount': amount,
        'currency': 'USD',
        'description': 'Congrats on completing your training!',
    }

    r = requests.post(API_URL + 'accounts/primary/transactions', json=payload, auth=auth)
    #print(r.json())
    
    # TODO: check if payment was sent, and if so, call some other groupmember's code to update user status in database


# main to test functions. comment out the one you dont want to test
def main():
    # Creates a payment request for user and returns the checkout page URL
    print(requestFundsFromUser(amount='3.00'))
    
    
    # Send/return funds to user
    #returnFundsToUser(to='mgd3@arizona.edu', amount='2.00')


main()