from PIL import Image
import numpy as np
import datetime
from werkzeug.utils import secure_filename
import sys
import codecs

count = 0 

#Binary to UTF
def bin_to_utf(data):
    
    Unicode_data = ''
    for d in data:
        binary_int = int(d,2)
        byte_number = binary_int.bit_length() + 7 # 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode("utf-8", 'ignore')       
        
        Unicode_data = Unicode_data + ascii_text        

    return Unicode_data



# Encode the image
def encode(image,data):
    # iterate the image pixels
    # store user input in LSB(least significant bit) of each pixels RGB depending on need
    # start with B then G then R..
   
    arr = np.array(image)
    # print(arr.shape) ...to see size of img
    
    # 3d array....2d pixel array with 3 channels
    red = arr[..., 0]  # All Red values
    green = arr[..., 1]  # All Green values
    blue = arr[..., 2]  # All Blue values
    
    # pixels can be odd or even    
    
    height,width = blue.shape
    incompBlue = True
    incompGreen = True
    incompRed = True

    blue[0][0] = 193
    blue[0][2] = 882
    i = 0
    j = -1
    global count
    c = 0
    for char in data:
        for bit in char:  
            count += 1
            if incompBlue == True:
                if i < height:
                    if j < width:                       
                        j+=1     
                    if j >= width:
                        i+=1
                        j=0
                    # print("{0:b}".format(blue[i][j]))
                    # if bit of char is 1
                    
                    #print(i,j)
                    if i < height:
                        if bit=='1':
                            blue[i][j] = blue[i][j] | 1  #set the last bit to 1
                        elif bit=='0':
                            blue[i][j] = blue[i][j] & (blue[i][j] -1)   #set the last bit to 0
                        c += 1  
                    else:
                        incompBlue = False
                        i = 0
                        j = -1
                      
                    
                    # print("{0:b}".format(blue[i][j]))
                    # print('\n')
       
                else:
                    incompBlue = False  
                    i = 0
                    j = -1                                                              
                
            if incompBlue == False and incompGreen == True:
                if i < height:
                    if j < width:                        
                        j+=1
                    if j >= width:
                        i+=1
                        j=0   
                    # print("{0:b}".format(green[i][j]))
                    # if bit of char is 1
                    # print("g",i,j)
                    if i < height:
                        if bit=='1':
                            green[i][j] = green[i][j] | 1  #set the last bit to 1
                        elif bit=='0':
                            green[i][j] = green[i][j] & (green[i][j] -1)   #set the last bit to 0
                        c += 1
                    else:
                        incompGreen = False
                        i = 0
                        j = -1                    
                    
                    # print("{0:b}".format(green[i][j]))
                    # print('\n')    
                else:
                    incompGreen = False  
                    i = 0
                    j = -1
            if incompBlue == False and incompGreen == False:
                if i < height:
                    if j < width:                        
                        j+=1
                    if j >= width:
                        i+=1
                        j=0   
                    # print("{0:b}".format(red[i][j]))
                    # if bit of char is 1
                    # print("r",i,j)
                    if i < height:
                        if bit=='1':
                            red[i][j] = red[i][j] | 1  #set the last bit to 1
                        elif bit=='0':
                            red[i][j] = red[i][j] & (red[i][j] -1)   #set the last bit to 0
                        c += 1
                    else:
                        incompRed = False  
                        sys.exit("Choose a higher quality image")                     

                    # print("{0:b}".format(red[i][j]))
                    # print('\n')    
                else:
                    incompRed = False  
                    i = 0
                    j = -1
                    break
                  
    if incompRed == False:
        sys.exit("Choose a higher quality image")        

    w, h = image.size
    test = np.zeros((h, w, 3), dtype=np.uint8)
    
    #reconstructing image
    test[:,:,0] = red
    test[:,:,1] = green
    test[:,:,2] = blue

    # current time and filename
    ct = datetime.datetime.now()
    filename = secure_filename('2'+str(ct) +'.jpg')
    
    # saving image
    img = Image.fromarray(test, 'RGB')    
    img.save(filename)
    # img.show()    
    return [img,filename]

# Convert user input to 8 bit binary using Unicode value of characters
def generate_binary(data):
    # converted data
    new_data = []

    for i in data:
        # converting every character of user input to its binary
        new_data.append(format(ord(i), '08b'))

    # ord returns the unicode of string(of unit length only..so a character basically)
    # character to Unicode to binary
    # unicode preferred over Ascii as superset of ascii and characters of other languages also available
    
    return new_data

# Load image
def load_img():
    resource_name = "1.jpg"
    image = Image.open(resource_name,'r')
    return image

