import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
import pandas as pd
import plotly.graph_objects as go
import random
import plotly.express as px
import plotly
'''
add the radar charts for comparing features of the genres and features of specific tracks

'''


# Load dataset
df_tracks = pd.read_csv(r'C:\Users\cibei\OneDrive\Desktop\Data Visualization Methods\pythonProject\data\spotify_songs.csv')

# Extract the release year from the release date
df_tracks['release_year'] = pd.to_datetime(df_tracks['track_album_release_date'], errors='coerce').dt.year

# Create a sample dataset for Popularity vs Duration scatterplot
df_sample = df_tracks.sample(n=1000, random_state=42)

# Define a color map for genres
genre_colors = {
    'pop': '#1DB954',
    'rock': '#70D6FF',
    'rap': '#FF9770',
    'latin': '#FF70A6',
    'edm': '#FFD670',
    'r&b': '#FF0000'
}

# Assign colors to genres
df_sample['color'] = df_sample['playlist_genre'].map(genre_colors)



# Available features for the scatterplot
scatter_features = [
    'duration_ms',       # Duration of the track in milliseconds
    'danceability',      # Suitability of the track for dancing
    'energy',            # Intensity and activity level of the track
    'acousticness',      # Likelihood of the track being acoustic
    'valence',           # Musical positivity conveyed by the track
    'liveness',          # Presence of an audience in the recording
    'speechiness',       # Presence of spoken words in the track
    'tempo',             # Speed or pace of the track in beats per minute
    'loudness',          # Overall volume of the track in decibels
    'instrumentalness'   # Absence of vocals in the track
]


# Data processing
# Data processing
energy_danceability = df_tracks.groupby('track_album_release_date')[['energy', 'danceability']].mean().reset_index()

# Get top 10 artists by popularity
top_artists_popularity = (
    df_tracks.groupby('track_artist')
    .agg({'track_popularity': 'mean'})
    .reset_index()
    .sort_values(by='track_popularity', ascending=False)
    .head(10)
)

# Get top 10 genres by popularity
popularity_by_genre = (
    df_tracks.groupby('playlist_genre')
    .agg({'track_popularity': 'mean'})
    .reset_index()
    .sort_values(by='track_popularity', ascending=False)
)

# Generate options for genre dropdown
available_genres = sorted(df_tracks['playlist_genre'].dropna().unique())
genre_dropdown_options = [{"label": "All Genres", "value": "All"}] + \
                         [{"label": genre, "value": genre} for genre in available_genres]


# Group data by genre and count the number of songs
genre_distribution = (
    df_tracks.groupby('playlist_genre', as_index=False)
    .agg({'track_name': 'count'})  # Count the number of songs
    .rename(columns={'track_name': 'num_songs'})  # Rename for clarity
    .sort_values(by='num_songs', ascending=False)  # Sort by number of songs
)


# Scatterplot for Popularity vs Duration using the sample dataset
fig_popularity_duration = go.Figure(go.Scatter(
    x=df_sample['duration_ms'] / 1000,  # Convert duration to seconds
    y=df_sample['track_popularity'],
    mode='markers',
    marker=dict(
        size=8,
        color="#1DB954",
        opacity=0.7,
    ),
    text=df_sample['track_name'],  # Hover text
    hovertemplate="<b>Track Name:</b> %{text}<br><b>Duration (s):</b> %{x}<br><b>Popularity:</b> %{y}<extra></extra>"
))

fig_popularity_duration.update_layout(
    title="Popularity vs Duration of Tracks (Sampled)",
    xaxis_title="Duration (Seconds)",
    yaxis_title="Popularity",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    margin=dict(l=40, r=40, t=50, b=40)
)

# Density plot for Track Duration
fig_duration_density = go.Figure()

fig_duration_density.add_trace(go.Histogram(
    x=df_tracks['duration_ms'] / 1000,  # Convert duration to seconds
    histnorm='probability density',  # Normalize to create a density plot
    marker=dict(
        color="#1DB954",
        opacity=0.7
    ),
    name="Duration (Seconds)",
    xbins=dict(
        start=0,
        end=df_tracks['duration_ms'].max() / 1000,
        size=30  # Bin size in seconds
    ),
))

fig_duration_density.update_layout(
    title="Density Plot of Track Durations",
    xaxis_title="Duration (Seconds)",
    yaxis_title="Density",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    margin=dict(l=40, r=40, t=50, b=40)
)

