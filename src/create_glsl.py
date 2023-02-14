# * Description:  Script for creating GLSL shader files
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
    print_help( "glnew: create new GLSL shader source files" )
    print_help( " -n, --name, string [string] [required] [position = 1]: set name of shader files. include parent directories if necessary" )
    print_help( " --vertex           [switch]: only create vertex file. error if --fragment is also defined" )
    print_help( " --fragment         [switch]: only create fragment file. error if --vertex is also defined" )
    print_help( " --no_info          [switch]: don't write info" )
    print_help( " -v, --version      [string]: change GLSL version. default = 460 core" )
    print_help( " -d, --description  [string]: description at the top of files. error if --no_info is also defined" )
    print_help( " -o, --overwrite    [switch]: will overwrite files if they already exist" )
    print_help( " -s, -q, --silent, --quiet [switch]: don't print status" )
    print_help( "\n -h, --help      [switch]: print this help message and quit" )
    sys.exit(0)

short_options = "n:d:v:ohsq"
long_options  = [
    "name=", "overwrite",
    "help", "vertex", "fragment",
    "no_info", "description", "version",
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

    no_vertex    = False
    no_fragment  = False
    no_info      = False
    overwrite    = False
    description  = ""
    version      = "460 core"

    try:
        args, values = getopt.getopt( arg_list, short_options, long_options )
    except getopt.error as err:
        print_fatal( err )

    for arg, value in args:
        if arg == "-h" or arg == "--help":
            display_help()
        if arg == "-n" or arg == "--name":
            name = value
        if arg == "--vertex":
            no_fragment = True
        if arg == "--fragment":
            no_vertex = True
        if arg == "--no_info":
            no_info = True
        if arg == "-v" or arg == "--version":
            version = value
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

    if no_vertex and no_fragment:
        print_fatal( "--vertex and --fragment cannot be defined simultaneously!" )

    vertex_ext   = ".vs"
    fragment_ext = ".fs"

    vertex_full_path   = name + vertex_ext
    fragment_full_path = name + fragment_ext

    desc = ""
    if not(no_info):
        today = date.today()
        desc += "/**\n"
        desc += " * Description:  " + description + "\n"
        desc += " * Author:       Alicia Amarilla (smushyaa@gmail.com)\n"
        desc += " * File Created: " + today.strftime( "%B %d, %Y" ) + "\n"
        desc += "*/\n"


    if not(no_vertex):
        if not(overwrite) and pathlib.Path( vertex_full_path ).is_file():
            print_err( "error: cannot create vertex file, file already exists" )
            print_err( "use -o or --overwrite to overwrite existing file" )
        else:
            try:
                with open( vertex_full_path, "w+", newline='\n' ) as write_file:
                    if not(no_info):
                        write_file.write( desc )
                    write_file.write( "#version " + version + "\n\n" )
                    write_file.write( "out struct{\n    \n} v2f;\n\n" )
                    write_file.write( "void main() {\n    \n}\n" )
            except OSError as err:
                print_fatal( str(err) )

            print_status( "created vertex file \"" + vertex_full_path + "\"" )

    if not(no_fragment):
        if not(overwrite) and pathlib.Path( fragment_full_path ).is_file():
            print_err( "error: cannot create fragment file, already exists" )
            print_err( "use -o or --overwrite to overwrite existing file" )
        else:
            try:
                with open( fragment_full_path, "w+", newline='\n' ) as write_file:
                    if not(no_info):
                        write_file.write( desc )
                    write_file.write( "#version " + version + "\n\n" )
                    write_file.write( "in struct{\n    \n} v2f;\n\n" )
                    write_file.write( "out vec4 FRAG_COLOR;\n" )
                    write_file.write( "void main() {\n    \n}\n" )
            except OSError as err:
                print_fatal( str(err) )

            print_status( "created fragment file \"" + fragment_full_path + "\"" )

    sys.exit(0)