PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    track_length INTEGER,
    media_url VARCHAR,
    album_art_url VARCHAR,
);

INSERT INTO tracks(title, album_title, artist, track_length, media_url, album_art_url) VALUES('')