# Create the bar chart with gradient colors
fig_genre_bar_chart = go.Figure()

# Define gradient colors
color_start = plotly.colors.hex_to_rgb('#d3f9d8')  # Light green
color_end = plotly.colors.hex_to_rgb('#1DB954')  # Spotify green
min_value = genre_distribution['num_songs'].min()
max_value = genre_distribution['num_songs'].max()
colors = [
    plotly.colors.find_intermediate_color(
        color_start, color_end, (value - min_value) / (max_value - min_value)
    ) for value in genre_distribution['num_songs']
]
colors_hex = [f"rgb({r},{g},{b})" for r, g, b in colors]

# Add bars to the chart
fig_genre_bar_chart.add_trace(go.Bar(
    x=genre_distribution['playlist_genre'],  # Genres on the x-axis
    y=genre_distribution['num_songs'],  # Number of songs on the y-axis
    marker=dict(color=colors_hex),  # Gradient color
    text=genre_distribution['num_songs'],  # Display values on the bars
    textposition='auto'  # Position the text in the center of the bars
))

# Customize the layout
fig_genre_bar_chart.update_layout(
    title=dict(
        text="Genre Distribution by Number of Songs",
        font=dict(size=20, color="white"),  # Title font
        x=0.5  # Center the title
    ),
    xaxis=dict(
        title="Genre",
        tickmode="linear",
        tickangle=-45,  # Rotate genre labels
        showgrid=False,
        title_font=dict(size=14, color="white"),  # Style the x-axis title
        tickfont=dict(size=12, color="white")  # Style the x-axis labels
    ),
    yaxis=dict(
        title="Number of Songs",
        showgrid=True,
        gridcolor="gray",
        title_font=dict(size=14, color="white"),  # Style the y-axis title
        tickfont=dict(size=12, color="white")  # Style the y-axis labels
    ),
    plot_bgcolor="black",  # Plot background color
    paper_bgcolor="black",  # Paper background color
    font=dict(color="white")  # General font color
)

# Define layout for Track Analysis page
    # Filter the data based on the selected genre
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Track Analysis", className="text-center", style={"color": "#1DB954", "margin-bottom": "20px"}), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_duration_density,
                                  config={
                                      "displayModeBar": False  # Disables the toolbar
                                  }
                ),
                width=6),
                dbc.Col(dcc.Graph(figure=fig_genre_bar_chart,
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
                        id="genre-selection",
                        options=genre_dropdown_options,
                        value="All",  # Default value
                        className="custom-dropdown"
                    )
                ]), width=6),
                dbc.Col(html.Div([
                    html.Label("Select First Track:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="track-selection-1",
                        options=[],
                        placeholder="Select the first track...",
                        className="custom-dropdown"
                    )
                ]), width=6)
            ],
            className="mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Number of Bars to Display:", style={"color": "#1DB954"}),
                    dcc.Input(
                        id="bar-count-input",
                        type="number",
                        min=1,  # Minimum value
                        value=10,  # Default value
                        className="custom-input",
                        style={"width": "100%"}
                    )
                ]), width=6),
                dbc.Col(html.Div([
                    html.Label("Select Second Track:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="track-selection-2",
                        options=[],
                        placeholder="Select the second track...",
                        className="custom-dropdown"
                    )
                ]), width=6)
            ],
            className="mb-4"
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id="subgenre-bar-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
            ),
            width=6),
            dbc.Col(dcc.Graph(id="track-radar-chart",
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
                    html.Label("Select Feature for X-Axis:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="scatter-feature-dropdown",
                        options=[{"label": feature, "value": feature} for feature in scatter_features],
                        value="duration_ms",  # Default feature
                        className="custom-dropdown",
                    )
                ]), width=6),
                dbc.Col(html.Div([
                    html.Label("Select Highlighted Genres:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="highlight-genres-dropdown",
                        options=[{"label": genre, "value": genre} for genre in available_genres],
                        multi=True,  # Allow multiple selections
                        placeholder="Select genres to highlight...",
                        className="custom-dropdown"
                    )
                ]), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="popularity-scatterplot",
                                  config={
                                      "displayModeBar": False  # Disables the toolbar
                                  }
                ),
                width=12),
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(html.H4("Top 50 Songs by Year (Stacked by Genre)", className="text-center", style={"color": "#1DB954"}), width=12),
                dbc.Col(
                    dcc.RangeSlider(
                        id="year-range-slider",
                        min=int(df_tracks['release_year'].min()),  # Minimum year
                        max=int(df_tracks['release_year'].max()),  # Maximum year
                        step=1,  # Step is 1 year
                        value=[
                            int(df_tracks['release_year'].min()),
                            int(df_tracks['release_year'].max())
                        ],
                        marks={year: str(year) for year in range(
                            int(df_tracks['release_year'].min()),
                            int(df_tracks['release_year'].max()) + 1, 5  # Every 5 years for labels
                        )},
                        className="custom-slider",
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                width=12
                ),
                dbc.Col(
                    dcc.Graph(
                        id="stacked-chart",
                        config={"displayModeBar": False}
                    ),
                    width=12
                )
            ],
            className="mb-4"
        ),
    ],
    fluid=True
)

