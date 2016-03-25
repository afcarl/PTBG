__author__ = 'luocheng'

from selenium import webdriver
from PIL import Image
im = Image.open('../data/screenshots/75.png')
width, height = im.size
print width,height
