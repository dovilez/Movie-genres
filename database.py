import os

import psycopg2

db_connection = psycopg2.connect(
    database=os.environ["DATABASE_NAME"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
    host=os.environ["DATABASE_HOST"],
    port=os.environ["DATABASE_PORT"],
)

cur = db_connection.cursor()

cur.execute(
    """
DROP TABLE IF EXISTS prediction;
CREATE table prediction (
  id serial PRIMARY key,
  input VARCHAR,
  output VARCHAR,
  time timestamp
)
"""
)


db_connection.commit()
db_connection.close()
