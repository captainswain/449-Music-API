-- :name create_description :insert
INSERT INTO descriptions(creator, track_id, description)
VALUES(:username, :track_id, :description)