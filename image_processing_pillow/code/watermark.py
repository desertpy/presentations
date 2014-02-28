from PIL import Image


imgfile = "/home/sbraden/Desktop/imgprocdemo_files/sunflower_sm.png"
watermark = "/home/sbraden/Desktop/imgprocdemo_files/sunflower_watermark.png"

# Important thing is the 3rd argument of the paste function. 
# You can specify your PNG as alpha also so that you avoid black background.
baseim = Image.open(imgfile)
logoim = Image.open(watermark) #transparent image
baseim.paste(logoim,
            (baseim.size[0]-logoim.size[0], baseim.size[1]-logoim.size[1]),
            logoim
            )
baseim.save('new.png',"PNG")


