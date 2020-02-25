'''
Created on Feb 25, 2020

@author: nicomp
'''
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os, sys
import requests
from io import BytesIO


def load_image( filename ) :
    '''
    Load an image file from disk
    :param filename: The file to load
    :return the image object
    '''
    try:
        myimage = Image.open(filename)
        myimage.load()
        return myimage
    except:
        print("load_image(): cannot open " + filename)
        return None