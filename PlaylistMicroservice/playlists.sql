PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS playlist_tracks;
CREATE TABLE playlist_tracks (
    playlist_id INTEGER,
    track_id INTEGER,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id),
    FOREIGN KEY(track_id) REFERENCES tracks(id)
);
COMMIT;