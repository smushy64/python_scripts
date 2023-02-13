# * Description:  Script for creating new C/C++ project structure
# * Author:       Alicia Amarilla ( smushyaa@gmail.com )
# * File Created: February 09, 2023

import sys
import os
import glob
import pathlib
import termcolor
import getopt
from datetime import date

today = date.today()

comment_author = "Alicia Amarilla ( smushyaa@gmail.com )"
comment_date   = today.strftime( "%B %d, %Y" )
comment_info0  = "    * Description:  \n"
comment_info1  = "    * Author:       " + comment_author + "\n"
comment_info2  = "    * File Created: " + comment_date + "\n"

comment_info = "/**\n" + comment_info0 + comment_info1 + comment_info2 + "*/\n"

def print_cyan( msg:str ):
    print( termcolor.colored( msg, "cyan" ) )

def print_status( msg:str ):
    print( termcolor.colored( msg, "green" ) )

def print_err( msg:str ):
    print( termcolor.colored( msg, "red" ) )

def print_fatal( msg:str ):
    print_err( msg )
    print_err( "run with -h or --help to get a list of valid options" )
    sys.exit(-1)

def create_default_compile_flags( is_cpp, version, is_silent ):
    cflags_path = "compile_flags.txt"
    if pathlib.Path( cflags_path ).is_file():
        if not(is_silent):
            print_err( "file \"" + cflags_path + "\" already exists" )
    else:
        file = open( cflags_path, "w+", newline='\n' )
        if is_cpp:
            file.write( "g++\n" )
        else:
            file.write( "gcc\n" )

        file.write( "-std=" + version + "\n" )
        file.write( "-I./src\n" )
        file.write( "-D_CLANGD=1\n" )

        for cflag in cflags:
            file.write(str(cflag) + "\n")

        file.close()
        if not( is_silent ):
            print_status( "created file \"" + cflags_path + "\"" )

def rename_proj( new_name, is_silent ):
    success = True

    launch_path = "./.vscode/launch.json"
    if pathlib.Path( launch_path ).is_file():
        launch_lines = []
        with open( launch_path, "r" ) as read_file:
            launch_lines = read_file.readlines()

        program_line_found = False

        for idx, line in enumerate( launch_lines ):
            if "\"program\":" in line:
                program_line_found = True
                launch_lines[idx] = "            \"program\": \"${workspaceFolder}/build/debug/" + new_name + ".exe\",\n"

        if program_line_found:
            with open( launch_path, "w+", newline='\n' ) as write_file:
                for line in launch_lines:
                    write_file.write( line )
            if not( is_silent ):
                print_status( "launch.json updated with new project name" )
        else:
            success = False
            if not( is_silent ):
                print_err( "failed to edit launch.json, formatting unrecognized" )
    else:
        if not( is_silent ):
            print_err( "failed to edit launch.json in vscode directory, could not find it" )

    makefile_path = "./Makefile"
    if pathlib.Path( makefile_path ).is_file():
        makefile_lines = []
        with open( makefile_path, "r" ) as read_file:
            makefile_lines = read_file.readlines()
        
        exe_line_found = False
        for idx, line in enumerate( makefile_lines ):
            if "EXE =" in line:
                exe_line_found = True
                makefile_lines[idx] = "EXE = " + new_name + ".exe\n"
                if not( is_silent ):
                    print_status( "Makefile updated with new project name" )
        
        if exe_line_found:
            with open( makefile_path, "w+", newline='\n' ) as write_file:
                for line in makefile_lines:
                    write_file.write( line )
        else:
            success = False
            if not( is_silent ):
                print_err( "failed to edit Makefile, formatting unrecognized" )
    else:
        if not( is_silent ):
            print_err( "failed to edit Makefile, could not find it" )
    
    if not( is_silent ):
        if success:
            print_status( "successfully renamed project to \"" + new_name + "\"" )
        else:
            print_err( "failed to fully rename project" )

