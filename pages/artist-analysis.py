import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors




# Load dataset
df_tracks = pd.read_csv(r'C:\Users\cibei\OneDrive\Desktop\Data Visualization Methods\pythonProject\data\spotify_songs.csv')
df_tracks['track_artist'] = df_tracks['track_artist'].astype(str)

# Calculate metrics for the visualizations
top_artists = df_tracks.groupby('track_artist').agg({'track_popularity': 'mean'}).nlargest(10, 'track_popularity').reset_index()
top_genres = df_tracks.groupby('playlist_genre').agg({'track_popularity': 'mean'}).nlargest(10, 'track_popularity').reset_index()
popularity_by_year = df_tracks.groupby('track_album_release_date')['track_popularity'].mean().reset_index()

top_artists = top_artists.sort_values(by='track_popularity', ascending=False)
# Get the range of popularity values for the bars being plotted
min_popularity = top_artists['track_popularity'].min()
max_popularity = top_artists['track_popularity'].max()

# Convert hex colors to RGB tuples
color_start = plotly.colors.hex_to_rgb('#d3f9d8')  # Light green
color_end = plotly.colors.hex_to_rgb('#1DB954')  # Spotify green

# Map popularity values to the gradient for the bars
popularity_artist = top_artists['track_popularity']
colors_artist = [
    plotly.colors.find_intermediate_color(
        color_start, color_end, (value - min_popularity) / (max_popularity - min_popularity)
    ) for value in popularity_artist
]

# Convert RGB tuples back to hex strings for Plotly
colors_artist_hex = [f"rgb({r},{g},{b})" for r, g, b in colors_artist]

# Generate options for genre dropdown
available_genres = sorted(df_tracks['playlist_genre'].dropna().unique())
dropdown_genre_options = [{"label": genre, "value": genre} for genre in available_genres]



# Define bar charts (vertical)
fig_artist_popularity = go.Figure(go.Bar(
    x=top_artists['track_artist'],  # Artists on the x-axis
    y=top_artists['track_popularity'],  # Popularity on the y-axis
    marker=dict(color=colors_artist_hex),  # Spotify green color
    text=top_artists['track_popularity'].round(1),  # Display values on the bars
    textposition='auto'  # Position the text in the center of the bars
))

fig_artist_popularity.update_layout(
    title=dict(
        text="Popularity by Artist",
        font=dict(size=20, color="white"),  # Larger title with white color
        x=0.5,  # Center the title
    ),
    xaxis=dict(
        title="Artist",
        tickmode="linear",
        tickangle=-45,  # Rotate artist names for readability
        showgrid=False,
        title_font=dict(size=14, color="white"),  # Style the axis title
        tickfont=dict(size=12, color="white")  # Style the tick labels
    ),
    yaxis=dict(
        title="Popularity",
        showgrid=True,
        gridcolor="gray",
        title_font=dict(size=14, color="white"),  # Style the axis title
        tickfont=dict(size=12, color="white")  # Style the tick labels
    ),
    plot_bgcolor="black",  # Set the plot background color to black
    paper_bgcolor="black",  # Set the paper background color to black
    font=dict(color="white")  # Set the overall font color to white
)


# Bar chart for popularity by genre
fig_genre_popularity = go.Figure(go.Bar(
    x=top_genres['playlist_genre'],  # Genres on the x-axis
    y=top_genres['track_popularity'],  # Popularity on the y-axis
    marker=dict(color=colors_artist_hex),  # Spotify green color
    text=top_genres['track_popularity'].round(1),  # Display values on the bars
    textposition='auto'  # Position the text in the center of the bars
))

fig_genre_popularity.update_layout(
    title=dict(
        text="Popularity by Genre",
        font=dict(size=20, color="white"),  # Larger title with white color
        x=0.5,  # Center the title
    ),
    xaxis=dict(
        title="Genre",
        tickmode="linear",
        tickangle=-45,  # Rotate genre names for readability
        showgrid=False,
        title_font=dict(size=14, color="white"),  # Style the axis title
        tickfont=dict(size=12, color="white")  # Style the tick labels
    ),
    yaxis=dict(
        title="Popularity",
        showgrid=True,
        gridcolor="gray",
        title_font=dict(size=14, color="white"),  # Style the axis title
        tickfont=dict(size=12, color="white")  # Style the tick labels
    ),
    plot_bgcolor="black",  # Set the plot background color to black
    paper_bgcolor="black",  # Set the paper background color to black
    font=dict(color="white")  # Set the overall font color to white
)



