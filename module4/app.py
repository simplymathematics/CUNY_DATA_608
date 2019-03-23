import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')
cocalc_project_id = os.environ['COCALC_PROJECT_ID']

city = pd.DataFrame()
boros = ["'Bronx'","'Staten Island'", "'Manhattan'", "'Queens'", "'Brooklyn'"]
for boro in boros:
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=health,count(tree_id)' +\
            '&$where=boroname='+boro +\
            'AND NOT health=\'NaN\''
            '&$group=health').replace(' ', '%20')
    #print(soql_url)
    soql_health = pd.read_json(soql_url)
    soql_health['boroname'] = boro
    city = city.append(soql_health)
city = city.replace({'health':'Poor'}, 1)
city = city.replace({'health':'Fair'}, 2)
city = city.replace({'health':'Good'}, 3)


app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Tree Health by Boro'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Queens', 'value': "'Queens'"},
            {'label': 'Brooklyn', 'value': "'Brooklyn'"},
            {'label': 'Manhattan', 'value': "'Manhattan'"},
            {'label': 'Staten Island', 'value': "'Staten Island'"},
            {'label': 'Bronx', 'value': "'Bronx'"}
        ],
        value="'Queens'"
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = city[city['boroname'] == selected_dropdown_value]

    return {
        'data': [{
            'x': dff.count_tree_id,
            'y': dff.health,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }

port = 9990
pfx = "/{}/server/{}/".format(cocalc_project_id, port)
app.config.requests_pathname_prefix = pfx

if __name__ == '__main__':
    print("browse to https://cocalc.com{}".format(pfx))
    app.run_server(debug=True, port=port, host='0.0.0.0')