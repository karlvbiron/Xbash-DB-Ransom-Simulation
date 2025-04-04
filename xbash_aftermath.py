import pymongo
import mysql.connector
import psycopg2
import redis
from elasticsearch import Elasticsearch
import oracledb
import logging
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_mongodb():
    """Check MongoDB contents"""
    try:
        client = pymongo.MongoClient("mongodb://root:example@192.168.1.11:27017/")
        db = client["my_database"]
        collections = db.list_collection_names()
        
        print("\n=== MongoDB Status ===")
        print(f"Collections found: {collections}")
        
        if "WARNING" in collections:
            data = list(db["WARNING"].find())
            print("\nWARNING collection contents:")
            print(data)
        
        if "users" in collections:
            print("\nOriginal 'users' collection still exists")
            
    except Exception as e:
        logger.error(f"MongoDB check failed: {str(e)}")

def check_mysql():
    """Check MySQL contents"""
    try:
        conn = mysql.connector.connect(
            host="192.168.1.12",
            user="root",
            password="example",
            database="my_database"
        )
        cursor = conn.cursor()
        
        print("\n=== MySQL Status ===")
        
        # Get list of tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables found: {[table[0] for table in tables]}")
        
        # Check WARNING table contents if it exists
        if ('WARNING',) in tables:
            cursor.execute("SELECT * FROM WARNING")
            data = cursor.fetchall()
            print("\nWARNING table contents:")
            print(tabulate(data, headers=cursor.column_names))
            
        if ('users',) in tables:
            print("\nOriginal 'users' table still exists")
            
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"MySQL check failed: {str(e)}")

def check_postgresql():
    """Check PostgreSQL contents"""
    try:
        conn = psycopg2.connect(
            host="192.168.1.13",
            database="my_database",
            user="postgres",
            password="example"
        )
        cursor = conn.cursor()
        
        print("\n=== PostgreSQL Status ===")
        
        # Get list of tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"Tables found: {[table[0] for table in tables]}")
        
        # Check WARNING table contents if it exists
        if ('warning',) in tables:
            cursor.execute('SELECT * FROM "warning"')
            data = cursor.fetchall()
            print("\nWARNING table contents:")
            print(tabulate(data, headers=['id', 'message']))
            
        if ('users',) in tables:
            print("\nOriginal 'users' table still exists")
            
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"PostgreSQL check failed: {str(e)}")

def check_redis():
    """Check Redis contents"""
    try:
        r = redis.Redis(host='192.168.1.14', port=6379, db=0)
        
        print("\n=== Redis Status ===")
        
        # Check all keys
        keys = r.keys('*')
        print(f"Keys found: {[key.decode('utf-8') for key in keys]}")
        
        # Check WARNING key if it exists
        if b'WARNING' in keys:
            warning_data = r.get('WARNING')
            print("\nWARNING key contents:")
            print(warning_data.decode('utf-8'))
            
        # Check if any user keys still exist
        user_keys = r.keys('user:*')
        if user_keys:
            print("\nOriginal user keys still exist:", 
                  [key.decode('utf-8') for key in user_keys])
            
    except Exception as e:
        logger.error(f"Redis check failed: {str(e)}")

def check_elasticsearch():
    """Check Elasticsearch contents"""
    try:
        es = Elasticsearch(['http://192.168.1.15:9200'])
        
        print("\n=== Elasticsearch Status ===")
        
        # Get list of indices
        indices = es.indices.get_alias().keys()
        print(f"Indices found: {list(indices)}")
        
        # Check WARNING index if it exists
        if 'warning' in indices:
            result = es.search(index='warning')
            print("\nWARNING index contents:")
            for hit in result['hits']['hits']:
                print(hit['_source'])
                
        if 'users' in indices:
            print("\nOriginal 'users' index still exists")
            
    except Exception as e:
        logger.error(f"Elasticsearch check failed: {str(e)}")

def check_oracle():
    """Check Oracle contents"""
    try:
        conn = oracledb.connect(
            user="my_database",
            password="my_password",
            dsn="192.168.1.16:1521/MYDB"
        )
        cursor = conn.cursor()
        
        print("\n=== Oracle Status ===")
        
        # Get list of tables
        cursor.execute("""
            SELECT table_name 
            FROM user_tables
        """)
        tables = cursor.fetchall()
        print(f"Tables found: {[table[0] for table in tables]}")
        
        # Check WARNING table contents if it exists
        if ('WARNING',) in tables:
            cursor.execute("SELECT * FROM WARNING")
            data = cursor.fetchall()
            print("\nWARNING table contents:")
            print(tabulate(data, headers=['id', 'message']))
            
        if ('users',) in tables:
            print("\nOriginal 'users' table still exists")
            
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Oracle check failed: {str(e)}")

def check_all_databases():
    """Check all databases"""
    print("Starting database verification...")
    
    #check_functions = [
    #    check_mongodb,
    #    check_mysql,
    #    check_postgresql,
    #    check_redis,
    #    check_elasticsearch,
    #    check_oracle
    #]
    
    check_functions = [
        check_mongodb,
        check_mysql,
        check_postgresql,
        check_redis,
        check_elasticsearch,
        check_oracle
    ]
    
    for check in check_functions:
        try:
            check()
            print("\n" + "-"*50)
        except Exception as e:
            logger.error(f"Failed to run {check.__name__}: {str(e)}")
            print("\n" + "-"*50)

if __name__ == "__main__":
    check_all_databases()
