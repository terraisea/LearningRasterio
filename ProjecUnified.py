from rasterio import open
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

with open("./database/zhangzhongjing1.tif") as dataset:
    width = dataset.width
    height = dataset.height

# 读取空格分隔的 TXT 文件
data = np.loadtxt("database/zhangzhongjing1020.txt")  # 默认按空格分割
rows = len(data)

for i in range(rows):
    x_center = data[i,1]
    y_center = data[i,2]
    box_width = data[i,3]
    box_height = data[i,4]

    x_center_coords = width*x_center
    y_center_coords = height*y_center

    width_coords=box_width*width/2
    height_coords=box_height*height/2

    X_LT=x_center_coords-width_coords
    Y_LT=y_center_coords-height_coords
    X_LB=x_center_coords+width_coords
    Y_LB=y_center_coords-height_coords
    X_RT = x_center_coords - width_coords
    Y_RT = y_center_coords + height_coords
    X_RB=x_center_coords+width_coords
    Y_RB=y_center_coords+height_coords


    xlt, ylt = dataset.transform * (X_LT, Y_LT)
    xlb, ylb = dataset.transform * (X_LB, Y_LB)
    xrt, yrt = dataset.transform * (X_RT, Y_RT)
    xrb, yrb = dataset.transform * (X_RB, Y_RB)

 #如果要导入arcmap需要360-x轴

    poly_coords = [(xlt,ylt), (xlb, ylb), (xrb, yrb),(xrt, yrt), (xlt,ylt)]#注意闭合

    polygon = Polygon(poly_coords)

    # Moon 2000 GEOGCS WKT
    moon2000_wkt = 'GEOGCS["GCS_Moon_2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400,0]],PRIMEM["Reference_Meridian",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST]]'

    gdf_poly = gpd.GeoDataFrame({'name': ['Region1'], 'geometry': [polygon]}, crs=moon2000_wkt)

    # 获取第一列的值作为文件名
    filename = str(data[i][1])

    # 构造完整路径
    filepath = f"./database/UnifiedProject/{filename}.shp"

    gdf_poly.to_file(filepath, driver="ESRI Shapefile")

    print(f"Saved {filename}")