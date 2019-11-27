-- :name create_user :insert
INSERT INTO users(username, password, displayname, email, homepage)
VALUES(:username, :password, :displayname, :email, :homepage)