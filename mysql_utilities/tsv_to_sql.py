#!/usr/bin/env python3

import os
import pandas as pd
import pymysql
import configparser

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

# Path to the folder containing TSV files
TSV_FOLDER_PATH = 'younger_tsv'

# Define the order of table processing based on dependencies
table_order = ['m_lines.tsv', 'lab_members.tsv', 'clutch.tsv', 'sort.tsv', 'passage.tsv']

try:
    # Connect to the database
    connection = pymysql.connect(**db_config)

    with connection.cursor() as cursor:
        # Iterate over files in the specified order
        for filename in table_order:
            file_path = os.path.join(TSV_FOLDER_PATH, filename)
            if os.path.isfile(file_path) and filename.endswith(".tsv"):
                table_name = os.path.splitext(filename)[0]  # Extract table name from file name

                # Read TSV file into a DataFrame
                df = pd.read_csv(file_path, sep='\t')

                # Replace blanks with NULLs
                df = df.where(pd.notnull(df), None)

                # SQL query to create table (if not exists)
                create_table_query = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join([f'{col} VARCHAR(255)' for col in df.columns])}
                );
                '''
                cursor.execute(create_table_query)

                # Insert data into the table
                for index, row in df.iterrows():
                    insert_query = f'''
                    INSERT INTO {table_name} ({', '.join(df.columns)})
                    VALUES ({', '.join(['%s' for _ in range(len(df.columns))])});
                    '''
                    cursor.execute(insert_query, tuple(row))

                print(f"Data inserted successfully into the MySQL table: {table_name}")

    # Commit changes to the database
    connection.commit()
    print("All data inserted successfully into the MySQL tables.")

finally:
    # Close the database connection
    connection.close()
