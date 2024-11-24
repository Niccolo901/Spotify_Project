import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

app.title = "Spotify Dashboard"

# Your app layout and callbacks here
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview Historic Dataset", href="/", style={"color": "#1DB954"})),
            dbc.NavItem(dbc.NavLink("Artist Analysis", href="/artist-analysis")),
            dbc.NavItem(dbc.NavLink("Track Analysis", href="/track-analysis")),
            dbc.NavItem(dbc.NavLink("Features Analysis", href="/features-analysis")),
            #dbc.NavItem(dbc.NavLink("Playlist Analysis", href="/playlist-analysis")),
            ],
        brand="Spotify Dashboard",
        color="black",
        dark=True,
        className="mb-4",
    ),
    dash.page_container  # Container to load the current page's layout
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
