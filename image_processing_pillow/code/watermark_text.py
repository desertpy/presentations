from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


imgfile = "/home/sbraden/Desktop/imgprocdemo_files/sunflower_sm.png"
font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", 40)

im = Image.open(imgfile)
imageW = im.size[0]
imageH = im.size[1]  

draw = ImageDraw.Draw(im)

wh = font.getsize("DesertPy")

draw.text((im.size[0]/2 - wh[0]/2, im.size[1]/2 + 30),
            "DesertPy", 
            fill=(255, 255, 255), 
            font=font
            )
draw.text((im.size[0]/2 - wh[0]/2, im.size[1]/2 - 90),
             "Gangplank", 
             fill=(255, 255, 255), 
             font=font
             ) 

im.show()

