from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass",
        port = 3333
        )

        curr = mydb.cursor()

    except Exception as e:
        print(e)
        return str(e)
    curr.execute("select * from `sys`.`customer_table`;")
    resp = curr.fetchall()
    return render_template('index.html',customers = resp)

def display():
    pass