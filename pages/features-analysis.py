import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly

# Load dataset
df_tracks = pd.read_csv(r'C:\Users\cibei\OneDrive\Desktop\Data Visualization Methods\pythonProject\data\spotify_songs.csv')

# Ensure the release date is in datetime format
df_tracks['track_album_release_date'] = pd.to_datetime(df_tracks['track_album_release_date'], errors='coerce')
df_tracks['release_year'] = df_tracks['track_album_release_date'].dt.year

# Ensure genres and subgenres are strings
df_tracks['playlist_genre'] = df_tracks['playlist_genre'].astype(str)
df_tracks['playlist_subgenre'] = df_tracks['playlist_subgenre'].astype(str)

# Features for comparison
comparison_features = ['danceability', 'energy', 'acousticness', 'valence', 'liveness', 'speechiness']

# Get unique genres and subgenres
unique_genres = sorted(df_tracks['playlist_genre'].unique())
unique_subgenres = sorted(df_tracks['playlist_subgenre'].unique())


# Features available for plotting trends
trend_features = [
    {"label": "Danceability", "value": "danceability"},
    {"label": "Energy", "value": "energy"},
    {"label": "Acousticness", "value": "acousticness"},
    {"label": "Valence", "value": "valence"},
    {"label": "Liveness", "value": "liveness"},
    {"label": "Speechiness", "value": "speechiness"},
    {"label": "Tempo", "value": "tempo"},
    {"label": "Loudness", "value": "loudness"},
    {"label": "Instrumentalness", "value": "instrumentalness"}
]

# Define layout for Feature Analysis page
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Audio Features Analysis", className="text-center", style={"color": "#1DB954", "margin-bottom": "20px"}), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Select Features to Plot:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="trend-feature-dropdown",
                        options=trend_features,
                        value=["danceability"],  # Default feature
                        multi=True,
                        className="custom-dropdown"
                    )
                ]), width=12)
            ],
            className="mb-4",
            style={"backgroundColor": "black"}
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="trend-line-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
            ), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(html.H2("Compare Genres And Subgenres", className="text-center", style={"color": "#1DB954"}), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.Label("Select Categories to Compare:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=[
                            {"label": "Genres", "value": "genre"},
                            {"label": "Subgenres", "value": "subgenre"}
                        ],
                        value="genre",  # Default to genres
                        className="custom-dropdown"
                    )
                ]), width=6),
                dbc.Col(html.Div([
                    html.Label("Select Items to Compare:", style={"color": "#1DB954"}),
                    dcc.Dropdown(
                        id="item-dropdown",
                        multi=True,  # Allow multiple selection
                        placeholder="Select genres or subgenres...",
                        className="custom-dropdown"
                    )
                ]), width=6)
            ],
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="comparison-radar-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
            ), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="comparison-bar-chart",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
            ), width=12),
            className="mb-4"
        ),
dbc.Row(
        [
            dbc.Col(html.Div([
                html.Label("Select X-axis Feature:", style={"color": "#1DB954"}),
                dcc.Dropdown(
                    id="scatter-x-feature-dropdown",
                    options=trend_features,
                    value="danceability",  # Default feature
                    className="custom-dropdown"
                )
            ]), width=6),
            dbc.Col(html.Div([
                html.Label("Select Y-axis Feature:", style={"color": "#1DB954"}),
                dcc.Dropdown(
                    id="scatter-y-feature-dropdown",
                    options=trend_features,
                    value="energy",  # Default feature
                    className="custom-dropdown"
                )
            ]), width=6)
        ],
        className="mb-4",
        style={"backgroundColor": "black"}
    ),
    dbc.Row(
            dbc.Col(dcc.Graph(id="feature-scatterplot",
                              config={
                                  "displayModeBar": False  # Disables the toolbar
                              }
            ), width=12),
            className="mb-4"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div([
                html.Label("Select Genre:", style={"color": "#1DB954"}),
                dcc.Dropdown(
                    id="genre-selection",
                    options=[{"label": genre, "value": genre} for genre in unique_genres] + [{"label": "All", "value": "All"}],
                    value="All",  # Default to "All"
                    className="custom-dropdown"
                )
            ]), width=12)
        ],
        className="mb-4"
    ),

    dbc.Row(
        [
            dbc.Col(html.H4("Parallel Coordinates Chart", className="text-center", style={"color": "#1DB954"}),
                    width=12),
            dbc.Col(
                dcc.Graph(
                    id="parallel-coordinates-chart",
                    config={"displayModeBar": False}
                ),
                width=12
            )
        ],
        className="mb-4"
    )

    ],
    fluid=True
)

