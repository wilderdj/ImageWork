'''
Created on Jan 6, 2020

@author: nicomp

pip install --user Pillow
https://www.pythonforbeginners.com/gui/how-to-use-pillow
http://code.nabla.net/doc/PIL/api/PIL/JpegImagePlugin/PIL.JpegImagePlugin.JpegImageFile.html
https://pillow.readthedocs.io/en/3.0.x/handbook/tutorial.html
https://pillow.readthedocs.io/en/stable/reference/Image.html#functions
'''

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os, sys
import requests
from io import BytesIO
from image_functions import *
    
def save_image( imageObject, outfilename ) :
    '''
    Save an image to disk
    :param imageObject: The Image to save
    :param outfilename: The target file
    '''
    imageObject.save( outfilename )

def blur_image(imageObject):
    blurred = imageObject.filter(ImageFilter.BLUR)    # Doesn't look too different but it does blur a little. Depends on the original image
#    blurred = imageObject.filter(ImageFilter.EMBOSS)    # This produces dramatic results. 
#    blurred = imageObject.filter(ImageFilter.DETAIL)    # Doesn't look different 
    return blurred

def remove_red(imageObject):
    new_image = Image.new('RGB', (imageObject.size[0], imageObject.size[1]))
    for i in range(imageObject.size[0]):
        for j in range(imageObject.size[1]):
            old_pixel = imageObject.getpixel((i, j))
            # old_pixel is a 3-value tuple with red, green, blue values
#            new_pixel = Image.Pixel(0, old_pixel.getGreen(), old_pixel.getBlue())
#            print (type(old_pixel))
            r = old_pixel[0]
            g = old_pixel[1]
            b = old_pixel[2]
            new_image.putpixel((i, j), (0, g, b))
    return new_image        
def remove_blue(imageObject):
    new_image = Image.new('RGB', (imageObject.size[0], imageObject.size[1]))
    for i in range(imageObject.size[0]):
        for j in range(imageObject.size[1]):
            old_pixel = imageObject.getpixel((i, j))
            # old_pixel is a 3-value tuple with red, green, blue values
#            new_pixel = Image.Pixel(0, old_pixel.getGreen(), old_pixel.getBlue())
#            print (type(old_pixel))
            r = old_pixel[0]
            g = old_pixel[1]
            b = old_pixel[2]
            new_image.putpixel((i, j), (r, g, 0))
    return new_image        
def remove_green(imageObject):
    new_image = Image.new('RGB', (imageObject.size[0], imageObject.size[1]))
    for i in range(imageObject.size[0]):
        for j in range(imageObject.size[1]):
            old_pixel = imageObject.getpixel((i, j))
            # old_pixel is a 3-value tuple with red, green, blue values
#            new_pixel = Image.Pixel(0, old_pixel.getGreen(), old_pixel.getBlue())
#            print (type(old_pixel))
            r = old_pixel[0]
            g = old_pixel[1]
            b = old_pixel[2]
            new_image.putpixel((i, j), (r, 0, b))
    return new_image        
            
            
            
            
            
def demo01():
    #imageName = 'moving still image 01.jpg'
    imageName = "SiriusAndViolet.jpg"
    
    myImage = load_image(imageName)
    print ('*****************')
    print ("The mode of the Image is: " + myImage.mode)
    print(myImage.format, myImage.size, myImage.mode)
    print ('*****************')
    #save_image(myImage, "catsout.jpg")
    
    blurred = blur_image(myImage)
    #myImage.show()
    #blurred.show()
    
    # save the new image
    blurred.save("blurred.JPG")
    
    noRed = remove_red(myImage)
    noBlueOrRed = remove_blue(noRed)
    #noBlueOrRed.show()
    noBlueOrRedOrGreen = remove_green(noBlueOrRed)
    noBlueOrRedOrGreen.show() # Ooops. Nothing to see here!


def write_text_to_image(imageFile, text):
    '''
    Write text onto an existing image
    :param imageFile: The image file name
    :param text: The text to write onto the image
    '''
    #**************************************************
    #* Add text to an image
    #* https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    #* https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
    #* Free fonts: https://www.fontsquirrel.com/fonts/list/classification/sans%20serif
    #**************************************************
    myImage = load_image(imageFile);
    draw = ImageDraw.Draw(myImage)
    # https://stackoverflow.com/questions/47694421/pil-issue-oserror-cannot-open-resource
    fontStyle = ImageFont.truetype("Aaargh.ttf", 48)     # font must be in the same folder as the .py file. 
    draw.text((30, 20), text, (0,0,0),font=fontStyle)    # Write in black
    
    draw.line((0, 0) + myImage.size, fill=128)
    draw.line((0, myImage.size[1], myImage.size[0], 0), fill=128)
    
    myImage.save('sample-out.jpg')

