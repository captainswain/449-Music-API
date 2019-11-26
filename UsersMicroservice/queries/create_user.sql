-- :name create_user :insert
INSERT INTO users(guid, username, password, displayname, email, homepage)
VALUES(:guid, :username, :password, :displayname, :email, :homepage)