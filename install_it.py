'''
Install a GIMP scheme script via a basic GUI

$Id: install_it.py,v 1.19 2015/03/20 16:55:02 sjg Exp $

(c) Stephen Geary, Mar 2015

'''



from gimpfu import *
import sys
import time
import gtk
import math
import stat
import shutil
import os

#----------------------------------------------------------------------------------

def plugin_install_pyorscm( filename ):
    
    ext = filename.split(".")[-1]
    
    ext = ext.lower()
    
    print "filename = ", filename
    print "ext = ", ext
    
    dstdir = ""
    
    if ext == "py":
        dstdir = "plug-ins"
    elif ext == "scm":
        dstdir = "scripts"
    else:
        gimp.message( "File was neither a Python plug-in nor a Scheme script." )
        return
    
    dst = os.path.join( gimp.directory, dstdir )
    dst = os.path.join( dst, os.path.basename( filename ) )
    
    print "dst = ", dst
    
    gimp.message( "plugin_install_pyorscm :: " + dst )
    
    shutil.copyfile( filename, dst )
    
    # if this is a Unix like OS then we need to set the file permissions
    # to allow execution of the file
    # But os.chmod() on Windows should ignore all bits except read
    # so it's safe to use that to do it.

    if ext == "py":
        os.chmod( dst, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH )


#----------------------------------------------------------------------------------

register(
    "python_fu_sjg_install_pyorscm",
    "Install a GIMP Scheme script or Python plug-in",
    "Install a GIMP Scheme script or Python plug-in",
    "Stephen Geary, ( sjgcit gmail com )",
    "(c) 2015, Stephen Geary",
    "2015",
    "Install Scheme Script or Python plugin",
    "",
    [
        (PF_FILE, 'filename', 'The name of the file to load', ""),
    ],
    [],
    plugin_install_pyorscm,
    menu = "<Image>/Filters",
    )


main()

