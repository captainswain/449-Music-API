BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;

CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    track_length INTEGER,
    media_url VARCHAR,
    album_art_url VARCHAR
);


COMMIT;