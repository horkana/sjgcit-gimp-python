
'''
Perspective Transform using paths to control operation

$Id: perspective_path.py,v 1.7 2014/02/07 02:48:53 sjg Exp $

(c) Stephen Geary, Feb 2014
'''



from gimpfu import *
import sys
import time
import gtk
import math

#----------------------------------------------------------------------------------



def plugin_perspective( image, drawable ):

  pdb.gimp_image_undo_group_start(image)

  # get points for transform from image
  
  vectors = pdb.gimp_image_get_active_vectors(image)
  
  nstrokes, strokes = pdb.gimp_vectors_get_strokes(vectors)
  
  if nstrokes == 0:
    # must be at least one stroke or we have no points
    gimp.message( "No strokes found" )
    return
  
  stoke_type, n_points, p, closed = pdb.gimp_vectors_stroke_get_points(vectors, strokes[0])
  
  if n_points != 24:
    # Note that 8 (x,y) ordinate pairs becomes 6 values per ordinate pair
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
        "<Image>/Tools/Transform Tools/Perspective from path",
        "*",
        [
        ],
        [],
        plugin_perspective,
        )

main()

