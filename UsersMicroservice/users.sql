-- User table creation & seeding
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER primary key,
    username VARCHAR,
    password VARCHAR,     
    displayname VARCHAR,  
    email VARCHAR,
    homepage VARCHAR,
    UNIQUE(username)
);

INSERT INTO users(username, password, displayname, email) VALUES('swain','12345','SwaiNy','me@shane.cx');

COMMIT;