def create_src_dir( directories, is_silent ):
    for dir in directories:
        if os.path.exists( dir ):
            if not( is_silent ):
                print_err( "dir \"" + dir + "\" already exists" )
        else:
            os.makedirs( dir )
            if not( is_silent ):
                print_status( "created dir \"" + dir + "\"" )

    makefile_path = "./Makefile"
    if pathlib.Path( makefile_path ).is_file():
        makefile_lines = []
        with open( makefile_path, "r" ) as read_file:
            makefile_lines = read_file.readlines()

        for idx, line in enumerate(makefile_lines):
            if "SRC = " in line:
                edit_line = makefile_lines[idx]
                edit_line = edit_line.replace( "\n", "" )
                for dir in directories:
                    append_dir = " ./" + dir
                    if not(append_dir in line):
                        edit_line += " ./" + dir
                makefile_lines[idx] = edit_line + "\n"

        with open( makefile_path, "w+", newline='\n' ) as write_file:
            for line in makefile_lines:
                write_file.write( line )

        print_status( "added source directories to Makefile" )
    else:
        if not( is_silent ):
            print_err( "failed to edit Makefile, no file present" )

def cflag_exists( lines, flag_to_find ) -> bool:
    for line in lines:
        if flag_to_find in line:
            return True
    return False

def add_cflags( cflags, is_silent ):
    cflags_path = "compile_flags.txt"
    if pathlib.Path( cflags_path ).is_file():
        cflag_lines = []
        with open( cflags_path, "r" ) as read_file:
            cflag_lines = read_file.readlines()
        
        with open( cflags_path, "a", newline='\n' ) as write_file:
            for flag in cflags:
                if not(cflag_exists( cflag_lines, flag )):
                    write_file.write( flag + "\n" )
                    if not( is_silent ):
                        print_status( "added \"" + flag + "\" to compile_flags.txt" )
                else:
                    if not( is_silent ):
                        print_err( "flag \"" + flag + "\" already exists in compile_flags.txt!" )
    else:
        if not( is_silent ):
            print_err( "failed to add compile flags, no compile_flags.txt present!" )

def add_makeflags( makeflags, is_silent ):
    makefile_path = "./Makefile"
    if pathlib.Path( makefile_path ).is_file():
        makefile_lines = []
        with open( makefile_path, "r" ) as read_file:
            makefile_lines = read_file.readlines()

        define_line_found = False

        for idx, line in enumerate(makefile_lines):
            if "DEF =" in line:
                define_line_found = True
                edit_line = makefile_lines[idx]
                edit_line = edit_line.replace( "\n", "" )
                for flag in makeflags:
                    if not( flag in edit_line ):
                        edit_line += " " + flag
                        if not( is_silent ):
                            print_status( "added \"" + flag + "\" to Makefile" )
                    else:
                        if not( is_silent ):
                            print_err( "flag \"" + flag + "\" already exists in Makefile!" )
                makefile_lines[idx] = edit_line + "\n"

        if not( define_line_found ):
            if not( is_silent ):
                print_err( "Makefile does not have a line named \"DEF =\"! could not add makeflags!" )

        with open( makefile_path, "w+", newline='\n' ) as write_file:
            for line in makefile_lines:
                write_file.write( line )
    else:
        if not( is_silent ):
            print_err( "failed to add makeflags, no Makefile present!" )

