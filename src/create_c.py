import sys
import pathlib
from datetime import date
import termcolor

today = date.today()

comment_author = "Alicia Amarilla ( smushyaa@gmail.com )"
comment_date   = today.strftime( "%B %d, %Y" )
comment_info0  = "    * Description:  \n"
comment_info1  = "    * Author:       " + comment_author + "\n"
comment_info2  = "    * File Created: " + comment_date + "\n"

comment_info = "/**\n" + comment_info0 + comment_info1 + comment_info2 + "*/\n"

def check_flags( flag, mask ):
    return ( flag & mask ) != 0

def create_source( name, ext, created_header_file ):
    file_path = name + ext

    file = open( file_path, "w+", newline='\n' )
    file.write( comment_info )

    header_ext = ".h"
    if ext == ".cpp":
        header_ext = ".hpp"

    if created_header_file:
        file.write( "#include \"" + name + header_ext + "\"" )

    file.close()
    print( termcolor.colored( "created source file \"" + file_path + "\"", "green" ) )

def create_header( name, ext, no_pragma ):
    file_path = name + ext

    file = open( file_path, "w+", newline='\n' )
    file.write( comment_info )

    if not(no_pragma):
        file.write( "#pragma once" )
    file.close()
    print( termcolor.colored( "created header file \"" + file_path + "\"", "green" ) )

if __name__ == "__main__":
    name_is_set = False
    name = "file"
    is_cpp = True
    overwrite = False
    no_pragma = False

    create_header_flag = ( 1 << 0 )
    create_source_flag = ( 1 << 1 )

    flags = create_header_flag | create_source_flag

    for i, arg in enumerate( sys.argv ):
        match arg:
            case "--help" | "-h":
                print( termcolor.colored( "cnew: create new header and/or source file for C/C++", "cyan" ) )
                print( termcolor.colored( "     -n, --name [required] [string]: set name of file.", "cyan" ) )
                print( termcolor.colored( "                                     include parent directory if deeper in current directory.", "cyan" ) )
                print( termcolor.colored( "     --header              [switch] [default=false]:  only create a header file", "cyan" ) )
                print( termcolor.colored( "     --source              [switch] [default=false]:  only create a source file", "cyan" ) )
                print( termcolor.colored( "     -o, --overwrite       [switch] [default=false]:  if file exists, overwrite", "cyan" ) )
                print( termcolor.colored( "     --no_pragma           [switch] [default=false]:  don't write pragma once in header file", "cyan" ) )
                print( termcolor.colored( "     -c                    [switch] [default=false]:  create .c and .h instead of .cpp and .hpp", "cyan" ) )

                print( termcolor.colored( "\n     -h, --help: print this help message and exit", "cyan" ) )
                sys.exit()
            case "-n" | "--name":
                name_is_set = True
                name = sys.argv[i + 1]
            case "--header":
                flags &= ~create_source_flag
            case "--source":
                flags &= ~create_header_flag
            case "-o" | "--overwrite":
                overwrite = True
            case "-c":
                is_cpp = False
            case "--no_pragma":
                no_pragma = True
            case _:
                continue
    
    if not(name_is_set):
        print( termcolor.colored( "must set file name! run with -h or --help for more info", "red" ) )
        sys.exit()

    created_header_file = check_flags( flags, create_header_flag )
    if created_header_file:
        ext = ".h"
        if is_cpp:
            ext = ".hpp"

        file_path = name + ext

        if overwrite:
            create_header(name, ext, no_pragma)
        else:
            if pathlib.Path(file_path).is_file():
                print( termcolor.colored( "cannot create header file \"" + file_path + "\". file already exists", "red" ) )
            else:
                create_header(name, ext, no_pragma)

    if check_flags( flags, create_source_flag ):
        ext = ".c"
        if is_cpp:
            ext = ".cpp"

        file_path = name + ext

        if overwrite:
            create_source(name, ext, created_header_file)
        else:
            if pathlib.Path(file_path).is_file():
                print( termcolor.colored( "cannot create source file \"" + file_path + "\". file already exists", "red" ) )
            else:
                create_source(name, ext, created_header_file)

