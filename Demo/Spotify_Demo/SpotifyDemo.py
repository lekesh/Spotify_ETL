import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime
import datetime
import sqlite3

import base64

client_id = 'b985d010454647eea7f72cf5d74f28a8'
client_secret = '9fda216d666b47148ff302c97109c723'

class SpotifyToken(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"


    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_creds(self): # returns base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("Set Client ID and Secret values")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_creds()
        return {
                "Authorization": f"Basic {client_creds_b64}",
                "Content-Type": "application/x-www-form-urlencoded"
        }

    def get_token_body_para(self):
        return {"grant_type": "client_credentials"}

    def perform_authentication(self):
        token_url = self.token_url
        token_body_para = self.get_token_body_para()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_body_para, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        access_token = r.json()['access_token']
        expires_in = r.json()['expires_in'] # in seconds
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True


DATABASE_LOCATION = "sqlite:///Spotify_Demo.sqlite"
USER_ID = "LeX" # Spotify username

def validity_check(df: pd.DataFrame) -> bool:
    
    # Check if no songs played
    if df.empty:
        print("No songs streamed in the past 24 hours")
        return False
    
    # Duplicate Primary Key check
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Duplicate Primary keys are found")
    
    # Check for NULL values
    if df.isnull().values.any():
        raise Exception("Null values found")
    
    # Check if all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamps = df["timestamp"].tolist()
    
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one song does not have yesterday's timestamp")
    
    return True


if __name__ == "__main__":

    client = SpotifyToken(client_id, client_secret)
    if client.perform_authentication():
        TOKEN = client.access_token
        print("Fresh Token Value: ", client.access_token)

    # Extract Step

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name","artist_name","played_at","timestamp"])


    # Transformation Step

    if validity_check(song_df):
        print("Data Valid. Proceed to Load the data")


    # Load step

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('Spotify_Demo.sqlite')
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS Spotify_Demo(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """
    cursor.execute(query)
    print("Database successfully opened")

    try:
        song_df.to_sql("Spotify_Demo", engine, index=False, if_exists='append')
        print("Loaded successfully")
    except:
        print("Data already exists in the DB")

    conn.close()
    print("Database successfully closed")
