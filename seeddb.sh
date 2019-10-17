#!/bin/bash
sqlite3 main.db < UsersMicroservice/users.sql
sqlite3 main.db < TracksMicroservice/tracks.sql
sqlite3 main.db < DescriptionsMicroservice/descriptions.sql
sqlite3 main.db < PlaylistMicroservice/playlist.sql
sqlite3 main.db < PlaylistMicroservice/playlists.sql