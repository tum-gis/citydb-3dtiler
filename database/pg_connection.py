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
    # print(f"(i)--> Connection Status: {cur.connection.status}")
    return cur.connection.status

def create_materialized_view(mv_name, query):
    mv=f"DROP MATERIALIZED VIEW IF EXISTS citydb.{mv_name}; \
    CREATE MATERIALIZED VIEW IF NOT EXISTS citydb.{mv_name} \
    TABLESPACE pg_default AS \
    {query} \
    WITH DATA;"
    return mv

def index_materialized_view(table_name, geom_column):
    iq = f"CREATE INDEX IF NOT EXISTS {table_name}_{geom_column}_idx \
    ON {table_name} \
    USING gist(st_centroid(st_envelope({geom_column})))"
    return iq

def get_query_results(args, query, name="not-specified"):
    conn = pg_establish(args)
    try:
        cur = pg_create_session(conn)
        if pg_check_session(cur):
            cur.execute(query)
        else:
            print("Something went wrong with the database.")
        result = cur.fetchone()
        conn.commit()
        conn.close()
        
    except OSError as err:
        print(f"Database error:\n{err}")
    finally:
        print(f"(i) {name} executed,  and the results were obtained.")
    return result

def run_sql(args, query, name="not-specified"):
    conn = pg_establish(args)
    try:
        cur = pg_create_session(conn)
        if pg_check_session(cur):
            cur.execute(query)
        else:
            print("Something went wrong with the database.")
        conn.commit()
        conn.close()
        
    except OSError as err:
        print(f"Database error:\n{err}")
    finally:
        print(f"(i) {name} executed.")

