# 449-Music-API
Shane Lindsay
Albert Balbon
Juan Vargas

## Getting started

```
pip3 install -r requirements.txt
pip3 install --user Flask Flask-API python-dotenv
sudo apt install --yes ruby-foreman

( Then log out and lock back in)

sqlite3 main.db < UsersMicroservice/users.sql
sqlite3 main.db < TracksMicroservice/tracks.sql
sqlite3 main.db < DescriptionsMicroservice/descriptions.sql
sqlite3 main.db < PlaylistMicroservice/playlist.sql
sqlite3 main.db < PlaylistMicroservice/playlists.sql

foreman start


```

## Testing

```
python3 Testing/populate_tables.py 
```
