from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd


app = Flask(__name__)


# This is an API meant to serve some tree health data for various neighborhoods in NYC
@app.route('/tree_health/<string:health>/<string:neighborhood>')
def return_health_data(health, neighborhood):

    # Read in raw data
    url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
           '$select=nta_name,tree_dbh,health' +\
           '&$where=nta_name='+neighborhood +\
           'AND health='+health).replace(' ', '%20')


    raw_data = pd.read_json(url)
    length = raw_data.shape[0]
    raw_data['index'] = range(length)


    # Filter based on seasonality and metro
    filtered_data = raw_data.loc[(raw_data['nta_name'] == neighborhood) & (raw_data['health'] == health),
                                 ['index', 'health', 'nta_name', 'tree_dbh']]

    # Pivot so it's easier to build our json. Data now looks like this:
    # | Date | High | Middle | Low |
    # (Date is the index)
    filtered_data = filtered_data.pivot(columns='nta_name', index='index', values='tree_dbh')

    # Build our json, then return it with jsonify


    return jsonify(filtered_data_json)


# This routing allows us to view index.html
@app.route('/')
def index():
    return render_template('index.html')


# This routing allows us to load local Javascript
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(debug=True)
