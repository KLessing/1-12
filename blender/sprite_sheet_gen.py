from PIL import Image
import os

ROW_COUNT = 6
COL_COUNT = 16

def add_img(sprite: Image, img: Image, y: int, x: int):
    w = img.size[0] * x
    h = img.size[1] * y

    # Full Resolution
    res = Image.new("RGBA", (img.size[0] * COL_COUNT, img.size[1] * ROW_COUNT))
  
    res.paste(sprite)
    res.paste(img, (w, h))

    return res

# init empty sprite sheet img
sprite_sheet = Image.new("RGBA", (0, 0))

for i in range(ROW_COUNT):
    dir = os.getcwd() + "\\images\\" + str(i + 1)
    files = os.listdir(dir)

    for j in range(len(files)):
        file = dir + "\\" + files[j]
        img = Image.open(file)
        sprite_sheet = add_img(sprite_sheet, img, i, j)

sprite_sheet.save("sprite_sheet.png")
