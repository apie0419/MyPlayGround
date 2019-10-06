## Usage

```python
from Oauth2 import GoolgeAuth, FacebookAuth
from flask import Flask, redirect

app = Flask(__name__)

googleauth = GoolgeAuth("<GOOGLE_CLIENT_ID>", "<GOOGLE_CLIENT_SECRET>")
fbauth     = FacebookAuth("<FACEBOOK_CLIENT_ID>", "<FACEBOOK_CLIENT_SECRET>")

@app.route("/Login/<string:TYPE>", methods = ["POST"])
def Login(TYPE):

    if TYPE == "Google":
        request_uri = googleauth.get_requests_uri(
            redirect_uri = request.url_root + "Callback/Google",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    elif TYPE == "Facebook":
        request_uri = fbauth.get_requests_uri(
            redirect_uri = request.url_root + "Callback/Facebook",
            scope = ["email", "public_profile"]
        )
    return redirect(request_uri)
        
@app.route("/Callback/<string:TYPE>")
def Callback(TYPE):
   
    code = request.args.get("code")
    if TYPE == "Google":
        userinfo = googleauth.get_user_info(
            code = code,
            redirect_url = request.base_url
        )
    elif TYPE == "Facebook":
        userinfo = fbauth.get_user_info(
            code = code,
            redirect_url = request.base_url
        )
    email = None
    _id   = userinfo["id"]
    name  = userinfo["name"]
    if "email" in userinfo:
        email = userinfo["email"]

    return "Login Successfully, Userid: {}, Name: {}, Email: {}".format(_id, name, email)

if __name__ == '__main__':
	app.run()

```

### We can use this module and implement the oauth2 feature quickly

### We need to run with HTTPS Protocol

### Redirect uri should set in [Google Console](https://console.cloud.google.com/apis) & [Facebook Developer](https://developers.facebook.com/apps)