# Callback to update the trend line chart based on selected features
@dash.callback(
    Output("trend-line-chart", "figure"),
    Input("trend-feature-dropdown", "value")
)
def update_trend_line_chart(selected_features):
    if not selected_features:
        return go.Figure()

    # Group data by year and calculate average for selected features
    avg_features_by_year = df_tracks.groupby('release_year')[selected_features].mean().reset_index()

    # Define the colors for the lines
    colors = ['#1DB954', '#70D6FF', '#FF9770', '#FF70A6', '#FFD670', '#FF0000']

    # Create the line chart
    fig = go.Figure()

    for i, feature in enumerate(selected_features):
        fig.add_trace(go.Scatter(
            x=avg_features_by_year['release_year'],
            y=avg_features_by_year[feature],
            mode='lines+markers',
            name=feature.capitalize(),
            line=dict(width=2, color=colors[i % len(colors)]),
            marker=dict(size=6)
        ))

    fig.update_layout(
        title="Feature Trends Over the Years",
        xaxis_title="Year",
        yaxis_title="Average Value",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        yaxis=dict(range=[0, 1]),
        legend=dict(
            x=0.01, y=0.99,
            bordercolor="white",
            borderwidth=1,
            bgcolor="rgba(0,0,0,0.5)"
        )
    )

    return fig


# Callback to update item dropdown based on category selection
@dash.callback(
    Output("item-dropdown", "options"),
    Input("category-dropdown", "value")
)
def update_item_dropdown(category):
    if category == "genre":
        return [{"label": genre, "value": genre} for genre in unique_genres]
    elif category == "subgenre":
        return [{"label": subgenre, "value": subgenre} for subgenre in unique_subgenres]
    return []