def Demo02():
    write_text_to_image("birds.jpg", "Hello World!")
    
def create_thumbnail_using_pillow(filename, size):    
#    Copied from https://pillow.readthedocs.io/en/3.0.x/handbook/tutorial.html
    outfile = os.path.splitext(filename)[0] + "_thumbnail.jpg"
    if filename != outfile:
        try:
            im = Image.open(filename)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print("cannot create thumbnail for", filename)
            
def create_thumbnail(filename, destinationFilename, show):    
    '''
    :param filename: Source file of original image
    :param destinationFilename: Where to write the thumbnail
    :param show: if true, open the thumbnail in a GUI window
    '''
    myImage = load_image(filename);
    scale = 10
    iOffset = -1
    jOffset = 0
    new_image = Image.new('RGB', (int(myImage.size[0]/scale + 1), int(myImage.size[1]/scale + 1)))
    print("Original image is (" + str(myImage.size[0]) + " by " + str(myImage.size[1]) + ")")
    print("New image is (" + str(new_image.size[0]) + " by " + str(new_image.size[1]) + ")")
    for i in range(myImage.size[0]):
        jOffset = 0
        if (i%scale==0):
            iOffset = iOffset + 1
        for j in range(myImage.size[1]):
            if (i % scale == 0 and j % scale == 0):
                old_pixel = myImage.getpixel((i, j))
#               print(str(i) + ", " + str(j) + "  " + str(old_pixel) + " to (" + str(iOffset) + ", " + str(jOffset) + ")")
                try:
                    new_image.putpixel((iOffset, jOffset), old_pixel)
                except:
                    pass
                jOffset = jOffset + 1
    new_image.save(destinationFilename)
    if (show):
        new_image.show()
 
def apply_point_transform_remove_all_but_black(filename): 
    # multiply each pixel by 1.2
    myImage = load_image(filename);
    # We are essentially removing everything but black...
    out = myImage.point(lambda i: i * 5)    # 255 is white so the larger all the pixel values get, the closer they get to white
    save_image(out, os.path.splitext(filename)[0] + "_transform.jpg")

def apply_point_transform_push_all_toward_black(filename): 
    # multiply each pixel by 1.2
    myImage = load_image(filename);
    # We are essentially reducing all the pixels toward 0, which is black...
    out = myImage.point(lambda i: int(i / 5.0))    # 0 is black so the smaller all the pixel values get, the closer they get to black
    save_image(out, os.path.splitext(filename)[0] + "_transform.jpg")

def split_image_into_bands(filename):
    img = Image.open(filename)
    data = img.getdata()
    # Suppress specific bands into three new images (e.g. (x, 0, 0) is red)
    red = [(d[0], 0, 0) for d in data]  # List Comprehension!
    green = [(0, d[1], 0) for d in data]
    blue = [(0, 0, d[2]) for d in data]

    # Reuse the image object to create the three new images. It's convenient because the dimensions are the same
    img.putdata(red)    # This overwrites whatever was in the image
    img.save(os.path.splitext(filename)[0] + "_red.jpg")
    img.putdata(green)
    img.save(os.path.splitext(filename)[0] + "_green.jpg")
    img.putdata(blue)
    img.save(os.path.splitext(filename)[0] + "_blue.jpg")

def combine_bands_into_one_image(red_filename, green_filename, blue_filename, combined_filename):
    red = Image.open(red_filename)
    green = Image.open(green_filename)
    blue = Image.open(blue_filename)
    combined = Image.merge('RGB', (red.getchannel('R'), green.getchannel('G'), blue.getchannel('B')))
    combined.save(combined_filename)


def sharpen_image(filename, count):
    myImage = load_image(filename)
    for i in range( 0,count):
        sharpenedImage = myImage.filter(ImageFilter.SHARPEN)
        myImage = sharpenedImage
    return sharpenedImage



