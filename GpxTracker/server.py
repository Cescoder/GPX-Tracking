from flask import Flask, request, render_template, jsonify
import gpxpy
import gpxpy.gpx

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/home')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

    
