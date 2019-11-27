-- :name add_track_to_playlist :insert
INSERT INTO playlist_tracks(playlist_id, track_guid) VALUES (:playlist_id, :track_guid); 
