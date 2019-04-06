from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd


app = Flask(__name__)


# This is an API meant to serve some tree health data for various neighborhoods in NYC
@app.route('/tree_health/<neighborhood>')
def return_health_data(neighborhood):
    base = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
    url = (base +
                 '$select=health, tree_dbh, nta_name' +
                 f'&$where=nta_name="{neighborhood}"')
    url = url.replace(' ', '%20')
    raw_data = pd.read_json(url)
    length = raw_data.shape[0]
    raw_data['index'] = range(length)

    # Pivot so it's easier to build our json. Data now looks like this:
    # | Date | High | Middle | Low |
    # (Date is the index)
    filtered_data = raw_data.pivot(columns='health', index='index', values='tree_dbh')

    # Build our json, then return it with jsonify


    return filtered_data.to_json()


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
