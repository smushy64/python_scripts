# * Description:  Script for creating Python scripts
# * Author:       Alicia Amarilla ( smushyaa@gmail.com )
# * File Created: February 09, 2023

import sys
import pathlib
from datetime import date
import termcolor

today = date.today()

comment_author = "Alicia Amarilla ( smushyaa@gmail.com )"
comment_date   = today.strftime( "%B %d, %Y" )
comment_info0  = "# * Description:  \n"
comment_info1  = "# * Author:       " + comment_author + "\n"
comment_info2  = "# * File Created: " + comment_date + "\n"

comment_info = comment_info0 + comment_info1 + comment_info2 + "\n"

def create_script( file_path ):
    file = open( file_path, "w+", newline='\n' )
    file.write( comment_info )
    file.write( "import sys\n\n" )
    file.write( "if __name__ == \"__main__\":\n    sys.exit()" )

    file.close()
    print( termcolor.colored( "created python script \"" + file_path + "\"", "green" ) )

if __name__ == "__main__":
    name_is_set = False
    name = "file"
    overwrite = False

    for i, arg in enumerate( sys.argv ):
        match arg:
            case "--help" | "-h":
                print( termcolor.colored( "pynew: create new Python script", "cyan" ) )
                print( termcolor.colored( "    -n, --name [required] [string]: set name of file.", "cyan" ) )
                print( termcolor.colored( "                                    include parent directory if deeper in current directory.", "cyan" ) )
                print( termcolor.colored( "    -o, --overwrite       [switch] [default=false]:  if file exists, overwrite", "cyan" ) )

                print( termcolor.colored( "\n    -h, --help: print this help message and exit", "cyan" ) )
                sys.exit()
            case "-n" | "--name":
                name_is_set = True
                name = sys.argv[i + 1]
            case "-o" | "--overwrite":
                overwrite = True
            case _:
                continue
    
    if not(name_is_set):
        print( termcolor.colored( "must set file name! run with -h or --help for more info", "red" ) )
        sys.exit()

    file_path = name + ".py"
    if overwrite:
        if pathlib.Path(file_path).is_file():
            print( termcolor.colored( "cannot create script \"" + file_path + "\". file already exists", "red" ) )
        else:
            create_script( file_path )
    else:
        create_script( file_path )
