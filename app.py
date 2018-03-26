from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from sklearn.externals import joblib
import pandas as pd
import geocoder
from key import key_s
import googlemaps
import ast
import numpy as np

dictionary={}
app = Flask(__name__)
app.secret_key = "thisisasecretshhhh"


@app.route('/',  methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        try:
            all_args = request.args.to_dict()
            print('allargs' + all_args['dicti'])
            return render_template('main.html', dicti= ast.literal_eval(all_args['dicti']))
        except Exception as e:
            pass

    return render_template('main.html', dicti=dictionary)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    error=None
    svm = joblib.load('dispatch_classifier.pkl')
    print('model loaded')
    if request.method == 'POST':
        location_input = request.form['location_input']
        time_input = request.form['time_input']
        if len(location_input.split(' ')) > 2:
            try:
                gm = googlemaps.Client(key=key_s)
                geocode_result = gm.geocode(location_input)
                lat = geocode_result[0]['geometry']['location']['lat']
                lon = geocode_result[0]['geometry']['location']['lng']
            except Exception as e:
                flash("Something went wrong! Check the format of the address and try to provide as much information as possible. If entering coordinates, make sure each coordinate is separated by a comma and a space.")

        elif len(location_input.split(' ')) > 0:
            try:
                loc_arr = location_input.split(', ')
                lat = loc_arr[0]
                lon = loc_arr[1]
                print("Latitude and Longitude: " + str(lat) + ", " + str(lon))

            except IndexError as e:
                flash("Something went wrong! Check the format of the address and try to provide as much information as possible. If entering coordinates, make sure each coordinate is separated by a comma and a space.")


        try:
            (h, m, s) = time_input.split(':')
            if (int(h) > 23) or (int(m) > 59) or (int(float(s)) > 59):
                raise Exception('Invalid time entered')
            time = int(h) * 3600 + int(m) * 60 + int(float(s))
            print(time)
        except Exception as e:
            flash("Something went wrong! Make sure the time is entered as a 24 hour time in the format hh:mm:ss.")


        try:
            print("we in here")
            df = pd.DataFrame()
            print(lat)

            df['Latitude'] = [lat]
            print("what about here")

            df['Longitude'] = [lon]
            df['timestamp'] = [time]
            print("what about here")
            print(svm.predict_proba(df))
            dictionary = dict(zip(svm.classes_, svm.predict_proba(df)[0]))
            print("what about here1")
            dictionary_key = sorted(dictionary, key=dictionary.get)[::-1]
            print("what about here2")
            dictionary_val = sorted(dictionary.values())[::-1]
            print("what about here3")
            dictionary = dict(zip(dictionary_key, dictionary_val))
            print("what about here3")
            return redirect(url_for('main', dicti=dictionary))

        except Exception as e:
            pass

    return redirect(url_for('main'))

@app.route('/map',  methods=['GET', 'POST'])
def map():
    return render_template('geo_heatmap.html')


if __name__ == "__main__":
    sess.init_app(app)
    app.run(debug = True)








'''
from flask import Flask, render_template, flash, request, url_for, redirect, session, logging
from sklearn.externals import joblib
import pandas as pd
import geocoder
from key import key_s
import googlemaps

app = Flask(__name__)
app.secret_key = "thisisasecretshhhh"


@app.route('/',  methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    error=None
    svm = joblib.load('svm_classifier.pkl')
    print('model loaded')
    if request.method == 'POST':
        location_input = request.form['location_input']
        time_input = request.form['time_input']
        if len(location_input.split(' ')) > 2:
            try:
                gm = googlemaps.Client(key=key_s)
                geocode_result = gm.geocode(location_input)
                lat = geocode_result[0]['geometry']['location']['lat']
                lon = geocode_result[0]['geometry']['location']['lng']
            except Exception as e:
                flash("Something went wrong! Check the format of the address and try to provide as much information as possible.")

        elif len(location_input.split(' ')) > 0:
            try:
                loc_arr = location_input.split(', ')
                lat = loc_arr[0]
                lon = loc_arr[1]
            except IndexError as e:
                flash("Something went wrong! Check the format of the coordinates. Make sure each coordinate is separated by a comma and a space.")


        try:
            (h, m, s) = time_input.split(':')
            if (int(h) > 23) or (int(m) > 59) or (int(float(s)) > 59):
                raise Exception('Invalid time entered')
            time = int(h) * 3600 + int(m) * 60 + int(float(s))
            print(time)
        except Exception as e:
            flash("Something went wrong! Make sure the time is entered as a 24 hour time in the format hh:mm:ss.")


        try:
            df = pd.DataFrame()
            df['Latitude'] = [lat]
            df['Longitude'] = [lon]
            df['timestamp'] = [time]
            dictionary = dict(zip(svm.classes_, svm.predict_proba(df)[0]))
            print(dictionary)
            return redirect(url_for('main', dictionary = dictionary))
        except Exception as e:
            pass

    return redirect(url_for('main'))

if __name__ == "__main__":
    sess.init_app(app)
    app.run(debug = True)


'''
