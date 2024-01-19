import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from bookstore.settings import *
 
# class MpesaC2bCredential:
   
#     consumer_key= c2b_consumer_key #input your consumer key from the sandbox  
#     consumer_secret  = c2b_consumer_secret #input your consumer secret from the sandbox
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# class MpesaAccessToken:
#     r = requests.get(MpesaC2bCredential.api_URL,
#                      auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']


# class LipanaMpesaPpassword:
#     lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
#     Business_short_code = "9680857" #for stk push
#     Test_c2b_shortcode = "600344" #for C2B 
#     passkey = passKey  #input your passkey from the safaricom dev portal
#     # security_credential = security_credential#add your security credential
#     data_to_encode = Business_short_code + passkey + lipa_time
#     online_password = base64.b64encode(data_to_encode.encode())
#     decode_password = online_password.decode('utf-8')