from flask import redirect, render_template, request, send_from_directory, flash, url_for
from app.main.forms import PointSjoinForm
from app.main import bp
from app.scripts.geospatial import sjoin_df, sjoin_point
from app.scripts.fileload import allowed_file
import pandas as pd
import os
from app import SHAPE_FILE, UPLOAD_FOLDER
import sys
from flask_login import login_required, current_user
from app.models import add_transaction, Transaction

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
@login_required
def api():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        #print(uploaded_file.filename, file=sys.stderr)
        if allowed_file(uploaded_file.filename):
            
            #Save uploaded file, read into Pandas DataFrame and check for errors
            save_path = os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), uploaded_file.filename)
            uploaded_file.save(save_path)
            df = pd.read_csv(save_path)
            cost = len(df)

            if cost > current_user.compute_credits:
                add_transaction(current_user.id, 0, f"Not enough compute credits ({ current_user.compute_credits}). Cost: {cost}")
            
            elif "latitude" not in df.columns or "latitude" not in df.columns:
                add_transaction(current_user.id, 0, f"latitude or longitude not in columns")
            
            else:
                #Spatial Join and limit to important columns
                df_joined = sjoin_df(df, SHAPE_FILE)
                #Limit to important output columns
                output_columns = ['GID_1', 'GID_2', 'GID_3', 'NAME_1', 'NAME_2', 'NAME_3']
                output_columns.extend(list(df.columns))
                df_joined = df_joined[output_columns]

                #Build output folder
                OUTPUT_FOLDER = os.path.join(os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), 'output'), str(current_user.id))
                if str(current_user.id) not in os.listdir(os.path.join(os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), 'output'))):
                    os.mkdir(os.path.join(os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), 'output'), str(current_user.id)))
                
                output_file = f"{uploaded_file.filename.split()[0]}-joined.csv"
                if output_file in os.listdir(OUTPUT_FOLDER):
                    output_file = output_file.split('.')[0]+'(1)'+'.csv'
                
                df_joined.to_csv(os.path.join(OUTPUT_FOLDER, output_file), index=False)

                #Send into browser for download
                download_link = url_for('main.download_file', file=output_file)

                add_transaction(current_user.id, cost, download_link)
                
        
        else:
            add_transaction(current_user.id, 0, f"File format not supported")

    #Get all transactions associated with current user
    transactions = Transaction.query.filter_by(user=current_user.id).all()
    transactions.reverse()

    return render_template('main/api.html', transactions=transactions)

@bp.route('/download/<file>', methods=['GET'])
@login_required
def download_file(file):
    OUTPUT_FOLDER = os.path.join(os.path.join(os.path.join(os.getcwd(), UPLOAD_FOLDER), 'output'), str(current_user.id))   
    return send_from_directory(OUTPUT_FOLDER, file)
