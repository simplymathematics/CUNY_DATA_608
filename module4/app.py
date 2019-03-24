import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os
import numpy as np
import plotly
import plotly.graph_objs as go
import scipy.stats as scs

server = flask.Flask('app')


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

# With steward, Good Heatlth

city2 = pd.DataFrame()
boros = ["'Bronx'","'Staten Island'", "'Manhattan'", "'Queens'", "'Brooklyn'"]
for boro in boros:
    soql_url2 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward, count(health)' +\
        '&$where=boroname='+boro +\
        'AND NOT health=\'NaN\'' +\
        'AND NOT steward=\'NaN\'' +\
        'AND NOT steward=\'None\'' +\
        'AND NOT health=\'Poor\'' +\
        '&$group=steward').replace(' ', '%20')
    soql_steward = pd.read_json(soql_url2)
    soql_steward['boroname'] = boro
    city2 = city2.append(soql_steward)
city2 = city2.replace('3or4', 1)
city2 = city2.replace('4orMore', 1)
city2 = city2.replace('1or2', 1)

city2 = city2.groupby('boroname').sum()
city2 = city2.drop(columns = 'steward')
city2

# No Steward, Good Health

city3 = pd.DataFrame()
boros = ["'Bronx'","'Staten Island'", "'Manhattan'", "'Queens'", "'Brooklyn'"]
for boro in boros:
    soql_url2 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward, count(health)' +\
        '&$where=boroname='+boro +\
        'AND NOT health=\'NaN\'' +\
        'AND steward=\'None\'' +\
        'AND NOT steward=\'NaN\'' +\
        'AND NOT health=\'Poor\'' +\
        '&$group=steward').replace(' ', '%20')
    soql_steward = pd.read_json(soql_url2)
    soql_steward['boroname'] = boro
    city3 = city3.append(soql_steward)

city3 = city3.replace({'None': 0})
city3 = city3.groupby('boroname').sum()
city3 = city3.drop(columns = 'steward')
city3

# With steward, Bad Health

city4 = pd.DataFrame()
boros = ["'Bronx'","'Staten Island'", "'Manhattan'", "'Queens'", "'Brooklyn'"]
for boro in boros:
    soql_url2 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward, count(health)' +\
        '&$where=boroname='+boro +\
        'AND NOT health=\'NaN\'' +\
        'AND NOT steward=\'NaN\'' +\
        'AND NOT steward=\'None\'' +\
        'AND health=\'Poor\'' +\
        '&$group=steward').replace(' ', '%20')
    soql_steward = pd.read_json(soql_url2)
    soql_steward['boroname'] = boro
    city4 = city4.append(soql_steward)
city4 = city4.replace('3or4', 1)
city4 = city4.replace('4orMore', 1)
city4 = city4.replace('1or2', 1)

city4 = city4.groupby('boroname').sum()
city4 = city4.drop(columns = 'steward')
city4

# No Steward, Bad Health

city5 = pd.DataFrame()
boros = ["'Bronx'","'Staten Island'", "'Manhattan'", "'Queens'", "'Brooklyn'"]
for boro in boros:
    soql_url2 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward, count(health)' +\
        '&$where=boroname='+boro +\
        'AND NOT health=\'NaN\'' +\
        'AND steward=\'None\'' +\
        'AND NOT steward=\'NaN\'' +\
        'AND health=\'Poor\'' +\
        '&$group=steward').replace(' ', '%20')
    soql_steward = pd.read_json(soql_url2)
    soql_steward['boroname'] = boro
    city5 = city5.append(soql_steward)

city5 = city5.replace({'None': 0})
city5 = city5.groupby('boroname').sum()
city5 = city5.drop(columns = 'steward')
city5

# Make big df for analysis

steward_good = city2
steward_bad = city4

no_good = city3
no_bad = city5
big = pd.DataFrame()

steward_good


big['steward good'] = steward_good['count_health']
big['steward bad']  = steward_bad['count_health']
big['no steward good'] = no_good['count_health']
big['no steward bad']  = no_bad['count_health']

big = big.transpose()

# Statistics Test

obs = [big[boro][0], big[boro][1] ]
exp = [big[boro][2], big[boro][3] ]

obs_total = np.sum(obs)
exp_total = np.sum(exp)

obs = obs/obs_total * 100
exp = exp/exp_total * 100

result = scs.chisquare(obs,exp)
result = bool(result[1]<.05)
if result == True:
    conclusion = "We have sufficient evidence to suggest that stewardship effects tree health."
else:
    conclusion = "We have insufficient evidence to suggest that stewardship effects tree health."
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
    dcc.Graph(id='my-graph'),
    html.H1('Tree Health vs Stewardship'),
    dcc.Dropdown(
        id='my-dropdown2',
        options=[
            {'label': 'Queens', 'value': "'Queens'"},
            {'label': 'Brooklyn', 'value': "'Brooklyn'"},
            {'label': 'Manhattan', 'value': "'Manhattan'"},
            {'label': 'Staten Island', 'value': "'Staten Island'"},
            {'label': 'Bronx', 'value': "'Bronx'"}
        ],
        value="'Queens'"
    ),
    dcc.Graph(id='total-graph'),
    html.H2("Conclustion: "),
    html.H3(conclusion)
], className="container")

#interactive graph
@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = city[city['boroname'] == selected_dropdown_value]

    return {
        'data': [{
            'x': dff.health,
            'y': dff.count_tree_id,
            'type': 'bar'
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


# graph 2
@app.callback(Output('total-graph', 'figure'),
              [Input('my-dropdown2', 'value')])
def update_graph2(selected_dropdown_value):
    boro = selected_dropdown_value
    trace1 = go.Bar(
        x=["Good Health", "Bad Health"],
        y= [big[boro][0], big[boro][1]],
        name='With Steward'
    )
    trace2 = go.Bar(
        x= ["Good Health", "Bad Health"],
        y= [big[boro][2], big[boro][3]],
        name='Without Steward'
    )
    return {
        'data': [trace1, trace2],
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
if __name__ == '__main__':
    print("browse to localhost:" + str(port))
    app.run_server(debug=True, port=port, host='0.0.0.0')