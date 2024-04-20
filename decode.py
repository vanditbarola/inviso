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


# Decode the image
def decode(image):    
    arr = np.array(image)
    red = arr[..., 0]  # All Red values
    green = arr[..., 1]  # All Green values
    blue = arr[..., 2]  # All Blue values

    height,width = blue.shape
    total_size = height*width
    data = []
    bit_size = 0
    data_byte = ''

    if count < total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if bit_size < 8:
                        data_byte = data_byte + str((blue[i][j] & 1))
                        bit_size+=1
                    else:
                        data.append(data_byte)                        
                        bit_size = 0
                        data_byte = '' 

                        data_byte = data_byte + str((blue[i][j] & 1))
                        bit_size+=1
                        
                    new_count+=1
                else:
                    break

    elif count > total_size and count < 2*total_size:
        new_count = 0
        for i in range(height):
            for j in range(width):                                    
                if bit_size < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size+=1
                else:
                    data.append(data_byte)                        
                    bit_size = 0
                    data_byte = '' 

                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size+=1
        bit_size = 0
        data_byte = ''                                                        
                
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if bit_size < 8:
                        data_byte = data_byte + str((green[i][j] & 1))
                        bit_size+=1
                    else:
                        data.append(data_byte)                        
                        bit_size = 0
                        data_byte = '' 

                        data_byte = data_byte + str((green[i][j] & 1))
                        bit_size+=1
                        
                    new_count+=1
                else:
                    break
    else: 
        new_count = 0
        for i in range(height):
            for j in range(width):                                    
                if bit_size < 8:
                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size+=1
                else:
                    data.append(data_byte)                        
                    bit_size = 0
                    data_byte = '' 

                    data_byte = data_byte + str((blue[i][j] & 1))
                    bit_size+=1
        bit_size = 0
        data_byte = ''

        for i in range(height):
            for j in range(width):                                    
                if bit_size < 8:
                    data_byte = data_byte + str((green[i][j] & 1))
                    bit_size+=1
                else:
                    data.append(data_byte)                        
                    bit_size = 0
                    data_byte = '' 

                    data_byte = data_byte + str((green[i][j] & 1))
                    bit_size+=1
        bit_size = 0
        data_byte = ''                                                        
                
        for i in range(height):
            for j in range(width):
                if new_count <= count:                    
                    if bit_size < 8:
                        data_byte = data_byte + str((red[i][j] & 1))
                        bit_size+=1
                    else:
                        data.append(data_byte)                        
                        bit_size = 0
                        data_byte = '' 

                        data_byte = data_byte + str((red[i][j] & 1))
                        bit_size+=1
                        
                    new_count+=1
                else:
                    break    
    return data


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
