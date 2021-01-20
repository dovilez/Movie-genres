import os

import psycopg2

db_connection = psycopg2.connect(
    database="darma2fl7gg2uo",
    user="rebouvprxuiitt",
    password="818f30dcd7f091b2764b0edc489f676a390a5c6ac669b0c13bc1b2620c4f0d96",
    host="ec2-54-78-127-245.eu-west-1.compute.amazonaws.com",
    port="5432",
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
