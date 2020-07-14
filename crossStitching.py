from sys import maxsize
from PIL import Image
from math import sqrt

#returns a dictionary of DMC floss colors
def getFlossColors():
    flossColorsFile = open("dmcFlossColors.txt", 'r')
    colorDict = {}
    for line in flossColorsFile:
        elmnts = line.split(',')
        codeAndName = elmnts[0] + " " + elmnts[1]
        rgbaVal = (int(elmnts[2]), int(elmnts[3]), int(elmnts[4])) #add the alpha value of 1 because they're all opaque
        colorDict[codeAndName] = rgbaVal
    flossColorsFile.close()
    return colorDict

#finds 'difference' in colors, where color1 and color2 are RGB tuples
#according to info found on https://www.compuphase.com/cmetric.htm
def colorDifference(color1, color2):
    r = (color1[0] + color2[0])/2.0
    deltaR = abs(color1[0] - color2[0])
    deltaG = abs(color1[1] - color2[1])
    deltaB = abs(color1[2] - color2[2])
    colorDiff = sqrt((2+(r/256)) * (deltaR * deltaR) + 4 * (deltaG * deltaG) + (2 + (255 - r)/256) * (deltaB * deltaB))
    return colorDiff
    

#Parameters:
#   colorDict - dictionary of DMC floss color codes/names and rgb values
#   color - the color that we are trying to covert to DMC floss color code
#Returns: dictionary key of the closest DMCcolor
def findClosestColor(colorDict, color):
    minimum = maxsize
    key = ''
    for name in colorDict:
        if colorDifference(colorDict[name], color) < minimum:
            key = name
            minimum = colorDifference(colorDict[name], color)
    return key


#replaces colors in color palette with closest DMC floss color, then puts color palette in the image
#Parameters: image - PIL image to replace the colors in, colorDict - dictionary of DMC floss color codes/names and rgb values
#Returns: list of colors used in the palette by their keys to look them up in colorDict
def replaceColors(image, colorDict):
    colorPalette = image.getpalette()
    colorsList = []
    cont = True
    i = 0
    while cont:
        RGB = (colorPalette[i], colorPalette[i+1], colorPalette[i+2])
        replacementColorName = findClosestColor(colorDict, RGB)
        replacementColor = colorDict[replacementColorName]

        colorsList.append(replacementColorName)
        colorPalette[i] = replacementColor[0]
        colorPalette[i+1] = replacementColor[1]
        colorPalette[i+2] = replacementColor[2]

        i += 3

        #stop the loop if we're at the end OR the color palette is just zeroes
        if i >= len(colorPalette): cont = False
        elif colorPalette[i] == 0 and colorPalette[i+1] == 0 and colorPalette[i+2] == 0:
                cont = False
    image.putpalette(colorPalette)
    return colorsList
        

        
def main():

    fileName = input("Name of file containing image to convert to cross stitch pattern? ")
    width = int(input("Width of cross-stitch? "))
    height = int(input("Height of cross-stitch? "))

    colorDict = getFlossColors()

    #resize image to get ready for converting to a cross stitch pattern
    image = Image.open(fileName)
    resizedImg = image.resize((width, height)) #holds an image with one pixel for each cross-stitch square
    resizedImg = resizedImg.convert('RGB')


    #put img in 'P' mode, meaning it has a color palette
    #instead of storing rgb vals in pixels, it stores the index to the palette
    colorNumber = int(input("How many colors do you want to use?"))
    quantizedColorImg = resizedImg.quantize(colorNumber)
    quantizedColorImg.save("quantized.png")
    

    #convert all palette colors to DMC floss colors
    colorsList = replaceColors(quantizedColorImg, colorDict)
    quantizedColorImg.save("final.png")
    print(colorsList)


    #write the final cross stitch pattern to a pdf
    xStitchPattern = Image.new('RGB', (width*25,height*25)) #this will hold the final formatted pattern


if __name__ == "__main__":
    main()

#2. for each 'pixel', draw a rectangle on the cross stitch pattern with the correct DMC color, outlined in grey
#3. each rectangle on xStitchPattern is 25 pixels height and width
