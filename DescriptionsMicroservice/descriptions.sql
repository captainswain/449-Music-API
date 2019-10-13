PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;


-- Each user can post their own description for a track. As with the playlist microservice, individual tracks are referred to by their URLs.
-- The following operations should be exposed:
-- Set a user’s description of a track
-- Retrieve a user’s description of a track

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
    id INTEGER primary key,
    creator VARCHAR,
    track_id INTEGER,
    description TEXT,
    FOREIGN KEY(creator) REFERENCES users(username)
    FOREIGN KEY(track_id) REFERENCES tracks(id)
);

INSERT INTO descriptions(creator, track_id, description) VALUES('Study Time', 'Playlist for studying', 'swain');