-- :name create_track :insert
INSERT INTO tracks(title, album_title, artist, track_length, media_url, album_art_url)
VALUES(:title, :album_title, :artist, :track_length, :media_url, :album_art_url)