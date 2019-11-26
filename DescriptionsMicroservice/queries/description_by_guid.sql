-- :name description_by_guid :one
SELECT * FROM descriptions
WHERE guid = :guid;
