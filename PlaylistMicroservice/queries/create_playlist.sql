-- :name create_playlist :insert
INSERT INTO playlists(guid, title, playlist_description, creator) VALUES (:guid, :title, :playlist_description, :creator);