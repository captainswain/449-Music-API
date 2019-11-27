-- :name create_description :insert
INSERT INTO descriptions(creator, track_guid, description)
VALUES(:creator, :track_guid, :description)