def process_bands(filename):    
    # split the image into individual bands
    myImage = load_image(filename);
    source = myImage.split()    # we get three elements in a list
    R, G, B = 0, 1, 2       # indices into source list
    # select red regions only where red is less than 100
    mask = source[R].point(lambda i: i < 100)
    # process the green band by reducing it by 70% in each pixel
    out = source[G].point(lambda i: i * 0.3)
    # paste the processed bands back
    source[G].paste(out, None, mask)
    # build a new multiband image
    im = Image.merge(myImage.mode, source)    
    im.save(os.path.splitext(filename)[0] + "_bands.jpg")

def max_filter(filename):
    image = load_image(filename)
    image2 = image.filter(ImageFilter.MaxFilter(size=5))
    image2.save(filename + "_maxFilter.jpg")
    return image2

im = Image.open("SiriusAndViolet.jpg")          # open an image file. The path is where this python file is
print(im.width, im.height, im.mode, im.format)  # Display some info about the image
im.close()

#im = Image.open("SiriusAndViolet.jpg")  
#im_c = im.crop((200,300,400,500)) # (left, top, right, bottom) it's a tuple!
#im_c.show()

im = Image.open("SiriusAndViolet.jpg") 
im_t = im.point(lambda x: 255 - x)
im_t.show()
im.close()   
   
#im_g = im.convert('L')   # convert an RGB (color image to a grayscale image   
#im_g.show();

#im.transpose(Image.FLIP_LEFT_RIGHT).show() # reflect about the vertical axis 
#im.show()

#im_thumbnail = im.copy() # copy the original image first
#im_thumbnail.thumbnail((200,200))
# paste the thumbnail on the original image 
#im.paste(im_thumbnail, (10,10))
#im.save("thumbnail.jpg")
#im.show()

img=Image.new("RGB",(640,480),(0,0,255))
img.show()
yp=0
while yp<480:
    xp=0
    while xp<640:
        img.putpixel((xp,yp),(0,255,0))
        xp+=1
    yp+=1
img.show()
   
#from PIL import ImageEnhance
#filename = "IMAG9758.jpg"
#filename = "glitters-rainbow-sky-shiny-rainbows-pastel-color-vector-24821792.jpg"
#applier = ImageEnhance.Contrast(load_image(filename))
#applier.enhance(100).show()   # Try 2 or 5
#load_image(filename).show()
   
   
#from PIL import ImageDraw
#image = Image.new("RGB", (400,500)) # It's new and it's all black
#Drawer = ImageDraw.Draw(image)
#Drawer.rectangle((50,50,75,75)) # One argument. It's a tuple.
#Drawer.rectangle((60,60,90,90), fill=None, outline="red", width=10)
#image.show()
   
#my_image = load_image("SiriusAndViolet.jpg")
#my_image.show(my_image)
    
#write_text_to_image("SiriusAndViolet.jpg", "Sirius and Violet)

#filename = "photo-1504487762795-8e9854335a0c.jpg"
#sharpened_image = sharpen_image(filename, 100)
#sharpened_image.show()
#load_image(filename).show()    
    
    
#image = max_filter("SiriusAndViolet.jpg")
#image.show()
#load_image("SiriusAndViolet.jpg").show()    
    
#filename = "SiriusAndViolet.jpg"
#sharpened_image = sharpen_image(filename, 3)
#sharpened_image.show()
#load_image(filename).show()    
    
#apply_point_transform_remove_all_but_black("SiriusAndViolet.jpg")    
 
#split_image_into_bands("SiriusAndViolet.jpg") 
#combine_bands_into_one_image("SiriusAndViolet_red.jpg",
#                             "SiriusAndViolet_green.jpg",
#                             "SiriusAndViolet_blue.jpg",
#                             "SiriusAndViolet_merged.jpg")
#process_bands("glitters-rainbow-sky-shiny-rainbows-pastel-color-vector-24821792.jpg")

#Demo02();
#create_thumbnail("catsEngaged.jpg", "catsEngagedThumbnail.jpg", 0)
#create_thumbnail_using_pillow("catsEngaged.jpg", (100,200))
#apply_point_transform_remove_all_but_black("catsEngaged.jpg")
#apply_point_transform_push_all_toward_black("catsEngaged.jpg")
#process_bands("Buggy at DQ.jpg")
#process_bands("rhino.jpg")
#process_bands("colorbands.png")

demo01()

print("Done")
