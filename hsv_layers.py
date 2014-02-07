#!/usr/bin/env python
# -*- coding: utf8 -*-

# ***************************************************************************
#
# Component Layers
#
# $Id: hsv_layers.py,v 1.15 2014/02/07 13:11:45 sjg Exp $
#
# (c) Stephen Geary, Apr 2011
#
# Split an layer into separate color component Layers in different spaces
#
# ***************************************************************************

from gimpfu import *
import math,random
from array import array

# ***************************************************************************

def plugin_spaces( idx ):

  if not hasattr( plugin_spaces, "colorspaces" ):
    # initialize
    plugin_spaces.colorspaces = [ "RGB", "HSV", "LAB", "HSL", "CMY" ]

  if idx == -1:
    return plugin_spaces.colorspaces
  else:
    return plugin_spaces.colorspaces[idx]

# ***************************************************************************

def sjg_component_layers( image, drawable, spaceidx ):

    colorspace = plugin_spaces( spaceidx )

    pdb.gimp_image_undo_group_start(image)
    
    im = pdb.plug_in_decompose( image, drawable, colorspace, 0 )
    
    l0 =   pdb.gimp_layer_new_from_visible( im[0], image, colorspace[0] + " component" )
    l1 =   pdb.gimp_layer_new_from_visible( im[1], image, colorspace[1] + " component" )
    l2 =   pdb.gimp_layer_new_from_visible( im[2], image, colorspace[2] + " component" )
    
    image.add_layer( l0, -1 )
    image.add_layer( l1, -1 )
    image.add_layer( l2, -1 )
    
    pdb.gimp_image_undo_group_end(image)

    gimp.displays_flush()



# ***************************************************************************

register(
  "sjg_component_layers_fn",
  "Split a layer into different color space component layers",
  "Split a layer into different color space component layers",
  "Stephen Geary",
  "(©) 2011 Stephen Geary",
  "2011-04-23",
  "<Image>/Colors/Components/Color Component Layers",
  "RGB*",
  [
    ( PF_OPTION, "spaceidx", "Component Space", 0, plugin_spaces(-1) )
  ],
  [],
  sjg_component_layers,
  )

main()


