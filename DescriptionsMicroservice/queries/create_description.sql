-- :name create_description :insert
INSERT INTO descriptions(guid, creator, track_id, description)
VALUES(:guid, :user_guid, :track_guid, :description)