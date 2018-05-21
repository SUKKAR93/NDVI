# Libraries
from Tkinter import *
import tkMessageBox
import tkFileDialog

import rasterio
import numpy 
import cv2
import matplotlib.pyplot as plt




def browse_file():
    global fname
    fname = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.type"), ("All files", "*")))
    filename1.insert(0, fname)
    
    
    return fname
    
def thresholding_method():
    x=ThresholdStatus.get()
    if x == 1 :
        thm=cv2.THRESH_BINARY
        print(x)
    elif x == 2 :
        thm=cv2.THRESH_BINARY_INV
    elif x == 3 :
        thm=cv2.THRESH_TRUNC
    elif x == 4 :
        thm=cv2.THRESH_TOZERO
    elif x == 5 :
        thm=cv2.THRESH_TOZERO_INV
    else:
        tkMessageBox.showinfo("ERROR!","YOU HAVE TO SELECT A METHOD")
    return thm
def pseudo_method () :
    x=PseudoColorStatus.get()
    if x == 1 :
        pcm='autumn'
        print(x)
    elif x == 2 :
        pcm='cool'
    elif x == 3 :
        pcm='gray'
    elif x == 4 :
        pcm='hot'
    elif x == 5 :
        pcm='pink'
    elif x == 6 :
        pcm='winter'    
    else:
        tkMessageBox.showinfo("ERROR!","YOU HAVE TO SELECT A METHOD")
    return pcm   
def Run ():
    
# Image
    image_file = fname

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
    plt.hist(ndvi.ravel(),256,[0,255]);
    plt.title('Histogram of NDVI')
    plt.show()


# Thersolding
    thm = thresholding_method()
    pcm = pseudo_method ()
    plt.imsave("ndvi_cmap.png", ndvi, cmap=plt.cm.gray)
    img = cv2.imread('C:\\Users\\technic\\Desktop\\ndvi_cmap.png')
    ret,thresh = cv2.threshold(img,120,255,thm)
# Option for thresholding: cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV,(https://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html)
    plt.imshow(thresh[:,:,0],cmap=pcm)
# Option for Color Map: autumn, bone, cool, copper, flag, gray, hot, jet, pink, prism, spring, summer, winter
    plt.title('NDVI Thersolding', color='k',fontsize=14, fontweight='bold')
    plt.colorbar()
    plt.show()
    
def main():
    Run(browse_file())
   
app = Tk()
app.title("NDVI")
app.geometry('450x560')

labeltext = StringVar()
labeltext.set("SELECT YOUR TIFF FILE")
label1=Label(app,textvariable=labeltext, height = 4)
label1.pack()

filename = StringVar(None)
filename1 = Entry(app ,textvariable = filename,width =60)
filename1.pack()

button1 = Button(app ,text="Browse", width=20,command=browse_file)
button1.pack(side='top',padx=2,pady=2)

labeltext2 = StringVar()
labeltext2.set("SELECT YOUR THRESHOLDING METHOD")
label2=Label(app,textvariable=labeltext2, height = 4)
label2.pack()

ThresholdStatus = IntVar()
ThresholdStatus.set(None)
radio1=Radiobutton(app ,text ="Threshold Binary", value =1,variable=ThresholdStatus,command =thresholding_method).pack()
radio2=Radiobutton(app ,text ="Threshold Binary,Inverted", value =2,variable=ThresholdStatus,command =thresholding_method).pack()
radio3=Radiobutton(app ,text ="Truncate", value =3,variable=ThresholdStatus,command =thresholding_method).pack()
radio4=Radiobutton(app ,text ="Threshold to Zero", value =4,variable=ThresholdStatus,command =thresholding_method).pack()
radio5=Radiobutton(app ,text ="Threshold to Zero, Inverted", value =5,variable=ThresholdStatus,command =thresholding_method).pack()

labeltext3 = StringVar()
labeltext3.set("SELECT YOUR PSEUDO COLORING METHOD")
label3=Label(app,textvariable=labeltext3, height = 4)
label3.pack()


PseudoColorStatus = IntVar()
PseudoColorStatus.set(None)
radio6=Radiobutton(app ,text ="AUTUMN", value =1,variable=PseudoColorStatus,command =pseudo_method).pack()
radio7=Radiobutton(app ,text ="COOL", value =2,variable=PseudoColorStatus,command =pseudo_method).pack()
radio8=Radiobutton(app ,text ="GRAY", value =3,variable=PseudoColorStatus,command =pseudo_method).pack()
radio9=Radiobutton(app ,text ="HOT", value =4,variable=PseudoColorStatus,command =pseudo_method).pack()
radio10=Radiobutton(app ,text ="PINK", value =5,variable=PseudoColorStatus,command =pseudo_method).pack()
radio11=Radiobutton(app ,text ="WINTER", value =6,variable=PseudoColorStatus,command =pseudo_method).pack()

button2 = Button(app ,text="Run", width=20,command=Run)
button2.pack(side='bottom',padx=2,pady=2)


app.mainloop()
 



print "hollo"