def init( project_name, is_cpp, version, cflags, makeflags, directories, create_readme, create_todo, is_silent, is_verbose ):
    status_message = ""

    main_dir = "."

    # create subdirectories

    for dir in directories:
        subdir = main_dir + "/" + dir
        if os.path.exists( subdir ):
            if is_verbose and not(is_silent):
                print_err( "dir \"" + subdir + "\" already exists" )
        else:
            os.makedirs( subdir )
            status_message += "created dir \"" + subdir + "\"\n"
    
    # create main.c/cpp

    main_path = "main"
    if is_cpp:
        main_path += ".cpp"
    else:
        main_path += ".c"

    main_path = main_dir + "/src/" + main_path

    if pathlib.Path(main_path).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + main_path + "\" already exists" )
    else:
        file = open( main_path, "w+", newline='\n' )
        file.write( comment_info )
        file.write( "\nint main( int argc, char* argv[] ) {\n    return 0;\n}\n" )
        file.close()
        status_message += "created file \"" + main_path + "\"\n"

    # create pch
    pch_path = "pch"
    if is_cpp:
        pch_path += ".hpp"
    else:
        pch_path += ".h"

    pch_path = main_dir + "/src/" + pch_path

    if pathlib.Path(pch_path).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + pch_path + "\" already exists" )
    else:
        file = open( pch_path, "w+", newline='\n' )
        file.write( comment_info )
        file.close()
        status_message += "created file \"" + pch_path + "\"\n"

    # create .gitignore

    gitignore_path = main_dir + "/.gitignore"

    if pathlib.Path( gitignore_path ).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + gitignore_path + "\" already exists" )
    else:
        file = open( gitignore_path, "w+", newline='\n' )
        file.write( "build\n.vscode\ncompile_flags.txt\n*.d\n*.o\n*.gch" )
        file.close()
        status_message += "created file \"" + gitignore_path + "\"\n"

    # create README and TODO

    if create_readme:
        readme_path = main_dir + "/README.md"
        if pathlib.Path( readme_path ).is_file():
            if is_verbose and not(is_silent):
                print_err( "file \"" + readme_path + "\" already exists" )
        else:
            file = open( readme_path, "w+", newline='\n' )
            file.write( "# " + project_name + "\n" )
            file.close()
            status_message += "created file \"" + readme_path + "\"\n"

    if create_todo:
        todo_path = main_dir + "/TODO.md"
        if pathlib.Path( todo_path ).is_file():
            if is_verbose and not(is_silent):
                print_err( "file \"" + todo_path + "\" already exists" )
        else:
            file = open( todo_path, "w+", newline='\n' )
            file.write( "# " + project_name + " todo list" + "\n\n - [ ] " )
            file.close()
            status_message += "created file \"" + todo_path + "\"\n"

    # create launch.json

    launch_path = main_dir + "/.vscode/launch.json"
    if pathlib.Path( launch_path ).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + launch_path + "\" already exists" )
    else:
        file = open( launch_path, "w+", newline='\n' )
        file.write( "{\n" )
        file.write( "    \"version\": \"0.2.0\",\n")
        file.write( "    \"configuarations\": [\n" )
        file.write( "        {\n" )
        file.write( "            \"name\": \"(gdb) Launch\",\n" )
        file.write( "            \"type\": \"cppdbg\",\n" )
        file.write( "            \"request\": \"launch\",\n" )
        file.write( "            \"program\": \"${workspaceFolder}/build/debug/" + project_name + ".exe\",\n" )
        file.write( "            \"args\": [],\n" )
        file.write( "            \"stopAtEntry\": false,\n" )
        file.write( "            \"cwd\": \"${workspaceFolder}\",\n" )
        file.write( "            \"environment\": [],\n" )
        file.write( "            \"externalConsole\": false,\n" )
        file.write( "            \"MIMode\": \"gdb\",\n" )
        file.write( "            \"miDebuggerPath\": \"C:/msys64/mingw64/bin/gdb.exe\",\n" )
        file.write( "            \"setupCommands\": [\n" )
        file.write( "                {\n" )
        file.write( "                    \"description\": \"Enable pretty-printing for gdb\",\n" )
        file.write( "                    \"text\": \"-enable-pretty-printing\",\n" )
        file.write( "                    \"ignoreFailures\": true\n" )
        file.write( "                }\n" )
        file.write( "            ]\n" )
        file.write( "        }\n" )
        file.write( "    ]\n" )
        file.write( "}" )
        file.close()
        status_message += "created file \"" + launch_path + "\"\n"

    # create compile_flags.txt

    cflags_path = main_dir + "/compile_flags.txt"
    if pathlib.Path( cflags_path ).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + cflags_path + "\" already exists" )
    else:
        file = open( cflags_path, "w+", newline='\n' )
        if is_cpp:
            file.write( "g++\n" )
        else:
            file.write( "gcc\n" )

        file.write( "-std=" + version + "\n" )
        file.write( "-I./src\n" )
        file.write( "-D_CLANGD=1\n" )

        for cflag in cflags:
            file.write(str(cflag) + "\n")

        file.close()
        status_message += "created file \"" + cflags_path + "\"\n"

    # create makefile

    makefile_path = main_dir + "/Makefile"
    if pathlib.Path( makefile_path ).is_file():
        if is_verbose and not(is_silent):
            print_err( "file \"" + makefile_path + "\" already exists" )
    else:
        file = open( makefile_path, "w+", newline='\n' )
        file.write( "# Desired compiler and C/C++ version\n" )
        cc = "CC = "
        if is_cpp:
            cc += "g++"
        else:
            cc += "gcc"
        cc += " -std=" + version + "\n"
        file.write( cc )

        file.write( "# change between DEBUG/RELEASE\n\n" )
        file.write( "# RELEASE BUILD\n" )
        file.write( "# CFLAGS = $(RELEASE)\n" )
        file.write( "# LNKFLAGS = --static -mwindows\n" )
        file.write( "# TARGETDIR = ./build/release\n\n" )

        file.write( "# DEBUG BUILD\n" )
        file.write( "CFLAGS = $(DEBUG)\n" )
        file.write( "LNKFLAGS = --static\n" )
        file.write( "TARGETDIR = ./build/debug\n\n" )

        file.write( "# executable name\n" )
        file.write( "EXE = " + project_name + ".exe\n\n" )

        file.write( "# source code paths\n" )
        src_paths = "./src"

        for dir in glob.iglob( main_dir + '/src/**', recursive=True ):
            if os.path.isdir( dir ):
                src_dir = str(dir).replace( main_dir + "/src\\", "" )
                if src_dir != "":
                    src_paths += " ./src/" + src_dir

        file.write( "SRC = " + src_paths + "\n\n" )

        file.write( "# defines\n" )
        makeflags_string = ""
        for flag in makeflags:
            makeflags_string += " " + flag
        file.write( "DEF =" + makeflags_string + "\n\n" )

        file.write( "# pre-compiled header\n" )
        file.write( "PCH = ./src/pch\n\n" )

        file.write( "# linker flags\n" )
        file.write( "LNK = -static-libstdc++ -static-libgcc -lmingw32\n\n" )

        file.write( "# DO NOT EDIT BEYOND THIS POINT!!! ======================================\n\n" )
        
        file.write( "DEBUG   = $(DFLAGS) $(foreach D, $(INC), -I$(D)) $(DEPFLAGS)\n" )
        file.write( "RELEASE = $(RFLAGS) $(foreach D, $(INC), -I$(D)) $(DEPFLAGS)\n\n" )

        file.write( "BINARY = $(TARGETDIR)/($EXE)\n\n" )

        file.write( "WARN     = -Wall -Wextra\n" )
        file.write( "DFLAGS   = $(WARN) $(DEF) -O0 -g -D DEBUG -march=native\n" )
        file.write( "RFLAGS   = $(DEF) -O2 -march=native\n" )
        file.write( "DEPFLAGS = -MP -MD\n" )
        file.write( "INC      = ./src\n\n" )

        file.write( "CPP  = $(foreach D, $(SRC), $(wildcard $(D)/*.cpp))\n" )
        file.write( "C    = $(foreach D, $(SRC), $(wildcard $(D)/*.c))\n" )
        file.write( "OBJ  = $(patsubst %.c,%.o, $(C)) $(patsubst %.cpp,%.o, $(CPP))\n" )
        file.write( "DEPS = $(patsubst %.c,%.d, $(C)) $(patsubst %.cpp,%.d, $(CPP))\n\n" )

        file.write( "PCH_TARG = $(PCH).gch\n\n" )

        file.write( "all: $(PCH_TARG) $(BINARY)\n\n" )

        file.write( "run: all\n\t$(BINARY)\n\n" )

        file.write( "-include $(DEPS)\n" )
        file.write( "$(BINARY): $(OBJ)\n" )
        file.write( "\t$(CC) -o $@ $(LIB) $^ $(LNK) $(LNKFLAGS)\n\n" )

        file.write( "%.o: %.c\n" )
        file.write( "\t$(CC) $(CFLAGS) -c -o $@ $<\n\n" )

        file.write( "%.o: %.cpp\n" )
        file.write( "\t$(CC) $(CFLAGS) -c -o $@ $<\n\n" )

        pch_ext = ".hpp"
        if not(is_cpp):
            pch_ext = ".h"

        file.write( "$(PCH_TARG): $(PCH)" + pch_ext + "\n" )
        file.write( "\t$(CC) $(CFLAGS) $(PCH)" + pch_ext + " -o $(PCH_TARG)\n\n" )

        file.write( "clean:\n\trm *.d, *.o, *.gch -r\n\n" )

        file.write( ".PHONY: all clean run\n" )

        file.close()
        status_message += "created file \"" + makefile_path + "\"\n"

    if not(is_silent):
        print_status( status_message )
    sys.exit(0)

