# Pictures to Cross Stitch Patterns

This is a Python program that converts a picture (png or jpg) into a counted cross stitch embroidery pattern. Currently it outputs a picture that uses a set number of DMC thread colors. Eventually, it will output a .png containing a full color and symbol cross stitch pattern.

## Dependencies
* [Python 3.xx](https://www.python.org/downloads/) 
* [Pillow (7.2)](https://pillow.readthedocs.io/en/stable/)

## Usage
dmcFlossColors.txt and crossStitching.py must be in the same directory. Run crossStitching.py with a Python interpreter. The program will prompt you for the file name of the picture to be converted to a cross stitch pattern, relative or absolute filenames work. It will ask for the width, height and the number of thread colors you want to be used in the final pattern. The final picture will be saved in the same directory as crossStitching.py as final.png.

## Release History
* .0.0.1
    * Work in progress
    * Outputs a picture that uses a set number of DMC thread colors

