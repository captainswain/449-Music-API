import sqlite3
import uuid
from psycopg2.extensions import register_adapter, AsIs


sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


db_names = ["shard1.db", "shard2.db", "shard3.db"]

for i in range(len(db_names)):

    conn = sqlite3.connect(db_names[i], detect_types=sqlite3.PARSE_DECLTYPES)

    c = conn.cursor()

    # c.execute('CREATE TABLE test (guid GUID PRIMARY KEY, name TEXT)')

    # Create Tracks table
    c.execute('DROP TABLE IF EXISTS tracks;')
    c.execute('CREATE TABLE tracks (guid GUID PRIMARY KEY, title VARCHAR, album_title VARCHAR, artist VARCHAR, track_length INTEGER, media_url VARCHAR, album_art_url VARCHAR );')

    # Create Descriptions table
    c.execute('DROP TABLE IF EXISTS descriptions;')
    c.execute('CREATE TABLE descriptions (guid GUID PRIMARY KEY, creator VARCHAR, track_id INTEGER, description TEXT);')

    # Create Playlist table
    c.execute('DROP TABLE IF EXISTS playlists;')
    c.execute('CREATE TABLE playlists (guid GUID PRIMARY KEY, title VARCHAR, playlist_description TEXT, creator VARCHAR);')

    # Create Playlist_tracks table
    c.execute('DROP TABLE IF EXISTS playlist_tracks;')
    c.execute('CREATE TABLE playlist_tracks (playlist_guid GUID, track_guid GUID);')

    # Create users table
    c.execute('DROP TABLE IF EXISTS users;')
    c.execute('CREATE TABLE users (guid GUID PRIMARY KEY, username VARCHAR, password VARCHAR, displayname VARCHAR, email VARCHAR, homepage VARCHAR, UNIQUE(username) );')

# data = (uuid.uuid4(), 'foo')
# print ('Input Data:', data)
# c.execute('INSERT INTO tracks VALUES (?,?,?)', data)

# c.execute('SELECT * FROM tracks')
# print ('Result Data:', c.fetchone())



