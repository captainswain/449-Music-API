set -e
set -x


# create keyspace
docker exec -it scylla cqlsh -e "DROP KEYSPACE IF EXISTS music;"
docker exec -it scylla cqlsh -e "CREATE KEYSPACE music WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};"


# Create users table
docker exec -it scylla cqlsh -e "CREATE TABLE music.users (username TEXT, password TEXT, displayname TEXT, email TEXT, homepage TEXT,  PRIMARY KEY (username));"


# Create descriptions table
docker exec -it scylla cqlsh -e "CREATE TABLE music.descriptions (guid uuid, creator TEXT, track_guid uuid, description TEXT, PRIMARY KEY (guid));"


# Create playlists table
docker exec -it scylla cqlsh -e "CREATE TABLE music.playlists (guid uuid, title TEXT, playlist_description TEXT, creator TEXT, PRIMARY KEY (guid));"

# Create playlist_tracks table
docker exec -it scylla cqlsh -e "CREATE TABLE music.playlist_tracks (playlist_guid uuid, track_guid uuid, PRIMARY KEY (playlist_guid,track_guid));"


# Tracks
docker exec -it scylla cqlsh -e "CREATE TABLE music.tracks (guid uuid, title TEXT, album_title TEXT, artist TEXT, track_length INT, media_url TEXT, album_art_url TEXT, PRIMARY KEY (guid));"

