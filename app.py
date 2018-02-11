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
    html.H1('Analysis of Spotify Data: When Songs Reach Their Peak', id='head-title'),
    html.P('The analysis is based on a spotify dataset. The dataset contains daily number of song plays for the top 200 songs in 53 countries. The data set covers all of 2017.', className='intro-information'),
    html.P('The data presented here has been filtered for songs that were played in all 53 countries represented in the data set. So if a song did not make it into the top 200 for all countries at least once, then the song was not included. Thus this visualization focuses on major international hits.', className='intro-information'),
    html.P('The dashboard contains two charts: a bar chart showing the order in which the song reached peak by country. For instance, Ed Sheeran Shape of You was the most played song in the data set. The song first hit peak number of plays in Ireland on January 6th, 2017 with about 130k plays Then it hit peak in the United Kingdom on January 9th with about 1.3 million plays', className='intro-information'),
    html.P('So you can get a feel for how a song traveled around the world gaining popularity in waves. The bar colors represent English speaking countries, Spanish speaking countries, and others. Although there is not always a discernible pattern with the bar colors, Despacito by Luis Fonsi presents an interesting case where clearly the song was popular in Spanish speaking countries before the song became popular around the world.', className='intro-information'),
    html.P("The second chart shows the total global plays by date. For Ed Sheeran Shape of You, he released the song at the beginning of January and then the song was also on his March album release. So you can clearly see the two spikes, which might be evidence of two separate marketing pushes. The song spiked again on New Year's Eve The general shape of a song is that it gets peak plays early in the release and quickly fizzles out.", className='intro-information'),
    html.H1('Choose a Song from the Dropdown Menu - Suggestion: Luis Fonsi Despacito', id='drop-down'),
    dcc.Dropdown(
            id='song-chooser',
            options=[{'label': i, 'value': i} for i in artists],
            value='Ed Sheeran Shape of You'
        ),
    html.Div([
        html.H3('Order in which the Song Peaked'),
        dcc.Graph(id='bar-chart')], id='chart-one'),
    html.Div([
        html.H3('Total Global Plays by Date'),
        dcc.Graph(id='line-chart')], id='chart-two')
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
        }],
        'layout': go.Layout(
            xaxis={'title': 'Country', 'tickangle':45},
            yaxis={'title': 'Number of Plays on Peak Day'},
            margin={'l': 100, 'b': 125, 't': 40, 'r': 20},
            legend={'x': 0, 'y': 1},
            showlegend=True,
            hovermode='closest',
            title='Order in which ' + selected_dropdown_value + ' Peaked'
        )

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
            margin={'l': 100, 'b': 40, 't': 40, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title='Total Global Plays by Date for ' + selected_dropdown_value + ' in 2017'
        )
    }

if __name__ == '__main__':
    app.run_server()
