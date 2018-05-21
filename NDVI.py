# Libraries
import rasterio
import numpy 
import cv2
import matplotlib.pyplot as plt

# Image
image_file = "C:\Users\SUKKAR\Desktop\Landsat7_for_NDVI.tif"

# Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
with rasterio.open(image_file) as src:
    band_red = src.read(3)

with rasterio.open(image_file) as src:
    band_nir = src.read(4)


# Image Statistics
nir_max = numpy.amax(band_nir) # max value in nir
nir_min = numpy.amin(band_nir) # min value in nir
red_max = numpy.amax(band_red) # max value in red
red_min = numpy.amin(band_red) # min value in red
nir_mean = numpy.mean(band_nir) # mean of nir 
red_mean = numpy.mean(band_red) # mean of red
nir_std = numpy.std(band_nir) # std of nir
red_std = numpy.std(band_red) # std of red
nir_var = numpy.var(band_nir) # var of nir
red_var = numpy.var(band_red) # var of red
nir_1D = numpy.ravel(band_nir) # to make it 1D 
red_1D = numpy.ravel(band_red) # to make it 1D 
cov = numpy.cov(nir_1D,red_1D) # cov function does not work with 2D inputs
cor = numpy.corrcoef(nir_1D,red_1D) # corrcoef function does not work with 2D inputs



# NIR vs. Red Scatter Plot
plt.plot(band_nir,band_red,'r+')
plt.xlabel('NIR',color='k',fontweight='bold')
plt.ylabel('RED',color='k',fontweight='bold')
plt.title('NIR vs RED', color='green', fontsize=14)
plt.axis([0, 256, 0, 256])
plt.text(160,5,cor)
plt.show()


# Allow division by zero
numpy.seterr(divide='ignore', invalid='ignore')

# Calculate NDVI
ndvi = ((band_nir.astype(float) - band_red.astype(float)) / (band_nir.astype(float) + band_red.astype(float))*128)+127.5

# Set spatial characteristics of the output object to mirror the input
kwargs = src.meta
kwargs.update(dtype = rasterio.uint8, count = 1)

# Create the file
with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndvi.astype(rasterio.uint8))

# Displaying NDVI    
plt.imshow(ndvi)
plt.title('Raw NDVI',color='k', fontsize=14, fontweight='bold')
plt.show()


# Histogram
plt.hist(ndvi.ravel(),256,[0,256]);
plt.title('Histogram of NDVI')
plt.show()


# Thersolding 
plt.imsave("ndvi_cmap.png", ndvi, cmap=plt.cm.gray)
img = cv2.imread('C:\\Users\\SUKKAR\\Desktop\\ndvi_cmap.png')
ret,thresh = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
# Option for thresholding: cv.THRESH_BINARY, cv.THRESH_BINARY_INV, cv.THRESH_TRUNC, cv.THRESH_TOZERO, cv.THRESH_TOZERO_INV,(https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html)
plt.imshow(thresh[:,:,0],cmap='copper')
# Option for Color Map: autumn, bone, cool, copper, flag, gray, hot, jet, pink, prism, spring, summer, winter
plt.title('NDVI Thersolding', color='k',fontsize=14, fontweight='bold')
plt.colorbar()
plt.show()
