from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Replace with your API key
API_KEY = "2f2c69d11da6fbec145966359891dd84"

# Database Model
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        # Save search history
        new_search = SearchHistory(city=city)
        db.session.add(new_search)
        db.session.commit()

        # Weather API URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather = {
                "city": city,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "description": data["weather"][0]["description"]
            }

    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)