#External libraries
import psycopg2

def pg_show_details(args):
    print(f"(i)--> Connection: {args.db_host}, {args.db_name}, {args.db_port}, {args.db_schema}, {args.db_username}, {args.db_password}\n")

def pg_establish(args):
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
        print(f"Error:\n{err}")
    finally:
        return conn

def pg_create_session(conn):
    cur = conn.cursor()
    return cur

def pg_check_connection(conn):
    print(f"Autocommit: {conn.autocommit} and Isolation Level: {conn.isolation_level}")
    print(dir(conn))

def pg_check_session(cur):
    print(f"(i)--> Connection Status: {cur.connection.status}")
    return cur.connection.status

