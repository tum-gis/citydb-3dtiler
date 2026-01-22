#!/usr/bin/env python3

# External Libraries
import argparse
import os

# Internal Libraries
from advise_main import advise
from tile_main import tile
from io_tools.folder import check_file_in, create_folder
from default_paths import get_base_path, get_shared_folder_path
# from custom_checks import check_arguments

# Added as a future task : Customizing the main help document.
def help():
    print("Welcome to the help doc.")

def main():
    # Add the main parser
    parser = argparse.ArgumentParser(
    prog="citydb-3dtiler", \
    description="citydb-3dtiler: Generates 3D Tiles by connecting to a 3DCityDB (v5) database instance with the provided custom arguments.")
    parser.add_argument("--tilers-path", help="Set the absolute/relative path of the selected 3D Tile Generator software.", metavar="File Path of the 3D Tiler", nargs="?", default="tiler_app/")
    parser.add_argument("--tiler-app", help="Choose one of the compatible 3D Tile Generator app.", default="pg2b3dm", choices=["pg2b3dm", "py3dtiles"])
    parser.add_argument("--separate-tilesets", help="exports separate tilesets for each objectclass or namespace", nargs="?", default=None, choices=["objectclass", "namespace"])

    # Subparsers used to gather together the command related arguments
    subparsers = parser.add_subparsers(help="Select one of the operations: advise, tile.", dest="command")

    # Advise command uses it"s own arguments
    parser_advise = subparsers.add_parser("advise", help="generates advisement docs for the existing dataset.")
    parser_advise.add_argument("--consider-thematic-features", action=argparse.BooleanOptionalAction, default=False)
    #parser_advise.add_argument("--consider-appearances", action=argparse.BooleanOptionalAction, default=False)
    parser_advise.add_argument("-o", "--output-file", metavar="Output File Name", nargs="?", default="advise.yml")
    

    # Tile command uses it"s own arguments
    parser_tile = subparsers.add_parser("tile", help="generates 3DTiles from the existing dataset.")
    parser_tile.add_argument("--style-mode", help="Select one of the available style-mode options.", choices=["existing-appearances", "property-based", "objectclass-based", "no-style"], default="objectclass-based")
    parser_tile.add_argument("--style-absence-behavior", help="If you want to change the appearance selection behavior of the tiling app, select one of the possible options. Default option is 'fall-down', which means that if you select a 'property-based' styling mode and there are no available predefined properties (in materials_for_features.csv file) that match your object, the tiling tool will automatically select the next styling mode ('objectclass-based' style mode) for the  instance.", choices=["fall-down", "rise-up"], default="fall-down")
    parser_tile.add_argument("-o", "--output-folder", help="Set the folder for the 3DTiles. Default value is the 'shared' folder.", metavar="Output Folder", nargs="?", default="shared")
    parser_tile.add_argument("--transparency", help="Choose of the possible options. Please consider that transparency values might vary regarding to the selected tiler application.", choices=["blend", "mask", "opaque"], default="blend")
    parser_tile.add_argument("--custom-style", help="If you want to provide a custom style file (any CSV file not named 'materials_for_features'), you can specify the file name (inc. file extension : CSV) using this argument.", metavar="Name of the custom style file", nargs="?", default="materials_for_features.csv")
    
    # Database authorization information gathered as a group,
    # so the group arguments can be used both of the commands.
    db_group = parser.add_argument_group("database-connection")
    db_group.add_argument("-H", "--db-host", metavar="Hostname", help="Type the name or the IP address of the database host machine.")
    db_group.add_argument("-P", "--db-port", metavar="Port Number", help="Type the port number of the database.", type=int, default=5432)
    db_group.add_argument("-d", "--db-name", metavar="Database Name", help="Type the database name.")
    db_group.add_argument("-S", "--db-schema", metavar="Schema", help="Type the schema name on the database.", default="citydb")
    db_group.add_argument("-u", "--db-username", metavar="Username", help="Type the username for the database.")
    db_group.add_argument("-p", "--db-password", metavar="Password", help="Type the password for the database.")

    # Time to parse the arguments
    args = parser.parse_args()

    # User arguments forwarded to the relevant functions.
    if args.command == "advise":
        advise(args)
    elif args.command == "tile":
        # Check if the advise command executed once or not.
        #  If not, try to run it first.
        if args.output_folder == "shared":
            advice_file = check_file_in("advise.yml", get_shared_folder_path())
        else:
            create_folder(get_shared_folder_path(), args.output_folder)
            #custom_folders_path = os.path.join(get_shared_folder_path(), args.output_folder)
            advice_file = check_file_in("advise.yml", get_shared_folder_path())
        if advice_file["exists"] == True:
            tile(args)
        else:
            args.output_file = 'advise.yml'
            advise(args)
            tile(args)
    else:
        print("Please select one of the available commands : advise, tile. Otherwiser add -h or --help to get help.")

if __name__ == "__main__":
    main()