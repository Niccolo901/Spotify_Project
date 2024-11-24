import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

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
            dbc.Col(dcc.Graph(id="trend-line-chart"), width=12),
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
            dbc.Col(dcc.Graph(id="comparison-radar-chart"), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="comparison-bar-chart"), width=12),
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

    # Create the line chart
    fig = go.Figure()

    for feature in selected_features:
        fig.add_trace(go.Scatter(
            x=avg_features_by_year['release_year'],
            y=avg_features_by_year[feature],
            mode='lines+markers',
            name=feature.capitalize(),
            line=dict(width=2),
            marker=dict(size=6)
        ))

    fig.update_layout(
        title="Feature Trends Over the Years",
        xaxis_title="Year",
        yaxis_title="Average Value",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(
            x=0.01, y=0.99,
            bordercolor="white",
            borderwidth=1,
            bgcolor="rgba(0,0,0,0.5)"
        )
    )

    return fig

# Callback to update Mode and Valence distribution charts (optional functionality)
@dash.callback(
    [Output("mode-distribution-chart", "figure"),
     Output("valence-distribution-chart", "figure")],
    Input("trend-feature-dropdown", "value")  # Use dropdown interaction to refresh distribution
)
def update_distribution_charts(_):
    # Mode distribution
    mode_distribution = (
        df_tracks.groupby('track_name', as_index=False)
        .agg({'mode': 'mean'})
        .sort_values(by='mode', ascending=False)
        .head(10)
    )
    fig_mode_distribution = go.Figure(go.Bar(
        x=mode_distribution['mode'],
        y=mode_distribution['track_name'],
        orientation='h',
        marker_color="#1DB954"
    ))
    fig_mode_distribution.update_layout(
        title="Distribution of Track over Mode",
        xaxis_title="Mode",
        yaxis_title="Track",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    # Valence distribution
    valence_distribution = (
        df_tracks.groupby('track_name', as_index=False)
        .agg({'valence': 'mean'})
        .sort_values(by='valence', ascending=False)
        .head(10)
    )
    fig_valence_distribution = go.Figure(go.Bar(
        x=valence_distribution['valence'],
        y=valence_distribution['track_name'],
        orientation='h',
        marker_color="#1DB954"
    ))
    fig_valence_distribution.update_layout(
        title="Distribution of Track over Valence",
        xaxis_title="Valence",
        yaxis_title="Track",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return fig_mode_distribution, fig_valence_distribution

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

# Callback to update radar and bar charts based on selected items
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

    # Radar Chart
    radar_chart = go.Figure()
    for _, row in avg_features.iterrows():
        radar_chart.add_trace(go.Scatterpolar(
            r=row[comparison_features].values,
            theta=comparison_features,
            fill='toself',
            name=row[group_col],
            opacity=0.7
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

    # Bar Chart
    bar_chart = go.Figure()
    for feature in comparison_features:
        bar_chart.add_trace(go.Bar(
            x=avg_features[group_col],
            y=avg_features[feature],
            name=feature
        ))
    bar_chart.update_layout(
        barmode="group",
        title="Feature Comparison (Bar Chart)",
        xaxis_title=group_col.capitalize(),
        yaxis_title="Average Feature Value",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return radar_chart, bar_chart



#Register the page
dash.register_page(__name__, path="/features-analysis")