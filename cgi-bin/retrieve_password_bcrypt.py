import sys
import pymysql
import json
import bcrypt
import configparser

inputString = sys.argv[1]

# Read configuration file
config = configparser.ConfigParser()
config.read('../config/user.ini')

# Get database configuration
db_config = {
    'host': config['database']['host'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'db': config['database']['db'],
    'port': int(config['database']['port'])
}

# Connect to MySQL
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Execute MySQL query to fetch the stored hash
    cursor.execute("SELECT pass FROM login_password")
    row = cursor.fetchone()

    match = False
    while row:
        stored_hash = row[0].encode()  # Fetch the stored hash
        if bcrypt.checkpw(inputString.encode(), stored_hash):
            match = True
            break
        row = cursor.fetchone()

    # Format response as JSON
    response = {'match': match}
    print(json.dumps(response))  # Output JSON response

except pymysql.Error as e:
    print(json.dumps({'match': False, 'error': str(e)}))  # Output JSON error response

finally:
    if connection:
        connection.close()
