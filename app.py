import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('peak_dates_world_songs.csv')
df_total = pd.read_csv('total_plays_by_date.csv')

artists = df['Artist_Trackname'].drop_duplicates().sort_values(ascending=True)

colors = {'Spanish Speaking':'rgba(93, 165, 218, 1)', 
        'Asia':'rgba(160,160,160,.8)', 
        'Portuguese Speaking':'rgba(160,160,160,.8)', 
        'Global':'rgba(160,160,160,.8)', 
        'English Speaking':'rgba(178, 145, 47, 1)', 
        'Spain':'rgba(93, 165, 218, 1)', 
        'Europe':'rgba(160,160,160,.8)'}

app = dash.Dash()

app.layout = html.Div([
    html.H1('Analysis of Spotify Data: When Songs Reach Their Peak'),
    html.P('The analysis is based on a spotify dataset containing the top 200 songs played daily in each country.'),
    html.P('The data is filtered for songs that were played at least once in all 54 countries'),
    html.P('So the data represents big international hits.'),
    html.P('The dashboard contains two charts: a bar chart showing the order in which the song hit peak by country. For instance, Ed Sheeran Shape of You first hit peak in Ireland on January 6th, 2017 with about 130k plays'),
    html.P('Then it hit peak in the United Kingdom on January 9th with about 1.3 million plays'),
    html.P('So you can get a feel for how a song traveled around the world gaining popularity in waves'),
    html.P('The bar colors represent English speaking countries, Spanish speaking countries, and others'),
    html.P('Although there is not always a discernible pattern with the bar colors, Despacito by Luis Fonsi presents an interesting case'),
    html.P('The second chart shows the total global plays by date. For Ed Sheeran Shape of You, he released the song at the beginning of January and then the song was also on his March album release. So you can see how marketing plays into when people listen.'),
    html.H3('Choose a Song from the Dropdown Menu'),
    dcc.Dropdown(
        id='song-chooser',
        options=[{'label': i, 'value': i} for i in artists],
        value='Ed Sheeran Shape of You'
    ),
    dcc.Graph(id='bar-chart'),
    html.H2('Total Global Plays By Date'),
    dcc.Graph(id='line-chart')
])

@app.callback(Output('bar-chart', 'figure'), [Input('song-chooser', 'value')])
def update_graph(selected_dropdown_value):
    dataframe = df[df['Artist_Trackname'] == selected_dropdown_value]
    dataframe = dataframe.sort_values('Date')
    dataframe = dataframe[dataframe['Region'] != 'Global']

    dataframe['Colors'] = dataframe['Group'].replace(colors)

    return {
        'data': [{
            'x': dataframe.Region,
            'y': dataframe.Streams,
            'text': dataframe.Date,
            'type': 'bar',
            'marker': dict(color = dataframe.Colors)
        }]
    }


@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('song-chooser', 'value')])
def update_figure(selected_dropdown_value):
    df_date = df_total[df_total['Artist_Trackname'] == selected_dropdown_value]
    df_date = df_date.sort_values('Date')

    traces = []
    traces.append(go.Scatter(
        x=pd.to_datetime(df_date['Date']),
        y=df_date['Streams'],
        text=df_date['Artist_Trackname'],
        mode='lines',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'blue'}
        }
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Total Plays'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
