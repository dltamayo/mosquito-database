#!/usr/bin/env python3

from datetime import date
import pymysql
import cgi
import cgitb
import json
import configparser

cgitb.enable()

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

# MySQL queries
l_id_dropdown = '''
SELECT l_id, GROUP_CONCAT(CONCAT_WS(' - ', yl_id, short_name)) AS 'ID - Name' 
FROM m_lines
GROUP BY l_id;
'''

m_id_dropdown = '''
SELECT m_id, GROUP_CONCAT(CONCAT_WS(' ', f_name, l_name)) AS full_name
FROM (SELECT * FROM lab_members WHERE active = 'Active') AS sub
GROUP BY m_id
ORDER BY full_name;
'''

hatch_date = '''
SELECT MAX(hatch_date)
FROM (SELECT l_id, hatch_date, 'passage' AS 'table'
	FROM passage p
	UNION
	SELECT l_id, hatch_date, 'sort' AS 'table'
	FROM sort
	UNION
	SELECT l_id, hatch_date, 'clutch' AS 'table'
	FROM clutch) AS sub
WHERE l_id = %s;
'''

bc_ib = '''
SELECT bc, ib
FROM passage p
WHERE l_id = %s
ORDER BY hatch_date DESC
LIMIT 1;
'''

#retrieve input data from the web server
form = cgi.FieldStorage() 

#next line is always required as first part of http output
print("Content-type: text/html\n")

if form:
    # Get submitted values
    selector = form.getvalue("selector")

    # Establish database connection
    try:
        connection = pymysql.connect(**db_config)

    except pymysql.Error as e:
        print(json.dumps({'error': str(e)}))
        exit()

    cursor = connection.cursor()

    try:
        if selector == 'l_id_dropdown':
            cursor.execute(l_id_dropdown)
            results = cursor.fetchall()
            print(json.dumps(results))

        elif selector == 'm_id_dropdown':
            cursor.execute(m_id_dropdown)
            results = cursor.fetchall()
            print(json.dumps(results))
        
        elif selector == 'hatch_date':
            l_id = form.getvalue("l_id", "")
            if l_id:
                cursor.execute(hatch_date, [l_id])
                result = cursor.fetchone()
                default_date = str(date.today()) if str(result[0]) == 'None' else str(result[0])
                print(json.dumps({'default_date': default_date}))
            else:
                print(json.dumps({'error': 'No line ID provided.'}))

        elif selector == 'bc_ib':
            l_id = form.getvalue("l_id", "")
            if l_id:
                cursor.execute(bc_ib, [l_id])
                results = cursor.fetchall()
                print(json.dumps(results))
            else:
                print(json.dumps({'error': 'No line ID provided.'}))

        else:
            print(json.dumps({'error': 'Invalid selector.'}))

    except pymysql.Error as e:
        print(json.dumps({'error': str(e)}))

    finally:
        connection.close()

else:
    print(json.dumps({'error': 'No form data received.'}))
