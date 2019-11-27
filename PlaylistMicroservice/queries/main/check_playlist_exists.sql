-- :name check_playlist_exists :scalar
SELECT EXISTS(SELECT 1 FROM playlists WHERE title= :title);