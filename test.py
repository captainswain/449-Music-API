from cassandra.cluster import Cluster
import uuid
cluster = Cluster(['172.17.0.2'])


session = cluster.connect()

session.set_keyspace('music')

# rows = session.execute('SELECT username, password, email FROM users')
# for user_row in rows:
#     print (user_row.username, user_row.password, user_row.email)



# session.execute(
#     """
#     INSERT INTO users (username, password, email)
#     VALUES (%s, %s, %s)
#     """,
#     ("John O'Reilly", "slick", "thick boy")
# )
# session.execute(
#     """
#     INSERT INTO descriptions (guid, creator, track_guid, description)
#     VALUES (uuid(), %s, uuid(), %s)
#     """,
#     ("slick", "thick boy")
# )

# rows = session.execute('SELECT * FROM descriptions')
# for user_row in rows:
#     print (user_row)
 


session.execute(
    """
    INSERT INTO descriptions (guid, creator, track_guid, description)
    VALUES (%s, %s, %s, %s)
    """,
    (uuid.uuid1(), "FatDickCharly", uuid.uuid1(), "FatDickCharly")
)

#print (str(uuid.uuid1()))

#  # for testing lets put a fake uuid
#  # AND track_guid= uuid()
# checkDesc = session.execute(
#     """
#     SELECT * FROM descriptions WHERE creator=%s AND track_guid= %s
#     ALLOW FILTERING
#     """
# )
checkDesc = session.execute(
    """
    SELECT * FROM descriptions WHERE creator=%s AND track_guid=%s
    ALLOW FILTERING;
    """,
    ("carl", uuid.UUID('d2059a20-1c9c-11ea-9ef7-7146b93e28ab'))
)
# run the program
# My terminal is botched
if (checkDesc.one() is None):
    print("WE DONT GOT NO ROWS BOSS")
else:
    print("wE gOt SomE rOWs DAD")


# Okay so now we got exactly what was written in mysql written using cassandra
