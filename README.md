# Pictures to Cross Stitch Patterns

This is a Python program that converts a picture (png or jpg) into a counted cross stitch embroidery pattern. Currently it outputs a .pdf containing a full color cross stitch pattern, along with several pages of the pattern split into smaller parts, and finally a list of DMC thread colors needed. Future versions plan to include numbered grid lines, every 5th grid line bolded so it's easier to read the pattern and symbol patterns as well as color patterns.

## Dependencies
* [Python 3.xx](https://www.python.org/downloads/) 
* [Pillow (7.2)](https://pillow.readthedocs.io/en/stable/)

## Usage
dmcFlossColors.txt and crossStitching.py must be in the same directory. Run crossStitching.py with a Python interpreter. The program will prompt you for the file name of the picture to be converted to a cross stitch pattern. It will ask for the number of stitches you want (width and height) and the maximum number of thread colors you want to be used in the final pattern. Then it will ask for some information on how to format the final pdf. The first is the pixel size of the cells in the magnified sections and the second is the number of stitches in the width of the magnified sections. The final pattern will be saved in the same directory as crossStitching.py as finalPattern.pdf.

## License
Licensed under MIT license. See LICENSE.txt for more information.
