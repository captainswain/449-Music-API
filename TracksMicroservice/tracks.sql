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
    album_art_url VARCHAR
);

INSERT INTO tracks(title, album_title, artist, track_length, media_url)
VALUES('Stairway to Heaven', 'Led Zeppelin IV', 'Led Zeppelin', '/home/music/stair2hvn.mp3', 482);
INSERT INTO tracks(Title, album_title, artist, track_length, media_url)
VALUES('Bohemian Rhapsody', 'A Night at the Opera', 'Queen', '/home/music/bohemianrhap.mp3', 355);
COMMIT;