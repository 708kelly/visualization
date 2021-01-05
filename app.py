import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# df = pd.read_csv('/Users/wangyiting/Downloads/country_indicators.csv')
app_data = {}
apps = ['OLS', 'XGBoost', 'Poisson', 'NB']
for w in apps:
    data_dic = {}
    file_path = os.path.join('output', 'best_policy_'+ w +'.xlsx')
    data_dic['Best Action'] = pd.read_excel(open(file_path, 'rb'),sheet_name='action', index_col=0)  
    data_dic['Expected Revenue'] = pd.read_excel(open(file_path, 'rb'),sheet_name='value', index_col=0) 
    app_data[w] = data_dic
# print(df)
available_indicators = data_dic.keys()
eg_data = list(data_dic.keys())
# print()
app.layout = html.Div([
    html.H2(children='球鞋需求估計與動態定價 - 第六組',
            style={
                    'textAlign': 'center',
                    'color': 'black'
        }),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=eg_data[0]
            )
        ],
        style={'width': '98%', 'display': 'inline-block'}),
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter2',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

    ]),
    html.Div([
        html.Div([
        html.Div(dcc.Slider(
            id='crossfilter-year--slider',
            min=max(data_dic[eg_data[0]].columns.min(),1),
            max=data_dic[eg_data[0]].columns.max(),
            value=data_dic[eg_data[0]].columns.max(),
            marks={str(p): str(p) for p in data_dic[eg_data[0]].columns},
            step=None
        ), style={'padding': '0px 20px 20px 20px'}),
        html.H6(children='剩下幾期',
            style={
                    'textAlign': 'center',
                    'color': 'black'
        })]
        , style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            html.Div(dcc.Slider(
                id='crossfilter-year--slider2',
                min=max(data_dic[eg_data[0]].index.min(),0),
                max=data_dic[eg_data[0]].index.max(),
                value=data_dic[eg_data[0]].index.max(),
                marks={str(p): str(p) for p in data_dic[eg_data[0]].index},
                step=None
            ), style={ 'padding': '0px 20px 20px 20px'}),
            html.H6(children='庫存數量',
            style={
                    'textAlign': 'center',
                    'color': 'black'
            })
                ]
            , style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

    ]),
    
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    dash.dependencies.Output('crossfilter-indicator-scatter2', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('crossfilter-year--slider2', 'value')])
def update_graph(xaxis_column_name, year_value, year2_value):
    df = data_dic[xaxis_column_name]
    # dff = df[year_value]
    # print(dff)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
                x=df.index,
                y=df[year_value],
                name="OLS"
            ))
    # fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig.add_trace(go.Scatter(
                x=df.index,
                y=app_data['Poisson'][xaxis_column_name][year_value],
                name="Poisson"
            ))
    fig.add_trace(go.Scatter(
                x=df.index,
                y=app_data['XGBoost'][xaxis_column_name][year_value],
                name="XGBoost"
            ))
    fig.add_trace(go.Scatter(
                x=df.index,
                y=app_data['NB'][xaxis_column_name][year_value],
                name="NB"
            ))
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(title="inventory", type='linear')

    fig.update_yaxes(title=xaxis_column_name, type='linear')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
                x=df.columns,
                y=df.loc[year2_value],
                name="OLS"
            ))
    # fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig2.add_trace(go.Scatter(
                x=df.columns,
                y=app_data['Poisson'][xaxis_column_name].loc[year2_value],
                name="Poisson"
            ))
    fig2.add_trace(go.Scatter(
                x=df.columns,
                y=app_data['XGBoost'][xaxis_column_name].loc[year2_value],
                name="XGBoost"
            ))
    fig2.add_trace(go.Scatter(
                x=df.columns,
                y=app_data['NB'][xaxis_column_name].loc[year2_value],
                name="NB"
            ))
    fig2.update_traces(mode='lines+markers')
    fig2.update_xaxes(title="period", type='linear')

    fig2.update_yaxes(title=xaxis_column_name, type='linear')

    fig2.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig, fig2




if __name__ == '__main__':
    app.run_server(debug=True)