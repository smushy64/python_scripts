# * Description:  Script for creating GLSL vertex/fragment source files
# * Author:       Alicia Amarilla ( smushyaa@gmail.com )
# * File Created: February 09, 2023

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

def create_vertex( name ):
    file_path = name + ".vs"

    file = open( file_path, "w+", newline='\n' )
    file.write( comment_info )
    file.write( "\n" + "#version 460 core\n" + "\nout struct {\n\n} v2f;\n\n" + "void main() {\n\n}\n" )

    file.close()
    print( termcolor.colored( "created glsl vertex source file \"" + file_path + "\"", "green" ) )

def create_fragment( name ):
    file_path = name + ".fs"

    file = open( file_path, "w+", newline='\n' )
    file.write( comment_info )
    file.write( "\n" + "#version 460 core\n" + "\nin struct {\n\n} v2f;\n\n" + "out vec4 FRAG_COLOR;\nvoid main() {\n\n}\n" )

    file.close()
    print( termcolor.colored( "created glsl fragment source file \"" + file_path + "\"", "green" ) )

if __name__ == "__main__":
    name_is_set = False
    name = "file"
    overwrite = False

    create_vertex_flag   = ( 1 << 0 )
    create_fragment_flag = ( 1 << 1 )

    flags = create_vertex_flag | create_fragment_flag

    for i, arg in enumerate( sys.argv ):
        match arg:
            case "--help" | "-h":
                print( termcolor.colored( "glnew: create new vertex and/or fragment source files for GLSL", "cyan" ) )
                print( termcolor.colored( "     -n, --name    [required] [string]: set name of file.", "cyan" ) )
                print( termcolor.colored( "                                        include parent directory if deeper in current directory.", "cyan" ) )
                print( termcolor.colored( "     --vertex        [switch] [default=false]:  only create a vertex file", "cyan" ) )
                print( termcolor.colored( "     --fragment      [switch] [default=false]:  only create a fragment file", "cyan" ) )
                print( termcolor.colored( "     -o, --overwrite [switch] [default=false]:  if file exists, overwrite", "cyan" ) )

                print( termcolor.colored( "\n     -h, --help: print this help message and exit", "cyan" ) )
                sys.exit()
            case "-n" | "--name":
                name_is_set = True
                name = sys.argv[i + 1]
            case "--vertex":
                flags &= ~create_fragment_flag
            case "--fragment":
                flags &= ~create_vertex_flag
            case "-o" | "--overwrite":
                overwrite = True
            case _:
                continue

    if not(name_is_set):
        print( termcolor.colored( "must set file name! run with -h or --help for more info", "red" ) )
        sys.exit()

    if check_flags( flags, create_vertex_flag ):
        if overwrite:
            create_vertex( name )
        else:
            if pathlib.Path( name + ".vs" ).is_file():
                print( termcolor.colored( "cannot create vertex source file \"" + name + ".vs" + "\". file already exists", "red" ) )
            else:
                create_vertex( name )

    if check_flags( flags, create_fragment_flag ):
        if overwrite:
            create_fragment( name )
        else:
            if pathlib.Path( name + ".fs" ).is_file():
                print( termcolor.colored( "cannot create fragment source file \"" + name + ".fs" + "\". file already exists", "red" ) )
            else:
                create_fragment( name )

