from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối tới cơ sở dữ liệu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['News']
collection = db['NewsAndLink']

@app.route('/tiente')
def index():
    data = collection.find()  # Truy vấn tất cả dữ liệu từ collection
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)