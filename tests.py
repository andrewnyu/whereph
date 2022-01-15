#!venv/bin/python
import unittest
from app import create_app, db
from config import Config

import numpy as np
import pandas as pd
from app.scripts.geospatial import sjoin_point, sjoin_df
import os

class SpatialJoinCase(unittest.TestCase):

    def setUp(self):
        #load shape file
        SHAPES_PATH = '~/prog/where-ph/app/static/shapefile'
        PKL_SHAPE_FILE = os.path.join(SHAPES_PATH, 'ph-shape.pkl')
        SHAPE_FILE = pd.read_pickle(PKL_SHAPE_FILE)
        self.shapes = SHAPE_FILE

    def testSpatialJoinPoint(self):
        df_joined = sjoin_point(10.541173972241738, 122.83989386089448, self.shapes)
        result = df_joined[['NAME_1', 'NAME_2', 'NAME_3']].iloc[0].values
        self.assertTrue((result[0]=='Negros Occidental'))

    def testSpatialJoinFile(self):
        sample_df = pd.DataFrame(data = zip([1,2,3], [10.541173972241738, 14.54136684853697, 8.041173972241738], 
                     [122.83989386089448, 121.03749818490371, 123.0374981840371]), 
             columns=['id', 'latitude', 'longitude'])
        
        joined = sjoin_df(sample_df, self.shapes)
        self.assertTrue(isinstance(joined, pd.DataFrame))


if __name__ == '__main__':
    unittest.main()


