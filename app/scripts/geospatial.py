import numpy as np
import pandas as pd
import geopandas as gpd

def sjoin_df(df, shapes, join_method='right'):

    for col in shapes.columns:
        if col in df.columns:
            df.rename(columns={col:f"{col}_old"}, inplace=True)

    #Limit to important output columns and rename if existing in df
    output_columns = ['GID_1', 'GID_2', 'GID_3', 'NAME_1', 'NAME_2', 'NAME_3']
    output_columns.extend(list(df.columns))


    #convert to GeoDataFrame and add CRS 4326
    df = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
    df.set_crs(epsg=4326, inplace=True)
    
    df_joined = gpd.sjoin(shapes, df, how=join_method)
    return df_joined[output_columns]

def sjoin_point(lat, lon, shapes):
    lat, lon = float(lat), float(lon)
    df = pd.DataFrame(data = [[lat, lon]], columns=['latitude', 'longitude'])
    
    df_joined = sjoin_df(df, shapes, join_method='inner')
    
    return df_joined