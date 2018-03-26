from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from sklearn.externals import joblib
import pandas as pd
import geocoder
from key import key_s
import googlemaps
import ast
import numpy as np

#global dictionary to preserve values
dictionary={}

app = Flask(__name__)

app.secret_key = "thisisasecretshhhh"

#Main page that handles a GET request from POSTed prediction data
@app.route('/',  methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        try:
            all_args = request.args.to_dict()
            return render_template('main.html', dicti= ast.literal_eval(all_args['dicti']))
        except Exception as e:
            pass

    return render_template('main.html', dicti=dictionary)

#This page exists to handle prediction data and results, but was mainly used to
#implement POST, Redirect, GET in single view application
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    error=None #Error log

    svm = joblib.load('dispatch_classifier.pkl') #deserializes LinearSVC model trained on dispatch data

    #Handles form data:
    if request.method == 'POST':
        location_input = request.form['location_input']
        time_input = request.form['time_input']

        #Checks input types for coordinates or address
        if len(location_input.split(' ')) > 2:  #handles address data
            try:
                gm = googlemaps.Client(key=key_s)   #utilizes googlemaps API to convert user entered address into coordinates
                geocode_result = gm.geocode(location_input)
                lat = geocode_result[0]['geometry']['location']['lat'] #extracting information from JSON data
                lon = geocode_result[0]['geometry']['location']['lng']
            except Exception as e:
                flash("Something went wrong! Check the format of the address and try to provide as much information as possible. If entering coordinates, make sure each coordinate is separated by a comma and a space.")

        elif len(location_input.split(' ')) > 0:     #handles coordinate data
            try:
                loc_arr = location_input.split(', ')
                lat = loc_arr[0]
                lon = loc_arr[1]

            except IndexError as e:
                flash("Something went wrong! Check the format of the address and try to provide as much information as possible. If entering coordinates, make sure each coordinate is separated by a comma and a space.")


        try:
            (h, m, s) = time_input.split(':')       #processing time input, calculating number of seconds since 00:00:00
            if (int(h) > 23) or (int(m) > 59) or (int(float(s)) > 59): #checks for valid input (23:59:59 max time)
                raise Exception('Invalid time entered')
            time = int(h) * 3600 + int(m) * 60 + int(float(s))
        except Exception as e:
            flash("Something went wrong! Make sure the time is entered as a 24 hour time in the format hh:mm:ss.")


        try: #populates a dataframe with input data
            df = pd.DataFrame()
            df['Latitude'] = [lat]
            df['Longitude'] = [lon]
            df['timestamp'] = [time]
            print(svm.predict_proba(df))
            dictionary = dict(zip(svm.classes_, svm.predict_proba(df)[0])) #zips predictino probabilites with labels
            dictionary_key = sorted(dictionary, key=dictionary.get)[::-1]
            dictionary_val = sorted(dictionary.values())[::-1]
            dictionary = dict(zip(dictionary_key, dictionary_val))  #sorts values based on prediction strength.
            return redirect(url_for('main', dicti=dictionary))

        except Exception as e:
            pass

    return redirect(url_for('main'))

#renders geo heat-map
@app.route('/map',  methods=['GET', 'POST'])
def map():
    return render_template('geo_heatmap.html')


if __name__ == "__main__":
    sess.init_app(app)
    app.run(debug = True)
