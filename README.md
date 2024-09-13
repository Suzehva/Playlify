# Playlify
Playlify creates a playlist with a hidden message: the titles of all the songs in the playlist form a sentence.

# Setup
To manage dependencies, we recommend using a Python venv. First, ensure that you have Python installed (see https://cloud.google.com/python/docs/setup).

Then, set up a venv and install the required dependencies using pip within the environment.
```bash
cd playlify/
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
# Running
To run Playlify, make sure you are in the parent directory of playlify and run:
```bash
python -m playlify.main
```
You should see a link pop up in your terminal where Playlify will now be hosted. Enjoy making playlists!

# Developer details
You can add songs to the common_songs.txt with the instructions in uri_finder.py
