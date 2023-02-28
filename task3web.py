from flask import Flask, render_template, request
from task3 import allss
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['POST'])
def map():
    artist_name = request.form['artist_name']
    data = allss(artist_name)
    return render_template('Spotify.html', data = data)

if __name__ == '__main__':
    app.run(debug=True, port = 8888)
