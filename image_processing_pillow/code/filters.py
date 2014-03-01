#temp.py
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageFilter

radius=10
im = Image.open("ex_noise.jpg")
out1 = im.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
out2 = im.filter(ImageFilter.UnsharpMask(radius=20, percent=150, threshold=3))
out3 = im.filter(ImageFilter.UnsharpMask(radius=40, percent=150, threshold=3))

#out1 = im.filter(ImageFilter.GaussianBlur(radius=20))
#out2 = im.filter(ImageFilter.GaussianBlur(radius=40))
#out = im.filter(ImageFilter.BLUR)
#im.show(out)

# The subplot() command specifies numrows, numcols, fignum 
# where fignum ranges from 1 to numrows*numcols.

plt.subplot(221), plt.imshow(im)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222), plt.imshow(out1)
plt.title('UnsharpMask radius=2'), plt.xticks([]), plt.yticks([])
plt.subplot(223), plt.imshow(out2)
plt.title('UnsharpMask radius=20'), plt.xticks([]), plt.yticks([])
plt.subplot(224), plt.imshow(out3)
plt.title('UnsharpMask radius=40'), plt.xticks([]), plt.yticks([])
plt.show()


 