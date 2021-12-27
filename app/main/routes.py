from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from app import db
from app.main.forms import PointSjoinForm
from app.main import bp
from app.scripts.whereph import sjoin_point
from sqlalchemy import func
import geopandas as gpd
import sys
import datetime

@bp.route('/', methods={'GET','POST'})
@bp.route('/index', methods={'GET','POST'})
def index():
    
    form = PointSjoinForm()

    if form.validate_on_submit():

        #SHAPE_FILE = url_for('static', filename='shapefile/gadm36_PHL_shp/gadm36_PHL_3.shp')
        SHAPE_FILE = '~/prog/where-ph/app/static/shapefile/gadm36_PHL_shp/gadm36_PHL_3.shp'
        shapes = gpd.read_file(SHAPE_FILE)

        #Run Sjoin Code
        df_joined = sjoin_point(form.latitude.data, form.longitude.data, shapes)
        #print(df_joined, file=sys.stderr)

        #Area not found
        if(len(df_joined)==0):
            return render_template('main/not-found.html')
        else:
            #Return Areas (Barangay, City, Province)
            result = df_joined[['NAME_1', 'NAME_2', 'NAME_3']].iloc[0].values
            #print(result, file=sys.stderr)
            return render_template('main/success.html', result=result)

    return render_template('main/index.html', form=form)