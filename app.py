from flask import Flask, render_template, g, url_for, redirect, request
import mysql.connector

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass",
        port = 3333
        )
        return g.db
    
    else:
        return g.db

def execute_query(query, q_type = 'select'):
    try:
        mydb = get_db()
        with mydb.cursor() as curr:
            curr.execute(query)

            if q_type == "CRUD":
                mydb.commit()
            resp = curr.fetchall()

        return resp

    except Exception as e:
        print("an exception occured:")
        s = f"%s: %s" % (type(e).__name__,e)
        print(s)
        return s

@app.route("/")
def home():
    query = "select * from `sys`.`customer_table`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('index.html',customers = resp)

@app.route("/insert")
def insert():
    query = "select * from `sys`.`customer_table`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('insert.html',customers = resp)

@app.route("/delete")
def delete():
    query = "select * from `sys`.`customer_table`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('delete.html',customers = resp)

@app.route("/insert_form",methods=["POST"])
def insert_form():
    customer_id = request.form['customer_id']
    customer_name = request.form['customer_name']
    customer_type = request.form['customer_type']
    date_time = request.form['date_time']

    query = f"insert into `sys`.`customer_table` values (%d,'%s','%s','%s:00');" % (int(customer_id),customer_name,customer_type,' '.join(date_time.split('T')))
    resp = execute_query(query,q_type="CRUD")

    if isinstance(resp, str):
        return resp
    else:
        return redirect('/')
    
@app.route("/delete_form",methods=["POST"])
def delete_form():
    filters = []

    for k,v in request.form.items():
        if v == '':
            continue
            
        if k == 'customer_id':
            filters.append(k+" = "+v)
        else:
            filters.append(k+" = '"+v+"'")

    query = f"delete from `sys`.`customer_table` where %s;" % (' and '.join(filters))
    print(query)
    resp = execute_query(query,q_type="CRUD")

    if isinstance(resp, str):
        return resp
    else:
        return redirect('/')