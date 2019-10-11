-- :name user_by_id :one
SELECT username, displayname, email, homepage FROM users
WHERE id = :id;