from flask import render_template, flash, redirect, url_for, request, g, current_app
from app import db
from app.main.forms import PointSjoinForm
from app.main import bp
from app.scripts.whereph import sjoin_point
from sqlalchemy import func
import geopandas as gpd
import pandas as pd
import os
from app import SHAPE_FILE

@bp.route('/', methods={'GET','POST'})
@bp.route('/index', methods={'GET','POST'})
def index():
    
    form = PointSjoinForm()

    if form.validate_on_submit():

        shapes = SHAPE_FILE
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