# directory structure:
# 
# src
#   |- main.c/cpp
# build
#   |- debug
#   |- release
# bin
# .vscode
#    |- launch.json
# compile_flags.txt
# .gitignore
# Makefile
# README.md
# TODO.md

short_options = "hcsqvd:f:"
long_options  = [
    "help", "dir=", "flag=", "cflag=", "makeflag=",
    "init=", "silent", "quiet", "version=", "rename=",
    "no_readme", "no_todo", "compile_flags", "verbose"
]
valid_cpp_versions = [ "c++20", "c++17", "c++11" ]
valid_c_versions = [ "c89", "c99", "c11" ]

def print_help():
    print_cyan( "cproj: manage simple C/C++ project" )
    print_cyan( " --init [string]: create new project with given name in current directory" )
    print_cyan( "                  will name project \"project\" if no name is provided" )
    
    print_cyan( "\noptions only when initializing:" )
    print_cyan( " -c          [switch] [default=false]:     initialize project as C instead of C++. REQUIRES --init" )
    print_cyan( " --version   [string] [default=C++20/C99]: set C/C++ version. REQUIRES --init. VALID = [c++20, c++17, c++11, c89, c99, c11]" )
    print_cyan( " --no_readme [switch] [default=false]:     don't create readme. REQUIRES --init." )
    print_cyan( " --no_todo   [switch] [default=false]:     don't create todo. REQUIRES --init." )
    
    print_cyan( "\noptions when initializing or in existing project:" )
    print_cyan( " -d, --dir  [string]: create new directory in current project, adds directory to Makefile" )
    print_cyan( " -f, --flag [string]: add new compiler flag to compile_flags.txt and Makefile" )
    print_cyan( " --cflag    [string]: add new compiler flag only to compile_flags.txt" )
    print_cyan( " --makeflag [string]: add new compiler flag only to Makefile" )

    print_cyan( "\noptions only in existing project:" )
    print_cyan( " --rename        [string]: rename project" )
    print_cyan( " --compile_flags [switch]: create default compile_flags.txt if it doesn't already exist" )
    print_cyan( "           NOTE: can also take -c and -v/--version to define compiler options if --compile_flags is the first argument" )

    print_cyan( "\nmiscellaneous options:" )
    print_cyan( " -s, -q, --silent, --quiet [switch] [default=false]: don't print status" )
    print_cyan( " -v, --verbose             [switch] [default=false]: print extra error messages" )
    print_cyan( "\n -h, --help: print this help message and exit" )
    sys.exit(0)

