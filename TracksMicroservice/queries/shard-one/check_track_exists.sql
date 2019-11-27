-- :name check_track_exists :scalar
SELECT EXISTS(SELECT 1 FROM tracks WHERE media_url=:media_url);