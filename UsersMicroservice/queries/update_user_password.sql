-- :name update_user_password :affected
update users set password = :new_password
where username = :username