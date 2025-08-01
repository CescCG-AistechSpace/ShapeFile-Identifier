import subprocess
import sys

### USER! Insert the following data to have your shapefile generated:
# 1. Insert the Image Name for which you want to generate the shapefile
# 2. Insert the top-left and bottom-right coordinates of the image in latitude and longitude
# ...Check the result... if there is too much or too little of the area identified:
# (3. OPTIONAL Adjust the Blue Color Range for the mask if needed)

# 1. Image to generate shapefile for
image_name = 'BarcelonaAOI.png'  

# 2. Top-left coordinates & Bottom-right coordinates
top_left_lat, top_left_lon = 41.529766, 1.763930  
bottom_right_lat, bottom_right_lon = 41.244830, 2.615664

# (3. OPTIONAL ONLY MODIFY TO ADJUST THE COLOR OF THE POLYGON SELECTED - Blue Color Range for the mask)
lower_blue = [99, 130, 220]
upper_blue = [130, 255, 255]

def main():

    subprocess.run([sys.executable, "ShapeFileCoordinateGen.py"])

if __name__ == "__main__":
    main()

def getMainData():
    return {
        "image_name": image_name,
        "top_left_lat": top_left_lat,
        "top_left_lon": top_left_lon,
        "bottom_right_lat": bottom_right_lat,
        "bottom_right_lon": bottom_right_lon,
        "lower_blue": lower_blue,
        "upper_blue": upper_blue
    }
