import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

all_datas = pd.read_csv('./games.csv',sep=',',encoding='gbk')
all_datas = all_datas.dropna(subset=["genre"])
all_types = list()
for item in all_datas.drop_duplicates(subset=['genre'], keep='first', inplace=False)['genre']:
    item_dict = {
        'label': item,
        'value': item
    }
    all_types.append(item_dict)

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

app.layout = html.Div([
    html.H1('Game Metacritic Analysis', style={'textAlign': 'center'}),
    html.Br(),
    html.Div(
        [html.Div(["Type: ", dcc.Dropdown(options=all_types,
                                        id='type',
                                        value='Action'),
                  ],
                 style={'width': '33%', 'display': 'inline-block'}
                 ),
        html.Div(["Attribute: ", dcc.Dropdown(options=[{'label':'metascore', 'value':'metascore'},
                                                       {'label':'user score', 'value':'user_score'}],
                                        id='attribute',
                                        value='user_score'),
                  ],
                 style={'width': '33%', 'display': 'inline-block'}),
        html.Div(["Year: ", dcc.Dropdown(options=[{'label':'{}'.format(year), 'value':'{}'.format(year)} for year in range(2011,2020)],
                                          id='year',
                                          value='2011'),
                   ],
                  style={'width': '33%', 'display': 'inline-block'}
                  ),
         ]),

    html.Div(id='dash_table'),

    html.Div(dcc.Graph(id='graph1')),
])


@app.callback(
    Output(component_id='dash_table', component_property='children'),
    [Input(component_id='type', component_property='value'),
     Input(component_id='attribute', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def update_output_div(type, attribute, year):
    new_datas = all_datas[all_datas['genre']==type]
    new_datas = new_datas[new_datas['release_date'].str.contains('-'+year[-2:]+'$', na=True)]
    new_datas[attribute].astype('float')
    new_datas = new_datas.sort_values(by=attribute, ascending=False)
    return generate_table(new_datas,max_rows=10)

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='type', component_property='value'),
     Input(component_id='attribute', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def update_output_div1(type, attribute, year):
    new_datas = all_datas[all_datas['genre']==type]
    new_datas = new_datas[new_datas['release_date'].str.contains('-'+year[-2:]+'$', na=True)]
    new_datas[attribute].astype('float')
    new_datas = new_datas.sort_values(by=attribute, ascending=False)
    new_datas.reset_index(inplace=True)
    new_datas = new_datas.loc[0:9,:]
    fig = px.bar(new_datas, x='game', y=attribute, barmode="group")
    fig.update_layout(title="%s of games" % (attribute),
                      xaxis_title="Game",
                      yaxis_title=attribute)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
