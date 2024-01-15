from PIL import Image
import os

def add_img(sprite: Image, img: Image, y: int, x: int):
    w = 240 * x
    h = 240 * (y - 1)
    im = Image.new("RGBA", (240 * 16, 240 * 6)) # Full Resolution
  
    im.paste(sprite)
    im.paste(img, (w, h))

    return im

sprite_sheet = Image.new("RGBA", (0, 0))

for i in range(1, 7):
    dir = os.getcwd() + "\\images\\" + str(i)
    files = os.listdir(dir)

    for j in range(len(files)):
        file = dir + "\\" + files[j]
        img = Image.open(file)
        sprite_sheet = add_img(sprite_sheet, img, i, j)

sprite_sheet.save("sprite_sheet.png")
