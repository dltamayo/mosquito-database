import sys
import pymysql
import json
import hashlib
import configparser

inputString = sys.argv[1]

# Hash the input string
hashedInput = hashlib.sha256(inputString.encode()).hexdigest()

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

    # Execute MySQL query
    cursor.execute("SELECT pass FROM login_password WHERE pass = %s", (hashedInput,))
    row = cursor.fetchone()

    # Format response as JSON
    if row:
        response = {'match': True}
    else:
        response = {'match': False}

    print(json.dumps(response))  # Output JSON response

except pymysql.Error as e:
    print(json.dumps({'match': False, 'error': str(e)}))  # Output JSON error response

finally:
    if connection:
        connection.close()
