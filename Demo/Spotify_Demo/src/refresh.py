import requests
import json
from secrets import refresh_token, base64_encoded

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base64_encoded
    
    def refresh(self):
        
        query = 'https://accounts.spotify.com/api/token'
        body_para = {"grant_type": "refresh_token","refresh_token":refresh_token}
        headers = {"Authorization": f"Basic {self.base_64}"}

        r = requests.post(query, data=body_para,headers=headers)
        r_json = r.json()
        return r_json["access_token"]

#a = Refresh()
#token = a.refresh()
#print("Freshly brewed token: {}".format(token))
