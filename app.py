from flask import Flask,  render_template, request
from datetime import datetime
import sqlite3
import csv
import os


app = Flask(__name__)

dete = datetime.now().strftime('%d-%m-%Y')


@app.route("/")
def home():
    with sqlite3.connect("database.db") as connect:
        cursor = connect.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, Titel TEXT, Amount INTEGER, Category TEXT, Date INTEGER )')
        file_exists = os.path.exists('data.csv')
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Title', 'Amount', 'Category', 'Date'])
    return render_template('home.html')


@app.route("/add", methods=["POST", 'GET'])
def add():
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')
    if not title or not amount or not category:
        return "felier"
    else:
        with sqlite3.connect("database.db") as connect:
            cursor = connect.cursor()
            cursor.execute('INSERT INTO Expenses(Titel, Amount, Category, dete) VALUES (?, ?, ?, ?)',
                       (title, amount, category, dete))
        with open('data.csv', 'w') as f:
            f.write(f"{title}, {amount:.2f}, {category}, {dete}")
        return "Expenses Added sucssesfuly"


@app.route("/view")
def view():
    view = cursor.execute('SELECT * FROM Expenses')
    v = [row[0] for row in view.fetchall()]
    return render_template('view.html', view=v)


if __name__ == '__main__':
    app.run(debug=True)
