-- :name get_playlist_tracks :many
SELECT * FROM playlist_tracks
WHERE playlist_id = :id;