#!/usr/bin/env python
# -*- coding: utf8 -*-

# ***************************************************************************
#
# Component Layers
#
# $Id: hsv_layers.py,v 1.71 2014/02/08 21:32:31 sjg Exp $
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

def makeMask( image, drawable, optype, pos ):

  if image.active_layer.mask != None:
    gimp.message( "Layer already has a mask.  Cannot proceed." )
    return

  # Basically this is a decompose op, creating a mask for the
  # decompose image that represents the component we want
  # and a copy and paste of that mask to the active layer.

  pdb.gimp_image_undo_group_start(image)
  
  im = pdb.plug_in_decompose( image, drawable, optype, 0 )
  
  msk = pdb.gimp_layer_create_mask( im[pos].layers[0], ADD_COPY_MASK )
  
  pdb.gimp_layer_add_mask( im[pos].layers[0], msk )
  
  pdb.gimp_edit_copy( msk )
  
  newmsk = pdb.gimp_layer_create_mask( image.active_layer, ADD_COPY_MASK )
    
  pdb.gimp_layer_add_mask( image.active_layer, newmsk )
  
  flt = pdb.gimp_edit_paste( newmsk, 0 )
  
  pdb.gimp_floating_sel_anchor( flt )
  
  # clean up the non-displayed temp images we made
  for img in im:
    # Note that "None" actually does appear in the list
    # so we do need to check
    if img != None:
      pdb.gimp_image_delete( img )
  
  pdb.gimp_image_undo_group_end( image )

  gimp.displays_flush()


def quickmask_R_RGB( image, drawable ):
  makeMask( image, drawable, "RGB", 0 )

def quickmask_G_RGB( image, drawable ):
  makeMask( image, drawable, "RGB", 1 )

def quickmask_B_RGB( image, drawable ):
  makeMask( image, drawable, "RGB", 2 )


def quickmask_H_HSV( image, drawable ):
  makeMask( image, drawable, "HSV", 0 )

def quickmask_S_HSV( image, drawable ):
  makeMask( image, drawable, "HSV", 1 )

def quickmask_V_HSV( image, drawable ):
  makeMask( image, drawable, "HSV", 2 )


def quickmask_L_LAB( image, drawable ):
  makeMask( image, drawable, "LAB", 0 )

def quickmask_A_LAB( image, drawable ):
  makeMask( image, drawable, "LAB", 1 )

def quickmask_B_LAB( image, drawable ):
  makeMask( image, drawable, "LAB", 2 )


def quickmask_C_CMY( image, drawable ):
  makeMask( image, drawable, "CMY", 0 )

def quickmask_Y_CMY( image, drawable ):
  makeMask( image, drawable, "CMY", 1 )

def quickmask_M_CMY( image, drawable ):
  makeMask( image, drawable, "CMY", 2 )


def quickmask_H_HSL( image, drawable ):
  makeMask( image, drawable, "HSL", 0 )

def quickmask_S_HSL( image, drawable ):
  makeMask( image, drawable, "HSL", 1 )

def quickmask_L_HSL( image, drawable ):
  makeMask( image, drawable, "HSL", 2 )


def quickmask_C_CMYK( image, drawable ):
  makeMask( image, drawable, "CMYK", 0 )

def quickmask_M_CMYK( image, drawable ):
  makeMask( image, drawable, "CMYK", 1 )

def quickmask_Y_CMYK( image, drawable ):
  makeMask( image, drawable, "CMYK", 2 )

def quickmask_K_CMYK( image, drawable ):
  makeMask( image, drawable, "CMYK", 3 )


def quickmask_Y_YCbCr_ITU_R470( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R470", 0 )

def quickmask_Cb_YCbCr_ITU_R470( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R470", 1 )

def quickmask_Cr_YCbCr_ITU_R470( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R470", 2 )


def quickmask_Y_YCbCr_ITU_R709( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R709", 0 )

def quickmask_Cb_YCbCr_ITU_R709( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R709", 1 )

def quickmask_Cr_YCbCr_ITU_R709( image, drawable ):
  makeMask( image, drawable, "YCbCr_ITU_R709", 2 )


def quickmask_Y_YCbCr_ITU_R470_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R470 256", 0 )

def quickmask_Cb_YCbCr_ITU_R470_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R470 256", 1 )

def quickmask_Cr_YCbCr_ITU_R470_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R470 256", 2 )


def quickmask_Y_YCbCr_ITU_R709_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R709 256", 0 )

def quickmask_Cb_YCbCr_ITU_R709_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R709 256", 1 )

def quickmask_Cr_YCbCr_ITU_R709_256( image, drawable ):
  makeMask( image, drawable, "YCbCr ITU R709 256", 2 )


# ***************************************************************************

def quickmask_register( shortname ):

  i = shortname.find( "_" )
  
  cn = shortname[:i]
  
  sn = shortname[(i+1):]
  
  # GIMP treats menu entries with underlines as accelator key markings
  # and will replace the underscore and next char with an underlined version
  # of that character.  So we replace the underscores with spaces.
  
  sn = sn.replace( "_", " " )

  desc = "Create a layer mask from the " + cn + " component of the " + sn + " representation of the image."
  
  # For the register call we need to construct some names
  # for the GIMP PDB, the menu entry and the function itself.
  #
  # The function is found by looking up globals() with the
  # name of the function required.
  #
  # GIMP's UI reorders sub-menu entries in alphabetical order,
  # which means we need to be careful about menu entries so
  # that the color spaces are close together in the menu.
  
register(
    "sjg_quickmask_" + cn + "_from_" + shortname[(i+1):],
    desc,
    desc,
    "Stephen Geary",
    "(©) 2014 Stephen Geary",
    "2014-02-07",
    "<Image>/Layer/Quick Mask/" + sn + " channel " + cn ,
    "RGB*",
    [
    ],
    [],
    globals()[ "quickmask_" + shortname ],
)


quickmask_register( "R_RGB" )
quickmask_register( "G_RGB" )
quickmask_register( "B_RGB" )

quickmask_register( "H_HSV" )
quickmask_register( "S_HSV" )
quickmask_register( "V_HSV" )

quickmask_register( "L_LAB" )
quickmask_register( "A_LAB" )
quickmask_register( "B_LAB" )

quickmask_register( "C_CMY" )
quickmask_register( "Y_CMY" )
quickmask_register( "M_CMY" )

quickmask_register( "H_HSL" )
quickmask_register( "S_HSL" )
quickmask_register( "L_HSL" )

quickmask_register( "C_CMYK" )
quickmask_register( "Y_CMYK" )
quickmask_register( "M_CMYK" )
quickmask_register( "M_CMYK" )

quickmask_register( "Y_YCbCr_ITU_R470" )
quickmask_register( "Cb_YCbCr_ITU_R470" )
quickmask_register( "Cr_YCbCr_ITU_R470" )

quickmask_register( "Y_YCbCr_ITU_R709" )
quickmask_register( "Cb_YCbCr_ITU_R709" )
quickmask_register( "Cr_YCbCr_ITU_R709" )

quickmask_register( "Y_YCbCr_ITU_R470_256" )
quickmask_register( "Cb_YCbCr_ITU_R470_256" )
quickmask_register( "Cr_YCbCr_ITU_R470_256" )

quickmask_register( "Y_YCbCr_ITU_R709_256" )
quickmask_register( "Cb_YCbCr_ITU_R709_256" )
quickmask_register( "Cr_YCbCr_ITU_R709_256" )


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

# ***************************************************************************


