# **Spotify Dashboard**

### **Project Overview**
The **Spotify Dashboard** is an interactive web application built using Dash and Plotly that allows users to analyze Spotify music data. The application provides detailed insights into tracks, artists, genres, and features through dynamic visualizations such as bar charts, line graphs, radar charts, and interactive tables.

---

## **Features**

### 1. **Overview Page**
   - High-level metrics such as:
     - Total number of tracks and artists.
     - Average track popularity and duration.
   - Interactive bar charts showing the number of songs released per year.
   - A dynamic table displaying the top tracks by popularity.

### 2. **Artist Analysis Page**
   - Bar charts visualizing:
     - Top 10 artists based on average popularity.
     - Top 10 genres based on popularity.
   - Interactive radar chart comparing features (e.g., danceability, energy) of two selected artists.
   - A table showing the most popular artists filtered by genre and minimum track count.
   - A dynamic bar chart showing the percentage contribution of artists' popularity within a genre.

---

## **Technologies Used**
- **Python 3.8+**: Backend logic.
- **Dash**: Web framework for interactive visualization.
- **Plotly**: For creating charts and visualizations.
- **Pandas**: Data processing and aggregation.
- **Dash Bootstrap Components**: For clean and responsive UI using Bootstrap styling.

---

## **Project Structure**

The project follows a modular design with separate pages for different features.

```plaintext
pythonProject/
│
├── assets/                          # Static assets (CSS, fonts, images, etc.)
│   ├── circular-std-medium.woff2    # Example font file
│   └── styles.css                   # Custom CSS styling for the Dash app
│
├── data/                            # Data files
│   └── spotify_songs.csv            # Main dataset file
│
├── pages/                           # Page-specific layouts and callbacks
│   ├── artist_analysis.py           # Artist Analysis page
│   ├── features_analysis.py         # Features Analysis page
│   ├── overview.py                  # Overview page
│   └── track_analysis.py            # Track Analysis page
│
├── pyproject.toml                   # Requirements and dependencies
├── .gitignore                       # List of files to ignore (e.g., .cache, data backups)
├── LICENSE                          # License information for the project
├── README.md                        # Project documentation
├── requirements.txt                 # List of required Python libraries
└── app.py                           # Main application file (entry point)

```
---
# Setup Instructions
Follow these steps to run the application locally:

### 1.  Clone the Repository
```plaintext
git clone https://github.com/your-username/spotify-dashboard.git
cd spotify-dashboard
```
### 2. Install Dependencies Using Poetry
Ensure you have Python 3.12 installed and Poetry set up. If Poetry is not installed, install it with:

```plaintext
pip install poetry
```

Install the required project dependencies:


```plaintext
poetry install
```
This will:

- Set up a virtual environment.
- Install all dependencies as defined in the pyproject.toml.

### 3. Prepare the Dataset
Ensure the dataset spotify_songs.csv is placed inside the data/ directory.

### 4. Run the Application
Start the Dash server:

```plaintext
python app.py
```
### 5. Open the Dashboard
Navigate to http://127.0.0.1:8050/ in your browser.

# How to Use
### Navigation
Use the Navigation Bar to switch between pages:
- Overview: Summary metrics and yearly song trends.
- Artist Analysis: Insights into artists, genres, and artist comparisons.
- Track Analysis: In-depth exploration of tracks (coming soon).
- Features Analysis: Audio features trends and comparisons (coming soon).

### Key Interactions
- Dropdowns: Select genres, years, or artists to filter data.
- Sliders: Adjust year ranges for line charts.
- Interactive Charts: Hover over bars and points for detailed information.
- Tables: View dynamically filtered top tracks or artists.

--- 
# Dataset
The dataset spotify_songs.csv contains the following columns:

- track_name: Name of the track.

- track_artist: Artist(s) who performed the track.

- track_popularity: Track's popularity score (0-100).

- track_album_name: Album name.

- track_album_release_date: Release date of the album.

- playlist_genre: Playlist genre.

- playlist_subgenre: Playlist sub-genre.

- danceability, energy, valence: Audio features scaled from 0 to 1.

- duration_ms: Duration of the track in milliseconds.

---

# Future Enhancements
- Add Track Analysis page with scatterplots and feature analysis.

- Add Features Analysis for comparing audio features across genres and years.

- Improve performance for larger datasets.

---
# Contributing
Contributions are welcome!

1. Fork the repository.
2. Create a new branch:

```plaintext
git checkout -b feature/your-feature
```

3. Commit your changes.
4. Open a pull request.
License
This project is licensed under the MIT License.

--- 

# Contact
- Author: Niccolo' Cibei
- Email: cibeiniccolo@gmail.com