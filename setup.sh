#!/usr/bin/env bash
RED='\033[0;31m'
GREEN='\033[0;32m'
LTBLUE='\033[1;34m'
NC='\033[0m' # No Color
echo -e "${GREEN}-----------------------------"
echo -e "Project 3 Installation Script: "
echo -e ""
echo -e "This script is going to install and prepare the following:"
echo -e "Docker, memcached, libmemcached-tools, and scylladb docker instance."
echo -e ""
echo -e "It will also (hopefully) replace the local cassandra IP addresses in the microservice sourcecode."
echo -e "-----------------------------${NC}"
read -p "Press enter to continue "
clear
echo -e "${GREEN}Updating system....${NC}"
sleep 1
sudo apt update
echo -e "${GREEN}Installing docker and memcached....${NC}"
sleep 1
sudo apt install --yes docker.io memcached libmemcached-tools
echo -e "${GREEN}Adding user to docker group....${NC}"
sleep 1
sudo usermod -aG docker $USER
echo -e "${GREEN}Creating scylladb docker instance....${NC}"
sleep 1
docker run --name scylla -d scylladb/scylla --smp 1 --memory 1G --overprovisioned 1 --developer-mode 1 --experimental 1
echo -e "${GREEN}Checking if scylladb is running.... ${NC}"
sleep 1
local_ip=$(docker exec -it scylla nodetool status | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
if [[ -z "$local_ip" ]]; then
  echo -e "${RED}Yikes It looks like something went wrong....${NC}"
  exit 1
elif [[ -n "$local_ip" ]]; then
  echo -e "${GREEN}Success! scylladb is now running at ${RED}$local_ip${GREEN}!"
  sleep 1
  echo -e "${GREEN}Replacing IP address in source....${NC}"
  echo -e "${GREEN} Replacing in ${NC} DescriptionsMicroservice/descriptions.py"
  sed -i "s/172.17.0.1/$local_ip/g" ./DescriptionsMicroservice/descriptions.py 
  sleep 1
  echo -e "${GREEN} Replacing in ${NC} PlaylistMicroservice/playlists.py"
  sed -i "s/172.17.0.1/$local_ip/g" ./PlaylistMicroservice/playlists.py
  sleep 1
  echo -e "${GREEN} Replacing in ${NC} TracksMicroservice/tracks.py"
  sed -i "s/172.17.0.1/$local_ip/g" ./TracksMicroservice/tracks.py
  sleep 1
  echo -e "${GREEN} Replacing in ${NC} UsersMicroservice/users.py"
  sed -i "s/172.17.0.1/$local_ip/g" ./UsersMicroservice/users.py
  sleep 1
fi
echo -e "${GREEN}Setting up database..... ${NC}"
sleep 2

echo -e "${GREEN} Creating Keyspace..... ${NC}"
# create keyspace
docker exec -it scylla cqlsh -e "DROP KEYSPACE IF EXISTS music;"
docker exec -it scylla cqlsh -e "CREATE KEYSPACE music WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};"
sleep 1

echo -e "${GREEN} Creating users table..... ${NC}"
# Create users table
docker exec -it scylla cqlsh -e "CREATE TABLE music.users (username TEXT, password TEXT, displayname TEXT, email TEXT, homepage TEXT,  PRIMARY KEY (username));"
sleep 1

echo -e "${GREEN} Creating descriptions table..... ${NC}"
# Create descriptions table
docker exec -it scylla cqlsh -e "CREATE TABLE music.descriptions (guid uuid, creator TEXT, track_guid uuid, description TEXT, PRIMARY KEY (guid));"
sleep 1

echo -e "${GREEN} Creating playlists table..... ${NC}"
# Create playlists table
docker exec -it scylla cqlsh -e "CREATE TABLE music.playlists (guid uuid, title TEXT, playlist_description TEXT, creator TEXT, PRIMARY KEY (guid));"

# Create playlist_tracks table
docker exec -it scylla cqlsh -e "CREATE TABLE music.playlist_tracks (playlist_guid uuid, track_guid uuid, PRIMARY KEY (playlist_guid,track_guid));"
sleep 1

echo -e "${GREEN} Creating tracks table..... ${NC}"
# Tracks
docker exec -it scylla cqlsh -e "CREATE TABLE music.tracks (guid uuid, title TEXT, album_title TEXT, artist TEXT, track_length INT, media_url TEXT, album_art_url TEXT, PRIMARY KEY (guid));"

echo -e "${LTBLUE} All done here boss! Let's get grading :-) ${NC}"

