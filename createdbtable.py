import sqlalchemy as sqla


URI = "database-test1.ckvmcnbipeqn.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "picto"
PASSWORD = "Comp30830"

engine = sqla.create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# Create the database dbbikes
sql = """
CREATE DATABASE IF NOT EXISTS dbbikes;
"""
conn = engine.connect()
result = conn.execute(sqla.text(sql))
print(result)

# Create table station containing station information
createsttsql = """
CREATE TABLE IF NOT EXISTS station(
address VARCHAR(115),
banking VARCHAR(115),
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(115),
name VARCHAR(115),
number INTEGER,
position_lat REAL,
position_lng REAL,
status VARCHAR(115)
)"""

try:
    res = conn.execute(sqla.text("DROP TABLE IF EXISTS station"))
    res = conn.execute(sqla.text(createsttsql))
    print(res.fetchall())
except Exception as e:
    print(e)

# Create table availability containing bikes and bike stands information
createavtsql = """
CREATE TABLE IF NOT EXISTS availability(
number INTEGER,
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update INTEGER)
"""
try:
    res = conn.execute(sqla.text(createavtsql))
    print(res.fetchall())
except Exception as e:
    print(e)