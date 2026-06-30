import os
import random
import colorsys
import sys

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200,200,200)

INTER_NONE = "INON"
INTER_LEFT = "ILFT"
INTER_RIGHT = "IRIG"
INTER_TOP = "ITOP"
INTER_BOTTOM = "IBOT"
    
bricksArray = []
brick_nb_cols = 1
brick_nb_rows = 1

frame_count = 1

def delete_all_files(directory_path):
    # Verify the directory exists before proceeding
    if not os.path.exists(directory_path):
        return

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_key_path = os.path.join(root, file)
            try:
                os.remove(file_key_path)
                #print(f"Deleted file: {file_key_path}")
            except Exception as e:      
                pass
                
def getColorFromHex(str1):
    str1 = str1.replace('#','')
    str1 = str1.replace('0x','')
    len1 = len(str1)
    val1 = 0; val2 = 0; val3 = 0; val4 = 255; 
    if len1 >= 2: 
        str2 = str1[0:2]
        val1 = int(str2, 16)
    if len1 >= 4: 
        str2 = str1[2:4]
        val2 = int(str2, 16)
    if len1 >= 6: 
        str2 = str1[4:6]
        val3 = int(str2, 16)
    if len1 >= 8: 
        str2 = str1[6:8]
        val4 = int(str2, 16)
    return (val1,val2,val3)

