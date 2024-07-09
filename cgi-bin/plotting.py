#!/usr/bin/env python3

import json
import pymysql
import cgi
import cgitb
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

print("Content-type: application/json\n")

form = cgi.FieldStorage()
l_id = form.getvalue('l_id')
clutch_number = form.getvalue('clutch_number')

def fetch_data(l_id, clutch_number):
    data = {'series': []}
    try:
        # connection = pymysql.connect(host='bioed.bu.edu',
        #                    user='camv',
        #                    password='camv',
        #                    db='Team_4',
        #                    port=4253)
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            if clutch_number == "All":
                query = "SELECT collection_date, egg_papers, clutch_number FROM clutch WHERE l_id = %s ORDER BY collection_date, clutch_number"
                cursor.execute(query, (l_id,))
                data['series'] = {}
                for date, egg_papers, clutch_num in cursor.fetchall():
                    date_str = date.strftime('%Y-%m-%d')
                    if clutch_num not in data['series']:
                        data['series'][clutch_num] = {'label': f"Clutch {clutch_num}", 'data': []}
                    data['series'][clutch_num]['data'].append([date_str, egg_papers])
                data['series'] = list(data['series'].values())

            else:
                query = "SELECT collection_date, egg_papers FROM clutch WHERE l_id = %s AND clutch_number = %s ORDER BY collection_date"
                cursor.execute(query, (l_id, clutch_number))
                series_data = []
                for date, egg_papers in cursor.fetchall():
                    date_str = date.strftime('%Y-%m-%d')
                    series_data.append([date_str, egg_papers])
                data['series'] = [{'label': f"Clutch {clutch_number}", 'data': series_data}]
                
    except pymysql.MySQLError as e:
        print(json.dumps({'error': str(e)}))
    finally:
        if connection:
            connection.close()
    return data

if l_id is not None:
    if clutch_number is not None:
        print(json.dumps(fetch_data(l_id, clutch_number)))
    else:
        print(json.dumps({'error': 'Invalid clutch number'}))
else:
    print(json.dumps({'error': 'Invalid line ID'}))
