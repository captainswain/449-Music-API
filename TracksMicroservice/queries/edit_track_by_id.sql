-- :name edit_track_by_id :affected
UPDATE tracks
SET title = :title, album_title = :album_title, artist = :artist, track_length = :track_length
WHERE id = :id;
