# Spotify-ETL-Pipeline

[Spotify Web API](https://developer.spotify.com/documentation/web-api/):
  The Spotify Web API provides a wealth of information on nearly all music within the Spotify catalog. From the API, you can get information on artists, tracks, albums, as well as both low and high-level audio analysis information. This project is a simple demonstration of using the Spotify Web API.

ETL Pipeline using Python (Jupyter Notebook & VS Code)

1. Extract the metadata of all the user's recently played tracks from [Spotify API](https://developer.spotify.com) using requests library.
2. Transform the extracted JSON data (Semi-Structured data) to a Pandas Dataframe (Structured data) using Pandas library and perform data validation.
3. Load the data into a SQL DB (SQLite) using SQLite library in python.

What is happening in the Back-end?
  Automated the process of obtaining the "Access token" using a "Refresh token" by implementing an [Authorization code flow](https://developer.spotify.com/documentation/general/guides/authorization/) process in order to authorize the access of user's [recently played tracks](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recently-played) using a *GET* request.

Upcoming:
- Extract
  - High-level audio features for tracks 
  - In-depth audio analysis for tracks
  and store it in the same DB
- Automate the whole process using Apache Airflow.

What can be done using this DB you might ask:
  This DB has the metadata and audio features such as Bars, Beats, Sections, Segments (Pitches, Timbre), Tatums and Echoprint Data which can tell about acousticness, danceability, instrumentalness, liveness, speechiness and valence of the songs. These data can be utilized to create a customized song recommendation.
  
Credits:
- [Karolina Sowinska](https://www.youtube.com/c/KarolinaSowinska) (ETL implementation)
- [Euan Morgan](https://github.com/EuanMorgan) (Authorization code flow)
- [Mark Koh](https://www.youtube.com/playlist?list=PLelwrr4wIIwQv7q9a6I00UsY0zYNtftAO) (Audio Analysis)