# Callback to update radar and grouped bar charts based on selected items
@dash.callback(
    [Output("comparison-radar-chart", "figure"),
     Output("comparison-bar-chart", "figure")],
    [Input("category-dropdown", "value"),
     Input("item-dropdown", "value")]
)
def update_comparison_charts(category, selected_items):
    if not selected_items:
        return go.Figure(), go.Figure()

    # Filter data based on selected items
    if category == "genre":
        filtered_data = df_tracks[df_tracks['playlist_genre'].isin(selected_items)]
        group_col = 'playlist_genre'
    elif category == "subgenre":
        filtered_data = df_tracks[df_tracks['playlist_subgenre'].isin(selected_items)]
        group_col = 'playlist_subgenre'
    else:
        return go.Figure(), go.Figure()

    # Calculate averages for each selected item
    avg_features = (
        filtered_data.groupby(group_col)[comparison_features].mean().reset_index()
    )

    # Define the colors for the charts
    colors = ['#1DB954', '#70D6FF', '#FF9770', '#FF70A6', '#FFD670', '#FF0000']

    # Radar Chart
    radar_chart = go.Figure()
    for i, row in avg_features.iterrows():
        radar_chart.add_trace(go.Scatterpolar(
            r=row[comparison_features].values,
            theta=comparison_features,
            fill='toself',
            name=row[group_col],
            opacity=0.7,
            line=dict(color=colors[i % len(colors)])
        ))
    radar_chart.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])  # Normalize to 0–1
        ),
        title="Feature Comparison (Radar Chart)",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    # Grouped Bar Chart
    bar_chart = go.Figure()
    for i, genre in enumerate(selected_items):
        for j, feature in enumerate(comparison_features):
            show_legend = j == 0  # Show legend only for the first feature of each genre
            bar_chart.add_trace(go.Bar(
                x=[feature],
                y=[avg_features[avg_features[group_col] == genre][feature].values[0]],
                name=genre if show_legend else None,
                marker=dict(color=colors[i % len(colors)]),
                offsetgroup=i,
                showlegend=show_legend
            ))
    bar_chart.update_layout(
        barmode="group",
        title="Feature Comparison (Grouped Bar Chart)",
        xaxis_title="Features",
        yaxis_title="Average Feature Value",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return radar_chart, bar_chart


# Define a color map for genres
genre_color_map = {
    'pop': '#1DB954',
    'r&b': '#70D6FF',
    'rap': '#FF9770',
    'latin': '#FF70A6',
    'edm': '#FFD670',
    'rock': '#FF0000'
}



# Callback to update the scatterplot based on selected features
@dash.callback(
    Output("feature-scatterplot", "figure"),
    [Input("scatter-x-feature-dropdown", "value"),
     Input("scatter-y-feature-dropdown", "value")]
)
def update_feature_scatterplot(x_feature, y_feature):
    # Sample 1000 songs from the dataset
    df_sample = df_tracks.sample(n=1000, random_state=42)

    # Map genres to colors
    df_sample['color'] = df_sample['playlist_genre'].map(genre_color_map)

    # Create scatterplot
    fig = go.Figure()

    # Add scatter plot trace
    fig.add_trace(go.Scatter(
        x=df_sample[x_feature],
        y=df_sample[y_feature],
        mode='markers',
        marker=dict(
            size=8,
            color=df_sample['color'],  # Use the mapped color column for marker colors
            opacity=0.7
        ),
        text=df_sample['track_name'],  # Hover text
        hovertemplate="<b>Track Name:</b> %{text}<br><b>" + x_feature.capitalize() + ":</b> %{x}<br><b>" + y_feature.capitalize() + ":</b> %{y}<extra></extra>",
        showlegend=False
    ))

    # Add dummy traces for legend
    for genre, color in genre_color_map.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=8, color=color),
            legendgroup=genre,
            showlegend=True,
            name=genre
        ))

    fig.update_layout(
        title=f"{x_feature.capitalize()} vs {y_feature.capitalize()}",
        xaxis_title=x_feature.capitalize(),
        yaxis_title=y_feature.capitalize(),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig

@dash.callback(
    Output("parallel-coordinates-chart", "figure"),
    Input("genre-selection", "value")
)
def update_parallel_coordinates(selected_genre):
    # Filter data by selected genre
    if selected_genre == "All":
        filtered_df = df_tracks.copy()
    else:
        filtered_df = df_tracks[df_tracks['playlist_genre'] == selected_genre]

    # Select relevant attributes for the chart
    attributes = ['danceability', 'energy', 'valence', 'liveness', 'speechiness', 'instrumentalness', 'track_popularity']
    filtered_df = filtered_df[attributes]

    # Remove rows with NaN or invalid values
    filtered_df = filtered_df.dropna()

    # Check if data is empty
    if filtered_df.empty:
        return go.Figure(layout=dict(
            title="No Data Available for Selected Genre",
            font=dict(color="white"),
            paper_bgcolor="black",
            plot_bgcolor="black"
        ))

    # Normalize attributes for better visualization (range 0–1)
    normalized_df = filtered_df.copy()
    for attr in attributes:
        min_val = filtered_df[attr].min()
        max_val = filtered_df[attr].max()
        if min_val == max_val:
            normalized_df[attr] = 1  # Handle cases where all values are identical
        else:
            normalized_df[attr] = (filtered_df[attr] - min_val) / (max_val - min_val)

    # Create the parallel coordinates chart
    dimensions = [
        dict(range=[0, 1], label=attr.capitalize(), values=normalized_df[attr]) for attr in attributes
    ]

    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=filtered_df['track_popularity'],
            colorscale='Viridis',
            showscale=True  # Show color scale
        ),
        dimensions=dimensions
    ))

    fig.update_layout(
        title="Parallel Coordinates Chart",
        font=dict(color="white"),
        paper_bgcolor="black",
        plot_bgcolor="black"
    )

    return fig




#Register the page
dash.register_page(__name__, path="/features-analysis")