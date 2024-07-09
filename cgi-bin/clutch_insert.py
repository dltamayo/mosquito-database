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
        m_id = form.getvalue('name')  # Assuming m_id corresponds to 'name' dropdown
        l_id = form.getvalue('genotype')  # Assuming l_id corresponds to 'genotype' dropdown
        hatch_date = form.getvalue('hatch_date')
        collection_date = form.getvalue('collection-date')
        clutch_number = form.getvalue('clutch-number')
        egg_papers = form.getvalue('egg-papers')
        
        sql = """
        INSERT INTO clutch (
            m_id, l_id, hatch_date, collection_date, clutch_number, egg_papers
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(sql, (m_id, l_id, hatch_date, collection_date, clutch_number, egg_papers))
        connection.commit()
        print("Data inserted successfully")
except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()
