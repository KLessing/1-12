from PIL import Image
import os

def add_img(sprite: Image, img: Image, col: int):
    w = sprite.size[0] + img.size[0]
    h = 240 * col
    im = Image.new("RGBA", (w, h))
  
    im.paste(sprite)
    im.paste(img, (sprite.size[0], 0))

    return im

for i in range(1, 7):
    dir = os.getcwd() + "\\images\\" + str(i)
    files = os.listdir(dir)

    # start with first img
    sprite_sheet = Image.open(dir + "\\" + files[0])

    for i in range(1, len(files)):
        file = dir + "\\" + files[i]
        img = Image.open(file)
        sprite_sheet = add_img(sprite_sheet, img, 1)

sprite_sheet.save("sprite_sheet.png")
