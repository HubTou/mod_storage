#!/usr/bin/env python3
""" mod_storage - Luanti mod_storage management
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier

# Database schema:
$ sqlite3 mod_storage.sqlite
sqlite> .schema
CREATE TABLE `entries` (
        `modname` TEXT NOT NULL,
        `key` BLOB NOT NULL,
        `value` BLOB NOT NULL,
        PRIMARY KEY (`modname`, `key`)
);
"""

import getopt
import sqlite3
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: mod_storage - Luanti mod_storage management v1.0.0 (December 23, 2024) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "database": "mod_storage.sqlite",
    "modname": "",
    "key": "",
    "value": ""
}

####################################################################################################
def _display_help():
    """ Display usage and help """
    #pylint: disable=C0301
    print("usage: mod_storage [--help|-?] [--version]", file=sys.stderr)
    print("       [-d|--db|--database FILE]", file=sys.stderr)
    print("       [-m|--mod|--modname MODNAME]", file=sys.stderr)
    print("       [-k|--key KEY]", file=sys.stderr)
    print("       [-v|--val|--value VALUE]", file=sys.stderr)
    print("       [--] [insert|delete|view]", file=sys.stderr)
    print("  -------------------  --------------------------------------------------", file=sys.stderr)
    print("  List table content        : mod_storage", file=sys.stderr)
    print('  Insert an entry           : mod_storage -m "modname" -k "key" -v "value" insert', file=sys.stderr)
    print('  delete an entry           : mod_storage -m "modname" -k "key" delete', file=sys.stderr)
    print('  delete all MODNAME entries: mod_storage -m "modname" delete', file=sys.stderr)
    print('  delete all KEY entries    : mod_storage -k "key" delete', file=sys.stderr)
    print(file=sys.stderr)
    #pylint: enable=C0301

####################################################################################################
def _process_command_line():
    """ Process command line options """
    #pylint: disable=C0103, W0602
    global parameters
    #pylint: enable=C0103, W0602

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "d:hk:m:v:?"
    string_options = [
        "help",
        "version",
        "db=",
        "database=",
        "key=",
        "mod=",
        "modname=",
        "val=",
        "value=",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        print(f"Syntax error: {error}", file=sys.stderr)
        _display_help()
        sys.exit(1)

    for option, argument in options:
        if option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option in ("-d", "--db", "--database"):
            parameters["database"] = argument

        elif option in ("-k", "--key"):
            parameters["key"] = argument.encode("utf-8")

        elif option in ("-m", "--mod", "--modname"):
            parameters["modname"] = argument

        elif option in ("-v", "--val", "--value"):
            parameters["value"] = argument.encode("utf-8")

    return remaining_arguments

####################################################################################################
def main():
    """ The program's main entry point """
    arguments = _process_command_line()

    if len(arguments) > 1:
        print("Syntax error: too many arguments", file=sys.stderr)
        _display_help()
        sys.exit(1)
        
    connection = sqlite3.connect(parameters["database"])
    cursor = connection.cursor()

    if not arguments or arguments[0] == "view":
        print("TABLE 'entries':")
        print("================")
        for row in cursor.execute("SELECT modname, key, value FROM entries"):
            print(row)

    elif arguments[0] == "insert":
        if parameters["modname"] and parameters["key"] and parameters["value"]:
            cursor.execute(f"""INSERT INTO entries VALUES (?, ?, ?)""", (parameters["modname"], parameters["key"], parameters["value"]))                        
            connection.commit()
        else:
            print("Syntax error: missing arguments", file=sys.stderr)
            _display_help()
            connection.close()
            sys.exit(1)

    elif arguments[0] == "delete":
        if parameters["modname"] and parameters["key"]:
            cursor.execute(f"""DELETE FROM entries WHERE modname=? AND key=?""", (parameters["modname"], parameters["key"]))            
            connection.commit()
        elif parameters["modname"]:
            cursor.execute(f"""DELETE FROM entries WHERE modname=?""", (parameters["modname"],))
            connection.commit()
        elif parameters["key"]:
            cursor.execute(f"""DELETE FROM entries WHERE key=?""", (parameters["key"],))
            connection.commit()
        else:
            print("Syntax error: missing arguments", file=sys.stderr)
            _display_help()
            connection.close()
            sys.exit(1)

    connection.close()
    sys.exit(0)

main()