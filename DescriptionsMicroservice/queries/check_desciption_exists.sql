-- :name check_description_exists :scalar
SELECT EXISTS(SELECT 1 FROM descriptions WHERE creator = :user_guid AND track_id = :track_guid);