"""
Client_ID = 'b985d010454647eea7f72cf5d74f28a8'
Client_Secret = '9fda216d666b47148ff302c97109c723'

https://accounts.spotify.com/authorize?client_id=b985d010454647eea7f72cf5d74f28a8&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=user-read-recently-played

b985d010454647eea7f72cf5d74f28a8:9fda216d666b47148ff302c97109c723

curl -H "Authorization: Basic Yjk4NWQwMTA0NTQ2NDdlZWE3ZjcyY2Y1ZDc0ZjI4YTg6OWZkYTIxNmQ2NjZiNDcxNDhmZjMwMmM5NzEwOWM3MjM=" -d grant_type=authorization_code -d code=AQBGZv_ESw9OJGrUApsah8fszW0fmKVE2rgOV2HEbAK6E7tqYbnb8hgEwv0DJuUSpXRlA3is50vWXC-M9An34j6SAWmtoxAoHNjpaTJMdmQsUgWzMliYdwwRSetj8xNQO6wRNsIZoz-SgkaBvYkbQ24JeIZFlBXIJ4adSgPjCaFFJ_5od7lNHJV6Deo6UEUI1w -d redirect_uri=https%3A%2F%2Flocalhost%2F https://accounts.spotify.com/api/token
"""

#spotify_token = 'BQBE7F9fYXmof3ri1pYSolJ-yCyLxWc62J3DsOKwEwrysaBhgPYL6aBP9Who0t1zRxjY0sg8cpNWECwDD3sLE8mYDR_gJo__2IittvfthLk-9N5eDZOzq48QEQP5XNcyqI75Z2X5WA_CPrCwEp8qwMqNZYqmvP9WEvBC'
spotify_user_id = 'LeX'
refresh_token = Secrets.refresh_token
base64_encoded = Secrets.base64_encoded
