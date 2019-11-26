-- :name create_track :insert
INSERT INTO tracks(guid, title, album_title, artist, track_length, media_url, album_art_url)
VALUES(:guid, :title, :album_title, :artist, :track_length, :media_url, :album_art_url)