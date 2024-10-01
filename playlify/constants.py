API_BASE_URL = 'https://api.spotify.com/v1/'

# TODO: probably shouldn't store client ID's etc out in the open
CLIENT_ID = '???'
CLIENT_SECRET = '???'
TOKEN_URL = 'https://accounts.spotify.com/api/token' # to refresh token

# the amount of playlist we process based on the mood
PLAYLIST_AMOUNT = 5

# the offset used to get playlists 
# (i.e. if this is 3, the first three playlists Spotify Search returns are skipped)
PLAYLIST_OFFSET = 0

# the amount of tracks we process per Spotify Search call
TRACK_AMOUNT = 5

# the offset used to get tracks
# (i.e. if this is 4, the first four playlists Spotify Search returns are skipped)
TRACK_INDIVIDUAL_OFFSET = 4
TRACK_COUPLED_OFFSET = 0


