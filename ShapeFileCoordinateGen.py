import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import os
import zipfile
import main


# 1. Load the image

image_name =   main.image_name
AreaName = image_name.split('.')[0]  # Extract the name without extension

if not image_name:
    input("Enter the image name (with extension): ")
image_path = '/home/cesccgasso/Python-Projects/Tools/ShapeFile Identifer/Images/' + image_name
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image '{image_name}' not found at '/home/cesccgasso/Python-Projects/Tools/ShapeFile Identifer/Images/'\n\nPlease maker sure the image is in the folder /Images/")
    exit()
height, width, _ = image.shape

# 2. Define the geographic extent of the image (top-left and bottom-right)
# Replace these with your known map bounds:

top_left_lat, top_left_lon = main.top_left_lat, main.top_left_lon
bottom_right_lat, bottom_right_lon = main.bottom_right_lat, main.bottom_right_lon
if not top_left_lat or not top_left_lon or not bottom_right_lat or not bottom_right_lon:
    input("Enter the top-left latitude and longitude (lat, lon): ")
    top_left_lat, top_left_lon = map(float, input("Top-left (lat, lon): ").split(','))
    input("Enter the bottom-right latitude and longitude (lat, lon): ")
    bottom_right_lat, bottom_right_lon = map(float, input("Bottom-right (lat, lon): ").split(','))
    exit()

# Functions to convert pixel (x, y) to lat/lon:
def pixel_to_coords(x, y):
    lon = top_left_lon + (x / width) * (bottom_right_lon - top_left_lon)
    lat = top_left_lat - (y / height) * (top_left_lat - bottom_right_lat)
    return lon, lat

# 3. Convert image to HSV and create mask for dark blue
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_blue = np.array(main.lower_blue)
upper_blue = np.array(main.upper_blue)
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 4. Clean mask
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# 5. Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 6. Create geographic polygons
polygons = []
for contour in contours:
    if cv2.contourArea(contour) > 100:  # Remove small shapes
        coords = []
        for point in contour:
            x, y = point[0]
            lon, lat = pixel_to_coords(x, y)
            coords.append((lon, lat))
        polygons.append(Polygon(coords))

# 7. Create GeoDataFrame in EPSG:4326 (WGS84)
gdf = gpd.GeoDataFrame({'id': list(range(1, len(polygons)+1)), 'geometry': polygons}, crs="EPSG:4326")

# 8. Fix shapefile
polygons = []
names = []

for i, geom in enumerate(gdf['geometry']):
    if geom and geom.is_valid:
        simple_geom = geom.simplify(0.0001, preserve_topology=True)
        polygons.append(simple_geom)
        names.append(f'Shape_{i+1}')

# 9. Create new GeoDataFrame in EPSG:4326 (WGS84)
gdf = gpd.GeoDataFrame({'Name': names, 'geometry': polygons}, crs="EPSG:4326")

# 10. Save shapefile
output_folder = AreaName + '_shapefile_geo'
os.makedirs(output_folder, exist_ok=True)
shapefile_path = os.path.join(output_folder, AreaName + '_extracted_shapes.shp')
gdf.to_file(shapefile_path)

# 11. Zip files
with zipfile.ZipFile(AreaName + '_extracted_shapes_geo.zip', 'w') as zipf:
    for ext in ['.shp', '.shx', '.dbf', '.cpg', '.prj']:
        zipf.write(os.path.join(output_folder, AreaName + '_extracted_shapes' + ext), arcname= AreaName + '_extracted_shapes' + ext)

print("✅ Shapefile with geographic coordinates created successfully!")