#!/usr/bin/env python3

import cgi
import json
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

# Parse form data
form = cgi.FieldStorage()

queries = {
    'line': '''
    UPDATE m_lines
    SET short_name = %s, full_genotype = %s, background = %s, published = %s,
        authors = %s, creators = %s, phenotype = %s, phenotype_notes = %s, genotype_notes = %s,
        dna_avail = %s, notes = %s, maintenance = %s
    WHERE l_id = %s;    
    ''',

    'member': '''
    UPDATE lab_members
    SET f_name = %s, l_name = %s, lab_role = %s, active = %s
    WHERE m_id = %s;
    ''',

    'sort': '''
    UPDATE sort
    SET hatch_date = %s, sort_date = %s, line_name = %s,
        marker_color = %s, marker_location = %s, fl_ratio = %s,
        fl_total = %s, notes = %s, l_id = %s, m_id = %s
    WHERE sort_id = %s;
    ''',

    'pass': '''
    UPDATE passage
    SET l_id = %s, m_id = %s, bc = %s, ib = %s, hatch_date = %s,
        passage_date = %s, next_passage = %s, mating_line = %s
    WHERE pass_id = %s;
    ''',
    
    'clutch': '''
    UPDATE clutch
    SET l_id = %s, m_id = %s, hatch_date = %s, collection_date = %s,
        clutch_number = %s, egg_papers = %s
    WHERE clutch_id = %s;
    '''
}

def replace_empty_with_none(value):
    return value if value else None

if form:
    try:
        selector = form.getvalue('selector')
        
        # Connect to the database
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            if selector == 'line':
                cursor.execute(queries[selector],
                            (replace_empty_with_none(form.getvalue('short_name', None)),
                                replace_empty_with_none(form.getvalue('full_genotype', None)),
                                replace_empty_with_none(form.getvalue('background', None)),
                                replace_empty_with_none(form.getvalue('published', None)),
                                replace_empty_with_none(form.getvalue('authors', None)),
                                replace_empty_with_none(form.getvalue('creators', None)),
                                replace_empty_with_none(form.getvalue('phenotype', None)),
                                replace_empty_with_none(form.getvalue('phenotype_notes', None)),
                                replace_empty_with_none(form.getvalue('genotype_notes', None)),
                                replace_empty_with_none(form.getvalue('dna_avail', None)),
                                replace_empty_with_none(form.getvalue('line_notes', None)),
                                replace_empty_with_none(form.getvalue('maintenance', None)),
                                
                                form.getvalue('l_id'),))
                connection.commit()


            if selector == 'member':
                cursor.execute(queries[selector],
                            (replace_empty_with_none(form.getvalue('f_name', None)),
                                replace_empty_with_none(form.getvalue('l_name', None)),
                                replace_empty_with_none(form.getvalue('lab_role', None)),
                                replace_empty_with_none(form.getvalue('active', None)),

                                form.getvalue('m_id'),))
                connection.commit()

            if selector == 'sort':
                cursor.execute(queries[selector],
                            (replace_empty_with_none(form.getvalue('hatch_date', None)),
                                replace_empty_with_none(form.getvalue('sort_date', None)),
                                replace_empty_with_none(form.getvalue('line_name', None)),
                                replace_empty_with_none(form.getvalue('marker_color', None)),
                                replace_empty_with_none(form.getvalue('marker_location', None)),
                                replace_empty_with_none(form.getvalue('fl_ratio', None)),
                                replace_empty_with_none(form.getvalue('fl_total', None)),
                                replace_empty_with_none(form.getvalue('sort_notes', None)),
                                replace_empty_with_none(form.getvalue('l_id', None)),
                                replace_empty_with_none(form.getvalue('m_id', None)),

                                form.getvalue('sort_id'),))
                connection.commit()
            
            if selector == 'pass':
                cursor.execute(queries[selector],
                            (replace_empty_with_none(form.getvalue('l_id', None)),
                                replace_empty_with_none(form.getvalue('m_id', None)),
                                replace_empty_with_none(form.getvalue('bc', None)),
                                replace_empty_with_none(form.getvalue('ib', None)),
                                replace_empty_with_none(form.getvalue('hatch_date', None)),
                                replace_empty_with_none(form.getvalue('passage_date', None)),
                                replace_empty_with_none(form.getvalue('next_passage', None)),
                                replace_empty_with_none(form.getvalue('mating_line', None)),

                                form.getvalue('pass_id'),))
                connection.commit()

            if selector == 'clutch':
                cursor.execute(queries[selector],
                            (replace_empty_with_none(form.getvalue('l_id', None)),
                                replace_empty_with_none(form.getvalue('m_id', None)),
                                replace_empty_with_none(form.getvalue('hatch_date', None)),
                                replace_empty_with_none(form.getvalue('collection_date', None)),
                                replace_empty_with_none(form.getvalue('clutch_number', None)),
                                replace_empty_with_none(form.getvalue('egg_papers', None)),

                                form.getvalue('clutch_id'),))
                connection.commit()
                
            response = {}
            # Update the response
            response["success"] = True
            response["message"] = "Data updated successfully"
    except Exception as e:
            response["success"] = False
            response["error"] = "Failed to update data: {}".format(str(e))

    finally:
        # Close the database connection
        if 'connection' in locals() and connection.open:
            connection.close()


    # Output JSON response
    print("Content-type: application/json\n")
    print(json.dumps(response))   
