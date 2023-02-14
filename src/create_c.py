# * Description:  Script for creating C header/source files
# * Author:       Alicia Amarilla ( smushyaa@gmail.com )
# * File Created: February 09, 2023

import sys
import os
import getopt
import pathlib
from datetime import date
import termcolor

silent = False

def print_status( msg:str ):
    if not(silent):
        print( termcolor.colored( msg, "green" ) )

def print_err( msg:str ):
    print( termcolor.colored( msg, "red" ) )

def print_fatal( msg:str ):
    print_err( "error: " + msg )
    print_err( "run with -h or --help to get a list of valid options" )
    sys.exit(-1)

def print_help( msg:str ):
    print( termcolor.colored( msg, "cyan" ) )

def display_help():
    print_help( "cnew: create new C/C++ header and/or source file" )
    print_help( " -n, --name, string [string] [required] [position = 1]: set name of source/header. don't include src directory as it is implicit" )
    print_help( "    if there is no src directory in the current directory, file will instead be created in the current directory." )
    print_help( " --no_pragma        [switch]: don't write pragma once in header file" )
    print_help( " --no_include       [switch]: don't header file in source file. error if --source or --header is also defined" )
    print_help( " --header           [switch]: only create header file. error if --source is also defined" )
    print_help( " --source           [switch]: only create source file. error if --header is also defined" )
    print_help( " --no_info          [switch]: don't write info" )
    print_help( " -d, --description  [string]: description at the top of files. error if --no_info is also defined" )
    print_help( " -c                 [switch]: create c source/header instead of cpp" )
    print_help( " -o, --overwrite    [switch]: will overwrite files if they already exist" )
    print_help( " -g, --header_guard [string]: define header guard to use instead of pragma once. --no_pragma has no effect with this option" )
    print_help( " -s, -q, --silent, --quiet [switch]: don't print status" )
    print_help( "\n -h, --help      [switch]: print this help message and quit" )
    sys.exit(0)

short_options = "n:g:d:ochsq"
long_options  = [
    "name=", "overwrite", "header_guard=",
    "no_pragma", "help", "header",
    "source", "no_info", "no_include",
    "description",
    "silent", "quiet"
]

if __name__ == "__main__":
    arg_list = sys.argv[1:]

    if len( arg_list ) == 0:
        print_fatal( "arguments required!" )

    name = ""

    if not("-" in arg_list[0]):
        name = arg_list[0]
        arg_list = arg_list[1:]

    cpp          = True
    no_header    = False
    no_source    = False
    header_guard = ""
    no_pragma    = False
    no_info      = False
    no_include   = False
    overwrite    = False
    description  = ""

    try:
        args, values = getopt.getopt( arg_list, short_options, long_options )
    except getopt.error as err:
        print_fatal( err )

    for arg, value in args:
        if arg == "-h" or arg == "--help":
            display_help()
        if arg == "-n" or arg == "--name":
            name = value
        if arg == "--source":
            no_header = True
        if arg == "--header":
            no_source = True
        if arg == "--no_pragma":
            no_pragma = True
        if arg == "--no_include":
            no_include = True
        if arg == "-c":
            cpp = False
        if arg == "-g" or arg == "--header_guard":
            header_guard = value
        if arg == "--no_info":
            no_info = True
        if arg == "-o" or arg == "--overwrite":
            overwrite = True
        if arg == "-s" or arg == "-q" or arg == "--silent" or arg == "--quiet":
            silent = True
        if arg == "-d" or arg == "--description":
            description = value

    if name == "":
        print_fatal( "must input file name!" )

    if no_info and description != "":
        print_fatal( "--no_info and -d/--description cannot be defined simultaneously!" )

    if no_header and no_source:
        print_fatal( "--header and --source cannot be defined simultaneously!" )

    if no_include and ( no_header or no_source ):
        print_fatal( "--no_include and --source/--header cannot be defined simultaneously!" )

    header_ext = ""
    source_ext = ""

    if cpp:
        header_ext = ".hpp"
        source_ext = ".cpp"
    else:
        header_ext = ".h"
        source_ext = ".c"

    base_name = os.path.basename(os.path.normpath( name ))

    header_full_path = ""
    source_full_path = ""

    if pathlib.Path( "src" ).is_dir():
        header_full_path = "src/" + name + header_ext
        source_full_path = "src/" + name + source_ext
    else:
        header_full_path = name + header_ext
        source_full_path = name + source_ext

    desc = ""
    if not(no_info):
        today = date.today()
        desc += "/**\n"
        desc += " * Description:  " + description + "\n"
        desc += " * Author:       Alicia Amarilla (smushyaa@gmail.com)\n"
        desc += " * File Created: " + today.strftime( "%B %d, %Y" ) + "\n"
        desc += "*/\n"


    if not(no_header):
        if not(overwrite) and pathlib.Path( header_full_path ).is_file():
            print_err( "error: cannot create header file, file already exists" )
            print_err( "use -o or --overwrite to overwrite existing file" )
        else:
            try:
                with open( header_full_path, "w+", newline='\n' ) as write_file:
                    if not(no_info):
                        write_file.write( desc )
                    if header_guard == "":
                        if not( no_pragma ):
                            write_file.write( "#pragma once" )
                    else:
                        write_file.write( "#if !defined(" + header_guard + ")\n" )
                        write_file.write( "#define " + header_guard + " 1\n" )
                        write_file.write( "#endif\n" )
            except OSError as err:
                print_fatal( str(err) )

            print_status( "created header file \"" + header_full_path + "\"" )

    if not(no_source):
        if not(overwrite) and pathlib.Path( source_full_path ).is_file():
            print_err( "error: cannot create source file, already exists" )
            print_err( "use -o or --overwrite to overwrite existing file" )
        else:
            try:
                with open( source_full_path, "w+", newline='\n' ) as write_file:
                    if not(no_info):
                        write_file.write( desc )
                    if not(no_include) and not(no_header):
                        write_file.write( "#include \"" + base_name + header_ext + "\"" )
            except OSError as err:
                print_fatal( str(err) )

            print_status( "created source file \"" + source_full_path + "\"" )

    sys.exit(0)
