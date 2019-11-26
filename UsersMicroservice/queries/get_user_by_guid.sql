-- :name get_user_by_guid :one
SELECT * FROM users
WHERE guid = :guid;
