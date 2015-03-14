This repository contain various Python scripts for GIMP.

The perspectiv_path plugin contain TWO routines.  Both take a vector path as a parameter ( easily created from the
GIMP vector path tool ) and simply generate a rotation or perspective correction from that path.  They're pretty
intuitive, the idea being you visually select points on the path that define what you want to be parallel ( in the
case of perspective corection ) or horizontal or vertical ( in the case of rotation ).

HSV_Layers is a set of quick layer mask creation tools to add a layer mask based on one component of a selected color
space.  I find such layer masks useful in some editing situation, but they can be tedious to make any other way.
