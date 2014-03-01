# fast fourier transform demo

import cv2
import numpy as np
from matplotlib import pyplot as plt


# zero freqency will be in the corners
# to bring zero frequency to the center, shift the result by N/2 
# in both the directions: use the function np.fft.fftshift()


def cv_fft(img):

    """
    OpenCV provides the functions cv2.dft() and cv2.idft()
    It returns the same result as numpy, but with two channels. 
    First channel will have the real part of the result and 
    second channel will have the imaginary part of the result. 
    The input image should be converted to np.float32 first.
    """

    dft = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    a = dft_shift[:,:,0]
    b = dft_shift[:,:,1]
    magnitude_spectrum = 20*np.log(cv2.magnitude(a, b))
    return magnitude_spectrum


def get_optimal_arraysize(img):
    """
    Performance of DFT calculation is better for some array sizes. 
    Fastest when array size is power of two. 
    You can modify the size of the array to any optimal size (by padding zeros) 
    before finding DFT. 
    """

    rows, cols = img.shape
    print rows, cols
    optimal_rows = cv2.getOptimalDFTSize(rows)
    optimal_cols = cv2.getOptimalDFTSize(cols)
    print optimal_rows, optimal_cols

    return optimal_rows, optimal_cols


def fft_plot(img, magnitude_spectrum): 
    
    plt.subplot(121), plt.imshow(img, cmap = 'gray')
    plt.title('High Pass Filter'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Mask'), plt.xticks([]), plt.yticks([])
    plt.show()


def np_fft(img):

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift)) 
    return magnitude_spectrum


def optimize_array(img):

    optimal_img = np.zeros((optimal_rows, optimal_cols)) # create new zero array
    optimal_img[:rows, :cols] = img # copy the data to new array

    return 


def create_mask(img):
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2

    # create a mask first, center square is 1, remaining all zeros
    mask = np.zeros((rows,cols,2),np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1 # low pass filter

    return mask


def apply_mask(mask, img):
    # apply mask and inverse DFTrum
    dft = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2
    # fshift = dft_shift*mask # for low pass filter
    dft_shift[crow-30:crow+30, ccol-30:ccol+30] = 0 #for high pass filter
    #f_ishift = np.fft.ifftshift(fshift) #fshift for low pass code
    f_ishift = np.fft.ifftshift(dft_shift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    return img_back


def main():

    img = cv2.imread('sunflower_sm.png', 0)
    optimal_rows, optimal_cols = get_optimal_arraysize(img)
    
    magnitude_spectrum = cv_fft(img)

    mask = create_mask(magnitude_spectrum) # mask[:,:,0] to display

    new_img = apply_mask(mask, img) 

    fft_plot(new_img, mask[:,:,0])

if __name__ == '__main__':
    main()