if __name__ == "__main__":
    arg_list = sys.argv[1:]

    for i, opt in enumerate( arg_list ):
        if opt == "--init":
            next_index = i + 1
            if next_index >= len(arg_list):
                arg_list.append( "project" )
            elif '-' in arg_list[next_index]:
                arg_list.insert( next_index, "project" )

    try:
        args, values = getopt.getopt( arg_list, short_options, long_options )
    except getopt.error as err:
        print_fatal( "error: " + str(err) )

    project_name = "project"
    is_cpp       = True
    is_init      = False
    version      = ""
    cflags       = []
    makeflags    = []
    directories  = []
    rename       = ""
    create_readme = True
    create_todo   = True
    create_compile_flags = False
    silent  = False
    verbose = False

    c_default_version = "c99"
    cpp_default_version = "c++20"
    input_version = ""

    for current_arg, current_value in args:
        if current_arg in ( "-h", "--help" ):
            print_help()
        if current_arg == "--init":
            is_init = True
            if current_value != "":
                project_name = current_value
        if current_arg == "--compile_flags":
            if is_init:
                print_fatal( "cannot create default compile_flags.txt and initialize at the same time!" )
            else:
                create_compile_flags = True
        if current_arg == "-c":
            if is_init or create_compile_flags:
                is_cpp = False
            else:
                print_fatal( "cannot create a C project without --init or --compile_flags!" )
        if current_arg == "--version":
            if is_init or create_compile_flags:
                input_version = current_value
            else:
                print_fatal( "cannot set C/C++ version without --init or --compile_flags!" )
        if current_arg in ( "-d", "--dir" ):
            directories.append( "src/" + current_value )
        if current_arg in ( "-s", "-q", "--silent", "--quiet" ):
            silent = True
        if current_arg == "-f" or current_arg == "--flag":
            if create_compile_flags:
                print_fatal( "cannot add flags when creating default compile_flags.txt!" )
            else:
                cflags.append( current_value )
                makeflags.append( current_value )
        if current_arg == "--cflag":
            if create_compile_flags:
                print_fatal( "cannot add flags when creating default compile_flags.txt!" )
            else:
                cflags.append( current_value )
        if current_arg == "--makeflag":
            if create_compile_flags:
                print_fatal( "cannot add flags when creating default compile_flags.txt!" )
            else:
                makeflags.append( current_value )
        if current_arg == "--rename":
            if is_init:
                print_fatal( "cannot rename project and initialize at the same time!" )
            else:
                rename = current_value
        if current_arg == "--no_readme":
            if not(is_init):
                print_fatal( "no_readme is only a valid option when initializing a project!" )
            else:
                create_readme = False
        if current_arg == "--no_todo":
            if not(is_init):
                print_fatal( "no_todo is only a valid option when initializing a project!" )
            else:
                create_todo = False
        if current_arg in ( "-v", "--verbose" ):
            verbose = True

    if verbose and silent:
        print_fatal( "verbose and silent cannot be enabled simultaneously!" )

    if input_version != "":
        input_version = input_version.lower()
        if is_cpp:
            if input_version in valid_cpp_versions:
                version = input_version
            else:
                print_fatal("\"" + input_version + "\" is not a valid version of C++!")
        else:
            if input_version in valid_c_versions:
                version = input_version
            else:
                print_fatal("\"" + input_version + "\" is not a valid version of C!")
    else:
        if is_cpp:
            version = cpp_default_version
        else:
            version = c_default_version

    if is_init:

        status_message = "creating "
        if is_cpp:
            status_message += "C++"
        else:
            status_message += "C"

        status_message += " project \"" + project_name + "\".\n"

        if is_cpp:
            status_message += "C++"
        else:
            status_message += "C"
        status_message += " version: " + version + ".\n"

        directories.insert( 0, "src" )
        directories.append( "build" )
        directories.append( "build/debug" )
        directories.append( "build/release" )
        directories.append( "bin" )
        directories.append( ".vscode" )

        if not(silent):
            print_status( status_message )
        
        init(
            project_name, is_cpp, version,
            cflags, makeflags,
            directories, create_readme, create_todo,
            silent, verbose
        )
    else:
        if rename != "":
            rename_proj( rename, silent )

        if create_compile_flags:
            create_default_compile_flags( is_cpp, version, silent )
            sys.exit(0)

        if len( directories ) != 0:
            create_src_dir( directories, silent )

        if len( cflags ) != 0:
            add_cflags( cflags, silent )

        if len( makeflags ) != 0:
            add_makeflags( makeflags, silent )

    sys.exit(0)