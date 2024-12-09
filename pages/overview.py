import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
import pandas as pd
import plotly.graph_objects as go


# Load the dataset
df_tracks = pd.read_csv(r'C:\Users\cibei\OneDrive\Desktop\Data Visualization Methods\pythonProject\data\spotify_songs.csv')

# Calculate metrics
total_artists = df_tracks['track_artist'].nunique()
total_tracks = len(df_tracks)
avg_artist_popularity = round(df_tracks['track_popularity'].mean(), 2)
avg_track_duration = round(df_tracks['duration_ms'].mean() / 1000, 2)

# Function to parse the date and extract the year
def parse_date(date):
    try:
        return pd.to_datetime(date, format='%Y-%m-%d').year
    except ValueError:
        try:
            return pd.to_datetime(date, format='%Y').year
        except ValueError:
            return pd.NaT

# Apply parse_date function and create a 'year' column
df_tracks['year'] = df_tracks['track_album_release_date'].apply(parse_date)

# Generate options for year dropdown
available_years = sorted(df_tracks['year'].dropna().unique().astype(int))
dropdown_year_options = [{"label": str(year), "value": year} for year in available_years]

# Initialize top tracks data for the table
top_tracks = df_tracks[['track_name', 'track_artist', 'track_popularity', 'duration_ms', 'year']].sort_values(
    by='track_popularity', ascending=False).head(10)

# Define layout for the Overview page
dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H1("Spotify Overview", className="text-center", style={"color": "#1DB954", "margin-bottom": "20px"})
                ]), width=12)
            ],
            className="mb-4",
            style={"backgroundColor": "black"},
        ),

        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H2(f"{total_artists}", className="text-center", style={"color": "#1DB954"}),
                    html.P("Total Artists", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"{avg_artist_popularity}", className="text-center", style={"color": "#1DB954"}),
                    html.P("Avg Artist Popularity", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"{total_tracks}", className="text-center", style={"color": "#1DB954"}),
                    html.P("Total Tracks", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"{avg_track_duration}", className="text-center", style={"color": "#1DB954"}),
                    html.P("Avg Track Duration (s)", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),
            ],
            justify="center",
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.Label("Select Starting Year:", style={"color": "#1DB954"}),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=dropdown_year_options,
                            value=available_years[0],  # Default to the earliest year
                            className="custom-dropdown"
                        )
                    ]),
                    width=6
                ),
                dbc.Col(
                    html.Div([
                        html.Label("Select Year for Top Tracks:", style={"color": "#1DB954"}),
                        dcc.Dropdown(
                            id="top-tracks-year-dropdown",
                            options=dropdown_year_options,
                            value=available_years[0],  # Default to earliest year
                            className="custom-dropdown"
                        )
                    ]),
                    width=6
                )
            ],
            className="mb-4",
            style={"backgroundColor": "black"}
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="songs-per-year-bar-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
                    ),
                    width=6
                ),
                dbc.Col(
                    html.Div([
                        html.H4("List of Top Tracks by Popularity",
                                style={"color": "#1DB954", "textAlign": "center", "margin-bottom": "10px"}),
                        DataTable(
                            id="top-tracks-table",
                            columns=[
                                {"name": "Track Name", "id": "track_name"},
                                {"name": "Artist", "id": "track_artist"},
                                {"name": "Popularity", "id": "track_popularity"},
                                {"name": "Duration (ms)", "id": "duration_ms"},
                                {"name": "Year", "id": "year"}
                            ],
                            data=top_tracks.to_dict('records'),
                            fixed_rows={'headers': True},
                            style_table={'height': '300px', 'overflowY': 'auto'},
                            style_header={'backgroundColor': '#1DB954', 'color': 'Black'},
                            style_cell={
                                'backgroundColor': 'black',
                                'color': 'white',
                                'textAlign': 'center',
                                'whiteSpace': 'normal',  # Allows text wrapping in cells
                                'height': 'auto',  # Automatically adjust row height
                            },
                            style_cell_conditional=[
                                {'if': {'column_id': 'track_name'}, 'width': '25%'},
                                {'if': {'column_id': 'track_artist'}, 'width': '20%'},
                                {'if': {'column_id': 'track_popularity'}, 'width': '15%'},
                                {'if': {'column_id': 'duration_ms'}, 'width': '20%'},
                                {'if': {'column_id': 'year'}, 'width': '20%'},
                            ],
                            style_data={'border': '1px solid gray'},
                            page_size=10
                        )
                    ]),
                    width=6
                )
            ],
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.Label("Select Year Range for Line Chart:",
                                   style={"color": "#1DB954", "font-size": "16px"}),
                        dcc.RangeSlider(
                            id="line-chart-year-slider",
                            min=min(available_years),
                            max=max(available_years),
                            value=[min(available_years), max(available_years)],
                            marks={str(year): str(year) for year in available_years if year % 5 == 0}, # Show every 5 years
                            step=1,  # Allow step-by-step movement
                            tooltip={"placement": "bottom", "always_visible": True},  # Show tooltip on slider
                            className="custom-slider"
                        )
                    ], style={"padding": "10px"})
                    , width=12)
            ],
            className="mb-2",
            style={"backgroundColor": "black"}
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="popularity-line-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
                    ),
                    width=12
                )
            ]
        ),
    ],
    fluid=True

)

# Define callbacks to update charts based on selected year
@dash.callback(
    Output("songs-per-year-bar-chart", "figure"),
    Input("year-dropdown", "value")
)

def update_bar_chart(start_year):
    filtered_df = df_tracks[df_tracks['year'] >= start_year]
    songs_per_year = filtered_df['year'].value_counts().reset_index()
    songs_per_year.columns = ['year', 'count']
    songs_per_year = songs_per_year.sort_values(by='year')

    # Bar Chart for number of songs per year
    fig_bar = go.Figure(go.Bar(
        x=songs_per_year['year'],
        y=songs_per_year['count'],
        marker_color="#1DB954"
    ))
    fig_bar.update_layout(
        title="Number of Songs per Year",
        xaxis_title="Year",
        yaxis_title="Number of Songs",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return  fig_bar

# Define callback to update line chart based on slider value
@dash.callback(
    Output("popularity-line-chart", "figure"),
    Input("line-chart-year-slider", "value")
)

def update_line_chart(year_range):
    filtered_df = df_tracks[(df_tracks['year'] >= year_range[0]) & (df_tracks['year'] <= year_range[1])]
    popularity_by_year = filtered_df.groupby('year')['track_popularity'].mean().reset_index()


    fig_line = go.Figure(go.Scatter(
            x=popularity_by_year['year'],
            y=popularity_by_year['track_popularity'],
            mode='lines+markers',
            line=dict(color="#1DB954", width=2),
            marker=dict(size=6, color="#1DB954", symbol='circle')
        ))
    fig_line.update_layout(
        title="Average of Track Popularity by Year",
        yaxis=dict(
            title="Average of Track Popularity",
            range=[0, 100],  # Set y-axis range from 0 to 100
            showgrid=False
        ),
        xaxis=dict(
            title="Year",
            showgrid=False
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return fig_line

# Define callback to update top tracks table based on selected year
@dash.callback(
    Output("top-tracks-table", "data"),
    Input("top-tracks-year-dropdown", "value")
)
def update_top_tracks_table(selected_year):
    filtered_top_tracks = df_tracks[df_tracks['year'] == selected_year].sort_values(
        by='track_popularity', ascending=False).head(10)
    return filtered_top_tracks.to_dict('records')

