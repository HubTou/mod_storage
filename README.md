# mod_storage manager
A [Luanti](https://www.luanti.org/) tool for managing the mod_storage SQLite3 database file content.

With it you can view the database entries, insert entries, delete an entry or delete all entries by modname or key.

## Installation
1. Install [Python](https://www.python.org/downloads/),
2. Copy the *mod_storage.py* script somewhere in your computer:
   1. Preferably somewhere in the PATH,
   2. Or in your *luanti/client* directory, where the *mod_storage.sqlite* file is located.

Note: If you haven't upgraded yet to luanti 5.10.0 or newer, your *luanti* directory will be called *minetest*...

## Usage
This is a command-line tool.

If you use Windows, run it through your [Terminal](https://github.com/microsoft/terminal) or your [PowerShell](https://github.com/PowerShell/PowerShell) application.
If your terminal opens a new window and doesn't give you a chance to see what is printed inside, just type the following command before trying anew:
```bat
$env:PATHEXT += ';.PY'
```

To obtain usage help, type one of the following commands:
```bash
mod_storage --help
mod_storage -?
```

If you don't run the script in the place where your *mod_storage.sqlite* file is located,
you'll need to indicate its path with the *-d*, *--db* or *--database* option.

To view the database content, type one of the following commands:
```bash
mod_storage
mod_storage view
```

To insert an entry, use the following command:
```bash
mod_storage --modname "My mod name" --key "The key" --value "The corresponding value" insert
```
 
You can replace:
* --modname by the shorter --mod or -m
* --key by the shorter -k
* --value by the shorter --val or -v

If the parameter is only one word, you don't have to quote it.

To delete entries, type one of the following commands:
```bash
mod_storage --modname "My mod name" --key "The key" delete
mod_storage --modname "My mod name" delete
mod_storage --key "The key" delete
```

The first form will delete the specified entry, the second one all entries for MODNAME and the last one all entries for KEY.

If you are unsure of what you're doing, just make a copy of your *mod_storage.sqlite" file before starting to edit it...

## Caveats
Processing of other backend storage methods is not supported.

## Possible future directions
This command was made to clean up my mod_storage file after playing too much with work-in-progress mods.

**And I especially wanted to test the possibility to communicate with a client-side mod through this file...
=> It works! Two way communication between Luanti and an external program is possible through mod_storage.sqlite**

Given this result, it would now be interesting to offer a batch mechanism to import/export file contents into/from mod_storage.

Other than that, I still need to check how [ints, floats and tables](https://github.com/minetest/minetest/blob/master/doc/lua_api.md#methods-6) are stored, and adapt the tool to handle them.

Go to [Discussions](https://github.com/HubTou/chat_exporter/discussions) if you want to suggest other things...
