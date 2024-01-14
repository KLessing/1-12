from PIL import Image
import os
import array

dir = os.getcwd()

file_path1 = dir + "\\images\\1\\0001.png"
file_path2 = dir + "\\images\\1\\0011.png"

im1 = Image.open(file_path1)
im2 = Image.open(file_path2)

def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

sprite_sheet = merge(im1, im2)
sprite_sheet.save("sprite_sheet.png")