# Define layout for the Artist Analysis page
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H1("Artist Analysis", className="text-center",
                            style={"color": "#1DB954", "margin-bottom": "20px"})
                ]), width=12)
            ],
            className="mb-4",
            style={"backgroundColor": "black"},
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_artist_popularity,
                                  config={
                                      "displayModeBar": False  # Disables the toolbar
                                  }
                ),
                width=6),
                dbc.Col(dcc.Graph(figure=fig_genre_popularity,
                                  config={
                                      "displayModeBar": False  # Disables the toolbar
                                  }
                ),
                width=6),
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Select Genre:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="genre-dropdown",
                        options=dropdown_genre_options,
                        value=available_genres[0],  # Default to the first genre
                        className="custom-dropdown"
                    )
                ]), width=6),  # Adjusted width to half of the row

                dbc.Col(html.Div([
                    html.Label("Select First Artist:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="artist-dropdown-1",
                        options=[{"label": artist, "value": artist} for artist in
                                 sorted(df_tracks['track_artist'].astype(str).unique())],
                        value="Dua Lipa",
                        placeholder="Select the first artist...",
                        className="custom-dropdown"
                    )
                ]), width=6)
            ],
            className="mb-4",
            style={"backgroundColor": "black"}
        ),

        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Minimum Number of Tracks:", style={"color": "#1DB954"}),
                    dcc.Input(
                        id="min-tracks-input",
                        type="number",
                        min=1,  # Minimum value for input
                        value=1,  # Default to 1 track
                        className="custom-input",
                        style={"width": "100%", "padding": "5px"}
                    )
                ]), width=6),

                dbc.Col(html.Div([
                    html.Label("Select Second Artist:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="artist-dropdown-2",
                        options=[{"label": artist, "value": artist} for artist in
                                 sorted(df_tracks['track_artist'].astype(str).unique())],
                        value="Maroon 5",
                        placeholder="Select the second artist...",
                        className="custom-dropdown"
                    )
                ]), width=6)
            ],
            className="mb-4",
            style={"backgroundColor": "black"}
        ),
        dbc.Row(
            [
                dbc.Col(html.H4("Most Popular Artist by Genre", className="text-left", style={"color": "#1DB954", "margin-bottom": "10px"}), width=12),
                dbc.Col(
                    DataTable(
                        id="most-popular-artist-table",
                        columns=[
                            {"name": "Artist", "id": "track_artist"},
                            {"name": "Genre", "id": "playlist_genre"},
                            {"name": "Popularity", "id": "avg_popularity"},
                            {"name": "Avg Duration (ms)", "id": "avg_duration"},
                            {"name": "Number of Tracks", "id": "num_tracks"},
                        ],
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
                            {'if': {'column_id': 'track_artist'}, 'width': '20%'},
                            {'if': {'column_id': 'playlist_genre'}, 'width': '20%'},
                            {'if': {'column_id': 'track_popularity'}, 'width': '20%'},
                            {'if': {'column_id': 'avg_duration'}, 'width': '20%'},
                            {'if': {'column_id': 'num_tracks'}, 'width': '20%'},
                        ],
                        style_data={'border': '1px solid gray'},
                        page_size=10,
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id="artist-radar-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
                    ),
                    width=6  # Adjust the width to fit the table
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Select Genre:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="genre-dropdown",
                        options=dropdown_genre_options,
                        value=available_genres[0],  # Default to the first genre
                        className="custom-dropdown"
                    )
                ]), width=6),

                dbc.Col(html.Div([
                    html.Label("Number of Top Artists:", style={"color": "#1DB954"}),
                    dcc.Input(
                        id="min-artists-input",
                        type="number",
                        min=1,  # Minimum value
                        value=5,  # Default top 5 artists
                        className="custom-input",
                        style={"width": "100%", "padding": "5px"}
                    )
                ]), width=6)
            ],
            className="mb-4",
            style={"backgroundColor": "black"}
        ),

        dbc.Row(
            [
                dbc.Col(html.H4("Artist-Genre Popularity Bar Chart", className="text-center", style={"color": "#1DB954"}),
                        width=12),
                dbc.Col(
                    dcc.Graph(
                        id="artist-genre-barchart",
                        config={
                                "displayModeBar": False  # Disables the toolbar
                                  }
                    ),
                    width=12  # Full width for treemap
                )
            ],
            className="mb-4"
        ),
    ],
    fluid=True
)

# Register the page
dash.register_page(__name__, path="/artist-analysis")


@dash.callback(
    Output("most-popular-artist-table", "data"),
    [Input("genre-dropdown", "value"),
     Input("min-tracks-input", "value")]
)
def update_most_popular_artist_table(selected_genre, min_tracks):
    # Filter by selected genre
    filtered_df = df_tracks[df_tracks['playlist_genre'] == selected_genre]

    # Group by artist and calculate metrics
    top_artists_by_genre = (
        filtered_df.groupby(['track_artist', 'playlist_genre'], as_index=False)
        .agg({
            'track_popularity': 'mean',  # Average popularity
            'duration_ms': 'mean',      # Average duration
            'track_id': 'count'         # Number of tracks
        })
        .rename(columns={
            'track_popularity': 'avg_popularity',  # Ensure correct column renaming
            'duration_ms': 'avg_duration',
            'track_id': 'num_tracks'
        })
    )

    # Filter by minimum number of tracks
    top_artists_by_genre = top_artists_by_genre[top_artists_by_genre['num_tracks'] >= min_tracks]

    # Sort by average popularity and limit to top 10 artists
    top_artists_by_genre = top_artists_by_genre.sort_values(by='avg_popularity', ascending=False).head(10)

    # Convert the DataFrame to dictionary format for the DataTable
    data = top_artists_by_genre.to_dict('records')
    return data

