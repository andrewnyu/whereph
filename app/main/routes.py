from flask import render_template, request, send_from_directory
from app.main.forms import PointSjoinForm
from app.main import bp
from app.scripts.geospatial import sjoin_df, sjoin_point
from app.scripts.fileload import allowed_file
import pandas as pd
import os
from app import SHAPE_FILE, UPLOAD_FOLDER
import sys

@bp.route('/', methods={'GET','POST'})
@bp.route('/index', methods={'GET','POST'})
def index():
    
    form = PointSjoinForm()

    if form.validate_on_submit():

        shapes = SHAPE_FILE
        df_joined = sjoin_point(form.latitude.data, form.longitude.data, shapes) 
        #print(df_joined, file=sys.stderr)

        #Area not found
        if len(df_joined)==0:
            return render_template('main/not-found.html')
        else:
            #Return Areas (Barangay, City, Province)
            result = df_joined[['NAME_1', 'NAME_2', 'NAME_3']].iloc[0].values
            #print(result, file=sys.stderr)
            return render_template('main/success.html', result=result)

    return render_template('main/index.html', form=form)

@bp.route('/api', methods=['GET', 'POST'])
def api():

    if request.method == 'POST':
        uploaded_file = request.files['file']
        print(uploaded_file.filename, file=sys.stderr)
        if allowed_file(uploaded_file.filename):
            
            #Save uploaded file, read into Pandas DataFrame and check for errors
            save_path = os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), uploaded_file.filename)
            uploaded_file.save(save_path)
            df = pd.read_csv(save_path)
            assert ('latitude' in df.columns) and ('longitude' in df.columns)

            #Spatial Join and export into file
            df_joined = sjoin_df(df, SHAPE_FILE)

            #Limit to important output columns
            output_columns = ['NAME_1', 'NAME_2', 'NAME_3']
            output_columns.extend(list(df.columns))

            df_joined = df_joined[output_columns]
            output_path = os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), 'output')
            df_joined.to_csv(os.path.join(output_path, 'joined.csv'), index=False)

            #Send into browser for download
            return send_from_directory(output_path, 'joined.csv')

    
    return render_template('main/api.html')