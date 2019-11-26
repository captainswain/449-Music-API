-- :name user_by_guid :one
SELECT username, displayname, email, homepage FROM users
WHERE guid = :guid;
