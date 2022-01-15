import numpy as np
import pandas as pd
import geopandas as gpd

def sjoin_df(df, shapes, join_method='right'):
    #convert to GeoDataFrame and add CRS 4326
    df = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
    df.set_crs(epsg=4326, inplace=True)
    
    df_joined = gpd.sjoin(shapes, df, how=join_method)
    return df_joined

def sjoin_point(lat, lon, shapes):
    lat, lon = float(lat), float(lon)
    df = pd.DataFrame(data = [[lat, lon]], columns=['latitude', 'longitude'])
    
    df_joined = sjoin_df(df, shapes)
    
    return df_joined