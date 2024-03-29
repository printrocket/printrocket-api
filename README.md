# Printrocket API Documentation v1.0

## Abstract

Printrocket allows users to collect & store lists of urls in order to compile into a final printed product.  The implementation somewhat resembles oauth, but without some of the more onerous requirements.

## Authentication
The Printrocket API requires some basic authentication in the form of a signature hash, which is comprised with at least a **client key**, a **secret key**, and a **nonce**.  Furthermore, any additional parameters (GET or POST) must be included in the signature

### Key Exchange
New users start out with an arbitrary client key, which can be a simple uuid that you'll generate on your end.  The user then must be forwarded to a url to authorize their client key as follows:

`http://printrocket.com/api/authorize/some-client-key/`

An optional callback can be specified in the form:

`...?callback=http://example.com/mycallback.html`

If the callback is provided, the user will be forwarded to the callback page once they complete authorization.

Once the user has authorized use of the api via their browser, you'll need to retrieve a secret key which you'll use going forward via the following url:

`http://printrocket.com/api/exchange/some-client-key/`

This url, if the user has successfully authorized use of the api, will return json containing the user's secret key. in the format:

`{"status": "ok", "secret_key": "the-users-secret_key"}`

This secret key is then used in all calls going forward along with the client key from before.

### Signature calculation
Base strings are calculated by taking the path of the request.  Then, clients must sort the keys of the parameters being sent, and then appending them as you would an http POST string, for example a call to `/lists/` with the following params:

`{'client_key': 'abc', 'nonce': '123', 'a_param': 'xyz'}` 

Would compute a base string as:

`/lists/ a_param=xyz&client_key=abc&nonce=123`

The base string is then hashed via hmac-sha256 with the **secret key** value as the key, and the base string as the message to hash.

Finally, the computed signature is then either attached to the querystring (in GET requests) or the post values (in POST request).

## General Format

Beyond the initial key exchange, requests are simple HTTP GET & POST requests.  Responses are in JSON, and try to conform to standard HTTP response codes.  POST requests contain a typical x-www-form-urlencoded querystring.

Generally, the response formats will include some variant of the following:

* success: `{'status': 'ok', 'message': 'some message'}`
* failure: `{'status': 'error', 'message': 'some error message'}`

## Calls

### Lists
* GET /lists/
	* Response: `{"status": "ok", "lists": [{"length": 1, "name": "My List"}]}`
* POST /lists/
	* Postbody: `list-name=mylist`
* GET /lists/\<listname\>/delete
	* Response: `{"status": "ok", "message": "deleted"}`

### Articles
* GET /lists/\<listname\>/
	* Response: `{"status": "ok", "articles": [{"url": "http://www.bbc.co.uk/news/technology-16543497", "title": "BBC News - IBM researchers make 12-atom magnetic memory bit"}]}`
* POST /lists/\<listname\>/
	* Postbody: `url=http%3A%2F%2Fwww.bbc.co.uk%2Fnews%2Ftechnology-16543497&title=BBC%20News%20-%20IBM%20researchers%20make%2012-atom%20magnetic%20memory%20bit`
* POST /lists/\<listname\>/delete-article/
	* Postbody: `url=http%3A%2F%2Fwww.bbc.co.uk%2Fnews%2Ftechnology-16543497`
