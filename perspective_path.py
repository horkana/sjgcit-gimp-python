#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Perspective and Rotation Transform using paths to control operation

$Id: perspective_path.py,v 1.30 2014/02/17 17:16:13 sjg Exp $

(c) Stephen Geary, Feb 2014

2014.02.17 - SJG - Make sure gimp_undo_group_start() is not called until
                        after all possible returns due to detected errors.
2014.02.12 - SJG - Added rotation by path tool

'''



from gimpfu import *
import sys
import time
import gtk
import math

#----------------------------------------------------------------------------------

def plugin_rotate( image, drawable ):

    # get points for transform from image
    
    vectors = pdb.gimp_image_get_active_vectors(image)
    
    nstrokes, strokes = pdb.gimp_vectors_get_strokes(vectors)
    
    if nstrokes == 0:
        # must be at least one stroke or we have no points
        gimp.message( "No strokes found" )
        return
    
    stoke_type, n_points, p, closed = pdb.gimp_vectors_stroke_get_points(vectors, strokes[0])
    
    if n_points != 12:
        # Note that each (x,y) ordinate pairs becomes 6 values per ordinate pair
        gimp.message( "Only found " + str(n_points/6) + " points, need 2" )
        return
    
    # do the transformation
    
    pdb.gimp_context_set_transform_direction( TRANSFORM_FORWARD )
    
    cx = image.width/2
    cy = image.height/2
    
    # note that y ordinates are opposite from what you expect
    # in maths, as the top is zeroand the bottom is positive
    
    y7 =image.height - 1 - p[7]
    y1 =image.height - 1 - p[1]
    
    if p[6] > p[0]:
        angle = math.atan2( y7-y1, p[6]-p[0] )
    else:
        angle = math.atan2( y1-y7, p[0]-p[6] )
    
    r45 = math.pi / 4.0
    r90 = math.pi / 2.0
    r135 = r45 + r90
    
    if angle > 0 :
        if angle > r45:
            angle2 = angle - r90
        else:
            angle2 = angle
    else:
        absangle = math.fabs( angle )
    
        if absangle > r45:
            angle2 = r90 - absangle
        else:
            angle2 = angle
    
    pdb.gimp_image_undo_group_start(image)

    pdb.gimp_item_transform_rotate( drawable, angle2, True, cx, cy )
    

    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

#----------------------------------------------------------------------------------

def plugin_perspective( image, drawable ):

    # get points for transform from image
    
    vectors = pdb.gimp_image_get_active_vectors(image)
    
    nstrokes, strokes = pdb.gimp_vectors_get_strokes(vectors)
    
    if nstrokes == 0:
        # must be at least one stroke or we have no points
        gimp.message( "No strokes found" )
        return
    
    stoke_type, n_points, p, closed = pdb.gimp_vectors_stroke_get_points(vectors, strokes[0])
    
    if n_points != 24:
        # Note that each (x,y) ordinate pairs becomes 6 values per ordinate pair
        gimp.message( "Only found " + str(n_points/6) + " points, need 4" )
        return
    
    # if force flag is True then we map the points to the top and bottom of
    # the time by projecting lines from the points we have.  This will produce
    # a perspective correction suitable for focing building verticals to be
    # vertical in the final image ( assuming you choose points on the
    # correct lines in the image ).
    
    # map the points to the top and bottom of the image

    w = drawable.width
    h = drawable.height

    a = ( p[7] - p[1] ) / ( p[6] - p[0] )
    b = p[7] - ( a * p[6] )

    c = ( p[19] - p[13] ) / ( p[18] - p[12] )
    d = p[19] - ( c * p[18] )
    
    # now work out the intersection of the two lines
    
    x0 = ( d - b ) / ( a - c )
    
    y0 = ( a * x0 ) + b
    
    # if y0 < 0 then the point is above the image otherwise it is below
    #
    # we use this to work out the bounding box we need
    
    q = []
    
    if y0 < 0:
        # intersection above image
        # use bounding box based on bottom corners of image
        
        q.append( -( ( h-1 )*x0 ) / (y0+1-h) )
        q.append( 0 )
        
        q.append( ( h*x0 - x0 - w*y0 + y0 ) / ( h - 1 - y0 ) )
        q.append( 0 )
        
        q.append( 0 )
        q.append( h-1 )
        
        q.append( w-1 )
        q.append( h-1 )
        
    else:
        # intersection below image
        # use bounding box based on top corners of image
        
        q.append( 0 )
        q.append( 0 )
        
        q.append( w-1 )
        q.append( 0 )
        
        q.append( ( x0*(h-1) ) / y0 )
        q.append( h-1 )
        
        q.append( ( y0*w - y0 + x0*h - x0 - (h-1)*(w-1) ) / y0 )
        q.append( h-1 )


    # need to work out the box to map to
    # we do this by using the middle two x and y ordinates of the
    # given points.  We map to this.
    
    # do the transformation
    
    pdb.gimp_image_undo_group_start(image)

    pdb.gimp_context_set_transform_direction( TRANSFORM_BACKWARD )

    pdb.gimp_item_transform_perspective( drawable, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7] )
    

    gimp.displays_flush()

    pdb.gimp_image_undo_group_end(image)

#----------------------------------------------------------------------------------

register(
    "python_fu_sjg_perspective",
    "Perspective transform using path from image.",
    "Perspective transform using path from image.",
    "Stephen Geary, ( sg euroapps com )",
    "(c) 2014, Stephen Geary",
    "2014",
    "<Image>/Tools/Transform Tools/SJG Perspective from path",
    "*",
    [
    ],
    [],
    plugin_perspective,
)

register(
    "python_fu_sjg_rotate",
    "Rotate to horizontal or vertical using path from image.",
    "Rotate to horizontal or vertical using path from image.",
    "Stephen Geary, ( sg euroapps com )",
    "(c) 2014, Stephen Geary",
    "2014",
    "<Image>/Tools/Transform Tools/SJG Rotation from path",
    "*",
    [
    ],
    [],
    plugin_rotate,
)

main()

#----------------------------------------------------------------------------------

