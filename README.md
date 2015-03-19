This repository contain various Python scripts for GIMP.

The perspective_path plugin contain TWO routines.  Both take a vector path as a parameter ( easily created from the
GIMP vector path tool ) and simply generate a rotation or perspective correction from that path.  They're pretty
intuitive, the idea being you visually select points on the path that define what you want to be parallel ( in the
case of perspective corection ) or horizontal or vertical ( in the case of rotation ).

HSV_Layers is a set of quick layer mask creation tools to add a layer mask based on one component of a selected color
space.  I find such layer masks useful in some editing situation, but they can be tedious to make any other way.

An example showing how to use the Perspective From Path tool is below.

**Example of Perspective Path Tool**

We start with a shape that has edges we want vertical.

First we choose the path tool.

Then we use it to mark a path of four points.  We start at one corner of the edges we want vertical, then proceed to the next point on our first vertical, and then move to the other edge we want vertical.  You'd normally use the counter-clockwise arrangement I have shown in 1-2-3-4, but you can experiment with the alternative orgeing and see what whackiness happens !

After that you just select the tool from the Tools->Transform Tools menu and the rest is done for you.

![JPEG showing steps to apply perspective from path tool.](https://farm9.staticflickr.com/8752/16852617191_6389508c22_b_d.jpg)




