import json
import requests
import datetime
from secrets import spotify_user_id
from refresh import Refresh
import sqlalchemy
import sqlite3
import pandas as pd

class SaveSongs:
    def __init__(self):

        self.user_id = spotify_user_id
        self.spotify_token = ""

    def GetSongs(self): 

        print("Gettings recently played tracks")

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.spotify_token)
        }

        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

        r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)
        r_json = r.json()
        return r_json
        
    def CallRefresh(self):
        print("Refreshing Token...")

        refreshCaller = Refresh()
        
        self.spotify_token = refreshCaller.refresh()


DATABASE_LOCATION = "sqlite:///Spotify_Demo.sqlite"

if __name__ == "__main__":


    a = SaveSongs()
    a.CallRefresh()

    # Extract Step
    data = a.GetSongs()

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
    """
    if validity_check(song_df):
        print("Data Valid. Proceed to Load the data")
    """

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

    print("Loading the data into SQLite DB")
    try:
        song_df.to_sql("Spotify_Demo", engine, index=False, if_exists='append')
        print("Loaded successfully")
    except:
        print("Data already exists in the DB")

    conn.close()
    print("Database successfully closed")
