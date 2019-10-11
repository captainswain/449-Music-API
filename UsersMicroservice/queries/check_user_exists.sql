-- :name check_user_exists :scalar
SELECT EXISTS(SELECT 1 FROM users WHERE username= :username);
