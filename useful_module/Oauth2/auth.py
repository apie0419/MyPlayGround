from oauthlib.oauth2 import WebApplicationClient
import requests, json, time

class FacebookAuth(object):
    
    AUTHORIZATION_ENDPOINT_URL = "https://www.facebook.com/v4.0/dialog/oauth"
    TOKEN_ENDPOINT_URL         = "https://graph.facebook.com/v4.0/oauth/access_token"
    USERINFO_ENDPOINT_URL      = "https://graph.facebook.com/me"

    def __init__(self, client_id, client_secret):
        self.CLIENT_ID     = client_id
        self.CLIENT_SECRET = client_secret
        self.client        = WebApplicationClient(self.CLIENT_ID)

    def get_requests_uri(self, redirect_uri, scope):

        
        request_uri = self.client.prepare_request_uri(
            self.AUTHORIZATION_ENDPOINT_URL,
            redirect_uri = redirect_uri,
            scope = scope,
            state = str(time.time())
        )

        return request_uri

    def get_user_info(self, code, redirect_url):
        
        token_url, headers, body = self.client.prepare_token_request(
            self.TOKEN_ENDPOINT_URL,
            client_secret = self.CLIENT_SECRET,
            client_id = self.CLIENT_ID,
            redirect_url = redirect_url,
            code = code
        )

        token_response = requests.post(
            token_url,
            headers = headers,
            data = body,
            auth = (self.CLIENT_ID, self.CLIENT_SECRET),
        )

        self.client.parse_request_body_response(json.dumps(token_response.json()))

        uri, headers, body = self.client.add_token(self.USERINFO_ENDPOINT_URL)

        params = {
            "fields": "email,name"
        }

        userinfo_response = requests.get(uri, headers = headers, params = params)

        return userinfo_response.json()

class GoogleAuth(object):

    AUTHORIZATION_ENDPOINT_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT_URL         = "https://oauth2.googleapis.com/token"
    USERINFO_ENDPOINT_URL      = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, client_id, client_secret):
        self.CLIENT_ID     = client_id
        self.CLIENT_SECRET = client_secret
        self.client        = WebApplicationClient(self.CLIENT_ID)

    def get_requests_uri(self, redirect_uri, scope):

        
        request_uri = self.client.prepare_request_uri(
            self.AUTHORIZATION_ENDPOINT_URL,
            redirect_uri = redirect_uri,
            scope = scope,
            state = str(time.time())
        )

        return request_uri

    def get_user_info(self, code, redirect_url):
        
        token_url, headers, body = self.client.prepare_token_request(
            self.TOKEN_ENDPOINT_URL,
            client_secret = self.CLIENT_SECRET,
            client_id = self.CLIENT_ID,
            redirect_url = redirect_url,
            code = code
        )

        token_response = requests.post(
            token_url,
            headers = headers,
            data = body,
            auth = (self.CLIENT_ID, self.CLIENT_SECRET),
        )

        self.client.parse_request_body_response(json.dumps(token_response.json()))

        uri, headers, body = self.client.add_token(self.USERINFO_ENDPOINT_URL)

        userinfo_response = requests.get(uri, headers = headers)

        if userinfo_response.json().get("email_verified"):
            _id = userinfo_response.json()["sub"]
            email = userinfo_response.json()["email"]
            name = userinfo_response.json()["given_name"]

            return {
                "id": _id,
                "email": email,
                "name": name
            }
        else:
            return {}