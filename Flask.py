from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Link to database MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['News']
collection = db['NewsAndLink']

@app.route('/')
def index():
    data = collection.find()  # Find all data from Database into variable data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)