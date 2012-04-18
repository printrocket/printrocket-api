#!/usr/bin/env python
import requests
import uuid
import hashlib
import hmac
import json

ENDPOINT_BASE = 'http://printrocket.com/api'

client_key = str(uuid.uuid4())
print 'client key: %s' % (client_key)

# Start registering the key
authorize_url = '%s/authorize/%s' % (ENDPOINT_BASE, client_key)
print 'request secret key by going to: %s' % (authorize_url)

# Wait for authorization
raw_input('press enter once authorized:')

# Exchange the client key for a secret key
exchange_url = '%s/exchange/%s/' % (ENDPOINT_BASE, client_key)
r = requests.get(exchange_url)
resp = json.loads(r.text)
secret_key = str(resp['secret_key'])

print 'received: '
print resp

print 'secret key: %s' % (secret_key)

# Use the secret key to get all the lists belonging to the user
path = '/lists/'
nonce = str(uuid.uuid4())
base_string = '%s client_key=%s&nonce=%s' % (path, client_key, nonce)
signature = hmac.new(secret_key, base_string, hashlib.sha256).hexdigest()

print 'path: %s' % (path)
print 'signature base string: %s' % (base_string)
print 'signature: %s' % (signature)

lists_url = '%s%s?client_key=%s&nonce=%s&signature=%s' % (ENDPOINT_BASE, \
    path, client_key, nonce, signature)
print 'full url: %s' % (lists_url)

r = requests.get(lists_url)

print 'response: '
print r.text

raw_input('press enter to create new list item in unsorted (ctrl-c to quit):')

path = '/lists/unsorted/'
url = 'http://www.bbc.co.uk/news/technology-17740574'
title = 'Printrocket API Client Test Article'
base_string = '%s client_key=%s&nonce=%s&title=%s&url=%s' % (path, \
    client_key, nonce, title, url)
signature = hmac.new(secret_key, base_string, hashlib.sha256).hexdigest()

print 'path: %s' % (path)
print 'signature base string: %s' % (base_string)
print 'signature: %s' % (signature)

post_url = '%s%s' % (ENDPOINT_BASE, path)
r = requests.post(post_url, data={'client_key': client_key, \
    'nonce': nonce, 'title': title, 'url': url, 'signature': signature})

print 'response: '
print r.text
