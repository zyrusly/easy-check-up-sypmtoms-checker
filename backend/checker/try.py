from hashlib import md5
import requests
import hmac
import base64
import json

AUTH_URI = 'https://sandbox-authservice.priaid.ch'
BASE_URI = 'https://sandbox-healthservice.priaid.ch'


# Hmac md5 hashing for Authorization as per Api docs
def generate_token():
    AUTH_URI = 'https://sandbox-authservice.priaid.ch/login'
    API_KEY = 'zyemnl@gmail.com'
    SECRET_KEY = 'Ed2e6ZKy79WaRz84D'

    hashed = hmac.new(str.encode(SECRET_KEY), AUTH_URI.encode('UTF-8'),md5).digest()
    hashed_key = base64.b64encode(hashed).decode()

    headers = {
        'Authorization': f'Bearer {API_KEY}:{hashed_key}'
    }
    token_request = requests.post(url= AUTH_URI, data = {}, headers=headers)
    ACCESS_TOKEN = token_request.json().get('Token')

    return ACCESS_TOKEN

# listing all the symtoms from the api


access_token = generate_token()

endpoint = f"{BASE_URI}/symptoms?token={access_token}&format=json&language=en-gb"
print(endpoint)
symptoms_request = requests.get(endpoint)
print(symptoms_request)
symptoms_request.encoding = 'utf-8-sig'

r = symptoms_request.json()
context = {}
for i in range(0, len(r)):
    ids = r[i]['ID']
    name = r[i]['Name']
    context.update({f'{ids}':f'{name}'})





print(context.get('10'))
    
    


    
    
