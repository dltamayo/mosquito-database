#!/usr/bin/env python3

import cgitb
import cgi
import pymysql
import configparser

cgitb.enable()
print("Content-type: text/html\n")

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

# Connect to the database
connection = pymysql.connect(**db_config)

# Parse form data
form = cgi.FieldStorage()

# Insert data
try:
    with connection.cursor() as cursor:
        f_name = form.getvalue('f_name')
        l_name = form.getvalue('l_name')
        role = form.getvalue('role')

        sql = """
        INSERT INTO lab_members (
            f_name, l_name, lab_role, active
        ) VALUES (
            %s, %s, %s, 'Active'
        );
        """
        cursor.execute(sql, (f_name, l_name, role))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()
