-- :name check_description_exists :scalar
SELECT EXISTS(SELECT 1 FROM descriptions WHERE creator = :creator AND track_id = :track_id);