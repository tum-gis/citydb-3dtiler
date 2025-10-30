import psycopg2
import os
import yaml

advisement = {
    'Advises' : {
        'Given Command Arguments' : None,
        'Maximum Feature Number per Tile' : None
        }
}

def write_yaml(folder, file_name, content):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path, "w") as advise_file:
            yaml.dump(content, advise_file, width=150, indent=4)
        print(f'(i)--> File has been created as {relative_file_path}.')
    except OSError as err:
        print(f'(e)--> File writing error :\n {err}')

def read_sql_query(folder, file_name):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path,"r") as advise_query:
            query = advise_query.read()
        return query
    except Error as err:
        print('File reading error:\n {err}')

def advise(args):
    # print(dir(args))
    print(f"(i)--> Connection: {args.db_host}, {args.db_name}, {args.db_port}, {args.db_schema}, {args.db_username}, ***")
    try: 
        conn = psycopg2.connect(
            host=args.db_host, 
            dbname=args.db_name, 
            port=args.db_port, 
            user=args.db_username, 
            password=args.db_password)
        conn.autocommit = True
        #print(f"Autocommit: {conn.autocommit} and Isolation Level: {conn.isolation_level}")
    except psycopg2.Error as err:
        print(f'Error:\n{err}')

    query = read_sql_query('advise_sql', 'calculate_recommended_max_features_per_tile.sql')
    #print(query)

    try:
        cur = conn.cursor()
        print(f"(i)--> Connection Status: {cur.connection.status}")
        cur.execute(query)
        result = cur.fetchone()
        conn.commit()
        conn.close()
        advisement['Advises']['Given Command Arguments'] = str(args._get_kwargs())
        advisement['Advises']['Maximum Feature Number per Tile'] = round(result[3])
        write_yaml('output', args.output, advisement)
    except psycopg2.DatabaseError as err:
        print(f'Database error:\n{err}')