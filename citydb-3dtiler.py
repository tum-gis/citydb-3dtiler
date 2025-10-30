#!/usr/bin/env python3

# External Libraries
import argparse

# Internal Libraries
from advise_main import advise
from tile_main import tile

# Added as a future task : Customizing the main help document.
def help():
    print('Welcome to the help doc.')

def main():
    # Add the main parser
    parser = argparse.ArgumentParser(
    prog='citydb-3dtiler', \
    description='citydb-3dtiler: Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance with the provided custom arguments.')

    # Subparsers used to gather together the command related arguments
    subparsers = parser.add_subparsers(help='Select one of the operations: advise, tile.', dest='command')

    # Advise command uses it's own arguments
    parser_advise = subparsers.add_parser('advise', help='generates advisement docs for the existing dataset.')
    parser_advise.add_argument('--consider-appearances', action=argparse.BooleanOptionalAction, default=False)
    parser_advise.add_argument('-o', '--output', metavar='Output File Name', nargs='?', default='advise.yml')
    
    # Tile command uses it's own arguments
    parser_tile = subparsers.add_parser('tile', help='generates 3DTiles from the existing dataset.')

    # Database authorization information gathered as a group,
    # so the group arguments can be used both of the commands.
    db_group = parser.add_argument_group('database-connection')
    db_group.add_argument('-H', '--db-host', metavar='Hostname', help='Type the name or the IP address of the database host machine.')
    db_group.add_argument('-P', '--db-port', metavar='Port Number', help='Type the port number of the database.', type=int, default=5432)
    db_group.add_argument('-d', '--db-name', metavar='Database Name', help='Type the database name.')
    db_group.add_argument('-S', '--db-schema', metavar='Schema', help='Type the schema name on the database.', default='citydb')
    db_group.add_argument('-u', '--db-username', metavar='Username', help='Type the username for the database.')
    db_group.add_argument('-p', '--db-password', metavar='Password', help='Type the password for the database.')

    # Time to parse the arguments
    args = parser.parse_args()

    # User arguments forwarded to the relevant functions.
    if args.command == 'advise':
        advise(args)
    elif args.command == 'tile':
        tile(args)
    else:
        print('Please select one of the available commands : advise, tile. Otherwiser add -h or --help to get help.')

if __name__ == "__main__":
    main()