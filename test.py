from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])


session = cluster.connect()

session.set_keyspace('music')

rows = session.execute('SELECT username, password, email FROM users')
for user_row in rows:
    print (user_row.username, user_row.password, user_row.email)



session.execute(
    """
    INSERT INTO users (username, password, email)
    VALUES (%s, %s, %s)
    """,
    ("John O'Reilly", "slick", "thick boy")
)

session.execute(
    """
    INSERT INTO descriptions (guid, creator, track_guid, description)
    VALUES (uuid(), %s, uuid(), %s)
    """,
    ("slick", "thick boy")
)

rows = session.execute('SELECT * FROM descriptions')
for user_row in rows:
    print (user_row)