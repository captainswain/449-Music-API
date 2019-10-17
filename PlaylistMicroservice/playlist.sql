PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists (
    id INTEGER primary key,
    title VARCHAR,
    playlist_description TEXT,
    creator VARCHAR,
    FOREIGN KEY(creator) REFERENCES users(username)
);

INSERT INTO playlists(title, playlist_description, creator) VALUES ('Study Time', 'Playlist for studying', 'swain');

COMMIT;