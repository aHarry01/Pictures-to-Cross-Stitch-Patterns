from sys import maxsize
from PIL import Image, ImageDraw, ImageFont
from math import sqrt, ceil

#formatter for final output PDF pattern
class Formatter:
    def __init__(self, image, width, height, sectionSize, cellSize):
        self.image = image
        self.width = width
        self.height = height
        self.pages = []
        self.sectionWidth = sectionSize # the width, in number of stitches, in a blown up section
        self.sctnCellSize = cellSize #width, in pixels, of the cells in blown up section
        self.fullCellSize = 0 #width, in pixels, of the cells in the full pattern


    def calculateFullCellSize(self):
        self.fullCellSize = int( (self.sectionWidth * self.sctnCellSize) / self.width  )

    def createFullPattern(self):
        self.calculateFullCellSize()
        fullPattern = Image.new('RGB', (self.fullCellSize*self.width, self.fullCellSize*self.height))
        fullPatternDraw = ImageDraw.Draw(fullPattern)
        fullPatternDraw.rectangle([(0,0),(self.fullCellSize*self.width,self.fullCellSize*self.height)], fill='white') #white background
        palette = self.image.getpalette()
        
        for x in range(self.width):
            for y in range(self.height):
                #draw a rectange with the correct color + pattern
                i = self.image.getpixel((x,y))
                color = (palette[i*3],palette[(i*3)+1],palette[(i*3)+2])
                fullPatternDraw.rectangle([(x*self.fullCellSize, y*self.fullCellSize), ((x+1)*self.fullCellSize, (y-1)*self.fullCellSize)],fill=color, outline="gray")
                   
        self.pages.append(fullPattern)

    def createThreadColorKey(self, colorsList):
        keyPage = Image.new("L", (self.fullCellSize*self.width, self.fullCellSize*self.height))
        font = ImageFont.truetype("arial.ttf",20)
        draw = ImageDraw.Draw(keyPage)
        draw.rectangle([0,0,(self.fullCellSize*self.width, self.fullCellSize*self.height)], fill="white")

        seperator = "\n"
        text = seperator.join(colorsList)
        draw.multiline_text((10,10),text)
        
        self.pages.append(keyPage)

    #will split the full pattern into a grid of smaller sections
    #creates a page for each of these magnified sections of the full pattern
    def createSections(self):

        sectionHeight = int(self.sectionWidth * 1.2941) #standard letter paper aspect ratio
        
        sectionCols = ceil(self.width / self.sectionWidth)
        sectionRows = ceil(self.height / sectionHeight)

        palette = self.image.getpalette()
        
        for row in range(sectionRows):
            for col in range(sectionCols):
                self.pages.append(Image.new('RGB', (self.sectionWidth*self.sctnCellSize, sectionHeight * self.sctnCellSize)))
                sectionDraw = ImageDraw.Draw(self.pages[-1])
                sectionDraw.rectangle([(0,0), (self.sectionWidth*self.sctnCellSize, sectionHeight * self.sctnCellSize)],fill="white") #white background

                #finds corresponding pixels in original image
                leftPixel = col*self.sectionWidth
                topPixel = row*sectionHeight
                rightPixel = leftPixel + self.sectionWidth
                bottomPixel = topPixel + sectionHeight

                rightPixel = self.width if rightPixel > self.width else rightPixel
                bottomPixel = self.height if bottomPixel > self.height else bottomPixel

                for xPixel in range(leftPixel, rightPixel):
                    for yPixel in range(topPixel, bottomPixel):
                        i = self.image.getpixel((xPixel,yPixel))
                        color = (palette[i*3],palette[(i*3)+1],palette[(i*3)+2])
                        sectionDraw.rectangle([((xPixel-leftPixel)*self.sctnCellSize,(yPixel-topPixel)*self.sctnCellSize),
                                              ((xPixel-leftPixel+1)*self.sctnCellSize,(yPixel-topPixel-1)*self.sctnCellSize)], fill=color, outline="gray")

    #creates the pages of the pdf and adds it to self.pages
    #first page = full pattern
    #second page = list of DMC thread colors and their corresponding symbols
    #last pages = pattern split up into blown-up sections that are easier to see and follow
    def createPages(self, colorsList):
        self.createFullPattern()
        self.createThreadColorKey(colorsList)
        self.createSections()
        self.pages[0].save("finalPattern.pdf", "PDF",save_all=True,append_images=self.pages[1:])
        
        
   

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
    return list(dict.fromkeys(colorsList)) #remove any repeats that many show up because colors in the palette correspond to the same color
        
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

    #convert all palette colors to DMC floss colors
    colorsList = replaceColors(quantizedColorImg, colorDict)

    #format PDF of pattern and save it
    print("--- Final Pattern Formatting Options ---")
    CELLSIZE = int(input("Pixel size of the cells in the magnified sections of the pattern? ")) #size, in pixels, of the cells in the blown up sections of the pattern
    SCTNSIZE = int(input("Width per magnified section (in stitches) in the final pattern? ")) #width, in stitches, of the smaller blown up portions of the final pattern pdf. height will be int(SCTNSIZE*1.2941)
    
    formatter = Formatter(quantizedColorImg, width, height, SCTNSIZE, CELLSIZE)
    formatter.createPages(colorsList)


    
if __name__ == "__main__":
    main()

