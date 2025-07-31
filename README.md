ShapeFile Identifier Tool
========================

Developped by Cesc Casanovas for Aistech Space  
cesc.casanovas@aistechspace.com

Description
------------
This tool generates shapefiles from images by identifying colored areas (default: blue). It converts pixel coordinates to geographic coordinates using provided bounds.

Prerequisites
------------
- Python 3.x
- Required packages:
  ```
  pip install opencv-python numpy geopandas shapely
  ```

Usage
-----
1. Place your image in the same directory as main.py, under the "Images" folder.
2. Open main.py and set these parameters:

   a. Image name:
      image_name = 'YourImage.png'

   b. Geographic bounds:
      top_left_lat = latitude value
      top_left_lon = longitude value
      bottom_right_lat = latitude value
      bottom_right_lon = longitude value

   c. Optional: Adjust color detection (default is blue):
      lower_blue = [110, 60, 60]   # HSV values
      upper_blue = [140, 255, 255] # HSV values

3. Run the tool:
   ```
   python3 main.py
   ```
4. Review your shapefile, adjust the parameters and rerun  
    - You can use [ShapeFile Viewer](https://www.chatdb.ai/tools/shapefile-viewer) to review your ShapeFile. It should appear like this:
   

Output
------
- Creates a folder named '{YourImage}_shapefile_geo'
- Generates shapefile components inside of the folder (.shp, .shx, .dbf, .cpg, .prj)
- Creates a zip file containing all shapefile components

Troubleshooting
--------------
1. "No module named 'cv2'":
   Run: pip install opencv-python

2. No shapes detected:
   - Verify image contains blue areas
   - Adjust color range values if needed
   - Confirm image exists in correct directory

3. Incorrect geographic placement:
   - Double-check coordinate values
   - Ensure coordinates are in correct order (lat, lon)

Notes
-----
- Images should have blue areas to be detected. If not, change the HSV color values to adapt to your color. 
- You can easily find the HSV value of your area by pasting the image in Paint, using the color picker, then pressing on the color selected and toggling HSV instead of RGB. 
- Coordinates must be in WGS84 format (EPSG:4326)
- Tool removes shapes smaller than 100 pixels to reduce noise
- Output is in standard GIS shapefile format

For support or bug reports, please create an issue in the repository. 
