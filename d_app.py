from dash.dependencies import Input, Output
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


df_usa = pd.read_csv('output/usa_covid19.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='COVID 19 USA Dashboard'),

    html.Div(children='''
        Dashboard created using plotly dash for Python. 
        Data from NY Times 
    '''),

    # dcc.Input(id='start-date', value='2020-03-26', type='text'),

    dcc.RadioItems(
        id='plot_by',
        options=[
            {'label': 'Case', 'value': '1'},
            {'label': 'Death', 'value': '0'},
        ],
        value='1',
    ),

    # dcc.Input(id='end-date', value='1', type='text'),

    # dcc.Graph(
    #     id='main-graph',
    # ),
    dcc.Graph(
        id='map-graph',
        style={"height": 800}
    )
])


@app.callback(
    Output(component_id='map-graph', component_property='figure'),
    [Input(component_id='plot_by', component_property='value'),
     # Input(component_id='start-date', component_property='value')
     ]
)
def query_data(plot_by):
    # df_tmp = df_who.query(f"location == '{country_name}' ")
    date = df_usa['date'].max()
    df_tmp = df_usa.query(f" date == '{date}' ").drop_duplicates(subset=['latitude', 'longitude'])
    if plot_by == "1":
        fig_map = px.scatter_geo(df_usa, lat="latitude", lon="longitude", color="state",
                       hover_name="county", size="cases", template='plotly_dark',
                       animation_frame="date", scope="usa", size_max=60)
        # fig_map = px.scatter_geo(df_tmp, lat="latitude", lon="longitude", color="state", size_max=80,
        #                          hover_name="county", size="cases", template='plotly_dark', scope='usa')
    else:
        fig_map = px.scatter_geo(df_usa, lat="latitude", lon="longitude", color="state",
                                 hover_name="county", size="deaths", template='plotly_dark',
                                 animation_frame="date", scope="usa", size_max=60)
        # fig_map = px.scatter_geo(df_tmp, lat="latitude", lon="longitude", color="state", size_max=90,
        #                          hover_name="county", size="deaths", template='plotly_dark', scope='usa')
    return fig_map


if __name__ == '__main__':
    app.run_server(debug=True)