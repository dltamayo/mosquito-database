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
        # Step 1: Retrieve the next yl_id
        cursor.execute("""
            SELECT CONCAT('YL', LPAD(SUBSTRING(yl_id, 3) + 1, 3, '0')) AS next_yl_id
            FROM m_lines
            ORDER BY yl_id DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        next_yl_id = result[0] if result else 'YL001'  # Handle case where there are no records

        # Step 2: Insert the data with the retrieved yl_id
        sql = """
        INSERT INTO m_lines (
            yl_id,
            short_name, full_genotype, background, published, authors,
            creators,
            phenotype, phenotype_notes, genotype_notes, dna_avail,
            notes, maintenance
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(sql, (
            next_yl_id,
            form.getvalue('short_name', None),
            form.getvalue('full_genotype', None),
            form.getvalue('background', None),
            form.getvalue('published', None),
            form.getvalue('authors', None),
            form.getvalue('creators', None),
            form.getvalue('phenotype', None),
            form.getvalue('phenotype_notes', None),
            form.getvalue('genotype_notes', None),
            form.getvalue('dna_avail', None),
            form.getvalue('notes', None),
            form.getvalue('maintenance', None)
        ))
        connection.commit()
        print("Data inserted successfully")

except Exception as e:
    print("Failed to insert data:", e)

# Close database connection
connection.close()
