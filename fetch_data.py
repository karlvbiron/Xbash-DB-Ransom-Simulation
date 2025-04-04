import pymongo
import mysql.connector
import psycopg2
import redis
from elasticsearch import Elasticsearch
import os
import cx_Oracle

# MongoDB
def fetch_mongo_data():
    client = pymongo.MongoClient("mongodb://root:example@192.168.1.11:27017/")
    db = client["my_database"]
    collection = db["my_table"]
    data = collection.find({})
    print("\nMongoDB Data:")
    for doc in data:
        print(doc)

# MySQL
def fetch_mysql_data():
    conn = mysql.connector.connect(
        host="192.168.1.12",
        user="root",
        password="example",
        database="my_database"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table;")
    rows = cursor.fetchall()
    print("\nMySQL Data:")
    for row in rows:
        print(row)

# PostgresSQL
def fetch_postgres_data():
    conn = psycopg2.connect(
        host="192.168.1.13",
        user = "postgres",
        password="example",
        dbname="my_database"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table;")
    rows = cursor.fetchall()
    print("\nPostgreSQL Data")
    for row in rows:
        print(row)

# Redis
def fetch_redis_data():
    try:
        # Connect to the Redis server
        r = redis.Redis(host='192.168.1.14', port=6379, decode_responses=True)

        # Use SCAN to find all keys matching the pattern "*user*"
        cursor = 0
        pattern = '*user*'

        print("\nRedis Data:")

        # Loop through all matching keys and fetch their hash data
        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern)
            for user_key in keys:
                # Check if the key is a hash (optional)
                if r.type(user_key) == 'hash':
                    user_data = r.hgetall(user_key)
                    if user_data:
                        print(f"Data for {user_key}:")
                        for field, value in user_data.items():
                            print(f"  {field}: {value}")
                    else:
                        print(f"No data found for {user_key}.")

            # If the cursor is 0, the scan is complete
            if cursor == 0:
                break

    except redis.ConnectionError:
        print("Could not connect to the Redis server.")

# Elasticsearch
def fetch_es_data():
    es = Elasticsearch([{'host': '192.168.1.15','port': 9200, 'scheme': 'http'}])
    res = es.search(index="my_index", body={"query": {"match_all": {}}})
    print("\nElasticsearch Data:")
    for hit in res['hits']['hits']:
        print(hit["_source"])

# OracleDB
def fetch_oracledb_data():
    # Set Oracle Client library path
    os.environ['ORACLE_HOME'] = '/opt/oracle/instantclient_19_19'
    os.environ['LD_LIBRARY_PATH'] = '/opt/oracle/instantclient_19_19'
    
    # Database connection details
    host = "192.168.1.16"
    port = 1521
    #service_name = "MYPDB"
    service_name = "MYDB"
    user = "my_database"
    password = "my_password"
    
    # Connect to the Oracle database
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    
    print("\nOracleDB Data:")
    
    try:
        cursor = connection.cursor()
        
        # Execute a query to select all data from my_table
        cursor.execute("SELECT * FROM my_table")
        
        # Fetch and print all rows from the table
        rows = cursor.fetchall()
        for row in rows:
            print(f"First Name: {row[0]}, Last Name: {row[1]}, Email: {row[2]}, Phone Number: {row[3]}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    fetch_mongo_data()
    fetch_mysql_data()
    fetch_postgres_data()
    fetch_redis_data()
    fetch_es_data()
    fetch_oracledb_data()
    print("\n")