@dash.callback(
    Output("subgenre-bar-chart", "figure"),
    [Input("genre-selection", "value"),
     Input("bar-count-input", "value")]
)
def update_subgenre_chart(selected_genre, bar_count):
    if selected_genre == "All":
        filtered_df = df_tracks
    else:
        filtered_df = df_tracks[df_tracks['playlist_genre'] == selected_genre]

    # Group by subgenre and count the number of songs
    subgenre_counts = filtered_df['playlist_subgenre'].value_counts().reset_index()
    subgenre_counts.columns = ['Subgenre', 'Number of Songs']

    # Limit the number of bars to display
    subgenre_counts = subgenre_counts.head(bar_count)

    # Define gradient colors
    color_start = plotly.colors.hex_to_rgb('#d3f9d8')  # Spotify green
    color_end = plotly.colors.hex_to_rgb('#1DB954')  # Light green
    min_value = subgenre_counts['Number of Songs'].min()
    max_value = subgenre_counts['Number of Songs'].max()
    colors = [
        plotly.colors.find_intermediate_color(
            color_start, color_end, (value - min_value) / (max_value - min_value)
        ) for value in subgenre_counts['Number of Songs']
    ]
    colors_hex = [f"rgb({r},{g},{b})" for r, g, b in colors]

    # Create the bar chart
    fig = go.Figure(go.Bar(
        x=subgenre_counts['Subgenre'],
        y=subgenre_counts['Number of Songs'],
        marker=dict(color=colors_hex),  # Gradient color
        text=subgenre_counts['Number of Songs'],  # Display values on the bars
        textposition='auto'  # Position the text in the center of the bars
    ))

    # Update layout for the chart
    fig.update_layout(
        title="Subgenre Distribution by Number of Songs",
        xaxis_title="Subgenre",
        yaxis_title="Number of Songs",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(categoryorder="total descending", tickangle=-45)  # Order bars by value and rotate labels
    )

    return fig

# Callbacks for updating track options and radar chart
@dash.callback(
    [Output("track-selection-1", "options"),
     Output("track-selection-2", "options")],
    Input("genre-selection", "value")
)
def update_track_options(selected_genre):
    # Filter tracks based on selected genre
    if selected_genre == "All":
        filtered_tracks = df_tracks
    else:
        filtered_tracks = df_tracks[df_tracks['playlist_genre'] == selected_genre]

    # Ensure each track has a unique and valid label and value
    track_options = [{"label": str(track), "value": str(track)} for track in filtered_tracks['track_name'].dropna().unique()]

    return track_options, track_options


# Callback to update radar chart based on selected tracks
@dash.callback(
    Output("track-radar-chart", "figure"),
    [Input("track-selection-1", "value"),
     Input("track-selection-2", "value")]
)
def update_radar_chart(track_1, track_2):
    if not track_1 or not track_2:
        return go.Figure()

    # Radar chart attributes
    attributes = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

    # Normalize the attributes to a range of 0–1
    normalized_data = df_tracks.copy()
    for attr in attributes:
        min_val = df_tracks[attr].min()
        max_val = df_tracks[attr].max()
        normalized_data[attr] = (df_tracks[attr] - min_val) / (max_val - min_val)

    # Filter normalized data for selected tracks
    track_1_data = normalized_data[normalized_data['track_name'] == track_1][attributes].mean()
    track_2_data = normalized_data[normalized_data['track_name'] == track_2][attributes].mean()

    # Ensure data exists for both tracks
    if track_1_data.isnull().all() or track_2_data.isnull().all():
        return go.Figure()

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=track_1_data,
        theta=attributes,
        fill='toself',
        name=track_1,
        marker=dict(color="#1DB954")
    ))

    fig.add_trace(go.Scatterpolar(
        r=track_2_data,
        theta=attributes,
        fill='toself',
        name=track_2,
        marker=dict(color="#FFD670")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])  # Normalized range
        ),
        showlegend=True,
        title="Track Feature Comparison",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    return fig



