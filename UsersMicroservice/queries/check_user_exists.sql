-- :name check_user_exists :one
SELECT EXISTS(SELECT 1 FROM users WHERE username= :username);
