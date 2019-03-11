# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735
import time


# Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port=0,
    cs=0,
    dc=9,
    backlight=18,
    rotation=90,
    spi_speed_hz=4000000
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
# Get a PIL Draw object to start drawing on the display buffer.
imgbg = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
# Get a PIL Draw object to start drawing on the display buffer.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

# Draw a red rectangle with yellow outline.
draw.rectangle((WIDTH-10, 10, WIDTH, HEIGHT-10), outline=(255,0,0), fill=(255,0,0))

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 16)

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)

# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
draw_rotated_text(img, 'WARNING', (0, 20), 270, font, fill=(0,0,0))
#draw_rotated_text(img, 'This is a line of text.', (10, HEIGHT-10), 0, font, fill=(255,255,255))

# Write buffer to display hardware, must be called to make things visible on the
# display!

for x in range(5):
  # Clear to black
  disp.display(imgbg)
  
  time.sleep(0.5)
  
  # Display message
  disp.display(img)
  
  time.sleep(0.10)

imgSolar = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

drawSolar = ImageDraw.Draw(imgSolar)

drawSolar.rectangle((WIDTH, 10, WIDTH-16, HEIGHT-10), outline=(0,0,0), fill=(255,255,0))

disp.display(imgSolar)

offset=WIDTH

time.sleep(0.5)

drawSolar.rectangle((offset, 10, offset-4, HEIGHT-10), outline=(255,255,0), fill=(255,255,0))
offset -= 14

time.sleep(0.5)


for x in range(1, 11):
  drawSolar.rectangle((offset, 10, offset-4, HEIGHT-10), outline=(255,255,0), fill=(255,255,0))
  offset -= 14
  disp.display(imgSolar)
  time.sleep(0.025)