# Callback to update the scatterplot based on selected feature
@dash.callback(
    Output("popularity-scatterplot", "figure"),
    [Input("scatter-feature-dropdown", "value"),
     Input("highlight-genres-dropdown", "value")]  # Input for selected genres
)
def update_scatterplot(selected_feature, selected_genres):
    # X-axis label
    x_label = "Duration (Seconds)" if selected_feature == "duration_ms" else selected_feature.capitalize()

    # Prepare the x values
    if selected_feature == "duration_ms":
        x_values = df_sample[selected_feature] / 1000  # Convert duration to seconds
    else:
        x_values = df_sample[selected_feature]

    # Determine which points to highlight
    highlighted = df_sample['playlist_genre'].isin(selected_genres) if selected_genres else [True] * len(df_sample)

    # Create scatterplot
    fig = go.Figure()

    # Add main scatterplot with conditional styling
    fig.add_trace(go.Scatter(
        x=x_values,
        y=df_sample['track_popularity'],
        mode='markers',
        marker=dict(
            size=[8 if h else 6 for h in highlighted],  # Larger size for highlighted points
            color=df_sample['color'],  # Use the color column for marker colors
            opacity=[1 if h else 0.5 for h in highlighted],  # Full opacity for highlighted points
            line=dict(width=0)
        ),
        text=df_sample['track_name'],  # Hover text
        hovertemplate="<b>Track Name:</b> %{text}<br><b>" + x_label + ":</b> %{x}<br><b>Popularity:</b> %{y}<extra></extra>",
        showlegend=False  # Hide this trace from the legend
    ))

    # Add dummy traces for legend
    unique_colors = df_sample[['playlist_genre', 'color']].drop_duplicates()
    for _, row in unique_colors.iterrows():
        fig.add_trace(go.Scatter(
            x=[None],  # No actual points
            y=[None],  # No actual points
            mode='markers',
            marker=dict(size=10, color=row['color']),
            name=row['playlist_genre']  # Genre name as the legend label
        ))

    # Update layout
    fig.update_layout(
        title=f"Popularity vs {x_label}",
        xaxis_title=x_label,
        yaxis_title="Popularity",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


 # Callback to update the stacked bar chart based on selected genre and year range
@dash.callback(
    Output("stacked-chart", "figure"),
    [Input("genre-selection", "value"),
     Input("year-range-slider", "value")]
)
def update_stacked_chart(selected_genre, selected_years):
    # Filter data by genre (optional)
    filtered_df = df_tracks.copy()
    if selected_genre != "All":
        filtered_df = filtered_df[filtered_df['playlist_genre'] == selected_genre]

    # Use release_year for year range filtering
    start_year, end_year = selected_years
    filtered_df = filtered_df[(filtered_df['release_year'] >= start_year) & (filtered_df['release_year'] <= end_year)]

    # Ensure valid years and filter top 50 songs by year
    top_songs_per_year = (
        filtered_df.groupby('release_year', group_keys=False)
        .apply(lambda x: x.nlargest(50, 'track_popularity'))
    )

    # Count the number of songs by genre for each year
    genre_distribution = (
        top_songs_per_year.groupby(['release_year', 'playlist_genre'])
        .size()
        .reset_index(name='count')
    )

    # Pivot to create data for stacking
    stacked_data = genre_distribution.pivot(index='release_year', columns='playlist_genre', values='count').fillna(0)

    # Create the stacked bar chart
    fig = go.Figure()
    for genre in stacked_data.columns:
        fig.add_trace(go.Bar(
            x=stacked_data.index,
            y=stacked_data[genre],
            name=genre,
            hovertemplate=f"<b>Genre:</b> {genre}<br><b>Count:</b> {{y}}<extra></extra>"
        ))

    # Update layout
    fig.update_layout(
        barmode='stack',
        title="Top 50 Songs by Year (Stacked by Genre)",
        xaxis_title="Year",
        yaxis_title="Number of Songs",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(
            title="Genres",
            x=1.05,
            y=1,
            bordercolor="gray",
            borderwidth=1
        )
    )

    return fig



#Register the page
dash.register_page(__name__, path="/track-analysis")