@dash.callback(
    Output("artist-radar-chart", "figure"),
    [Input("artist-dropdown-1", "value"),
     Input("artist-dropdown-2", "value")]
)
def update_comparison_chart(artist_1, artist_2):
    if not artist_1 or not artist_2:
        return go.Figure()

    # Features to compare
    attributes = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

    # Normalize the attributes to a range of 0–1
    normalized_data = df_tracks.copy()
    for attr in attributes:
        min_val = df_tracks[attr].min()
        max_val = df_tracks[attr].max()
        normalized_data[attr] = (df_tracks[attr] - min_val) / (max_val - min_val)

    # Filter normalized data for selected artists and calculate mean
    artist_1_normalized = normalized_data[normalized_data['track_artist'] == artist_1][attributes].mean()
    artist_2_normalized = normalized_data[normalized_data['track_artist'] == artist_2][attributes].mean()

    # Ensure that data exists for both artists
    if artist_1_normalized.isnull().all() or artist_2_normalized.isnull().all():
        return go.Figure()

    # Radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=artist_1_normalized,
        theta=attributes,
        fill='toself',
        name=artist_1,
        marker=dict(color="#1DB954")
    ))

    fig.add_trace(go.Scatterpolar(
        r=artist_2_normalized,
        theta=attributes,
        fill='toself',
        name=artist_2,
        marker=dict(color="#FFD670")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])  # Normalized range
        ),
        showlegend=True,
        title="Artist Comparison Radar Chart",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    return fig

@dash.callback(
    Output("artist-genre-barchart", "figure"),
    [Input("genre-dropdown", "value"),
     Input("min-artists-input", "value")]
)
def update_artist_genre_percentage_barchart(selected_genre, top_artists_count):
    # Filter data by selected genre
    filtered_df = df_tracks if selected_genre == "All" else df_tracks[df_tracks['playlist_genre'] == selected_genre]

    # Group by artist and genre, calculate total popularity
    artist_genre_popularity = (
        filtered_df.groupby(['track_artist', 'playlist_genre'], as_index=False)
        .agg({'track_popularity': 'sum'})  # Aggregate popularity by sum
        .rename(columns={'track_popularity': 'total_popularity'})
    )

    # Calculate the total popularity for each genre
    genre_total_popularity = artist_genre_popularity.groupby('playlist_genre')['total_popularity'].transform('sum')

    # Add a percentage column
    artist_genre_popularity['popularity_percentage'] = (artist_genre_popularity['total_popularity'] / genre_total_popularity) * 100

    # Filter the top artists by percentage contribution within the genre
    top_artists = (
        artist_genre_popularity.sort_values(by='popularity_percentage', ascending=False)
        .head(top_artists_count)
    )

    # Create gradient colors for the bars
    color_start = plotly.colors.hex_to_rgb('#d3f9d8')  # Light green
    color_end = plotly.colors.hex_to_rgb('#1DB954')  # Spotify green
    min_percentage = top_artists['popularity_percentage'].min()
    max_percentage = top_artists['popularity_percentage'].max()
    colors = [
        plotly.colors.find_intermediate_color(
            color_start, color_end, (value - min_percentage) / (max_percentage - min_percentage)
        ) for value in top_artists['popularity_percentage']
    ]
    colors_hex = [f"rgb({r},{g},{b})" for r, g, b in colors]

    # Create the bar chart
    fig_barchart = go.Figure(go.Bar(
        x=top_artists['track_artist'],  # Artists on the x-axis
        y=top_artists['popularity_percentage'],  # Percentage on the y-axis
        text=top_artists['popularity_percentage'].round(2),  # Hover text with percentage
        marker=dict(color=colors_hex),  # Gradient color
        hovertemplate="<b>Artist:</b> %{x}<br><b>Genre:</b> %{text}<br><b>Popularity Contribution:</b> %{y:.2f}%<extra></extra>"
    ))

    # Customize the layout
    fig_barchart.update_layout(
        title=dict(
            text=f"Top {top_artists_count} Artists' Popularity Contribution in {selected_genre}",
            font=dict(size=20, color="white"),
            x=0.5,  # Center title
        ),
        xaxis=dict(
            title="Artist",
            tickmode="linear",
            tickangle=-45,  # Rotate artist names for readability
            showgrid=False,
            title_font=dict(size=14, color="white"),
            tickfont=dict(size=12, color="white")
        ),
        yaxis=dict(
            title="Popularity Contribution (%)",
            showgrid=True,
            gridcolor="gray",
            title_font=dict(size=14, color="white"),
            tickfont=dict(size=12, color="white")
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return fig_barchart


#Register the page
dash.register_page(__name__, path="/artist-analysis")