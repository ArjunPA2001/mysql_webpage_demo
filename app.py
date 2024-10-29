from flask import Flask, render_template, g, url_for, redirect, request
import mysql.connector

app = Flask(__name__)

schema = {"customer_table":{"customer_id":{"type":"number"},
                            "customer_name":{"type":"text","maxlength":45},
                            "customer_type":{"type":"text","maxlength":1,"placeholder":"Please enter one character"},
                            "date_time":{"type":"datetime-local"}},
          "orders":{"order_id":{"type":"number"},
                    "customer_id":{"type":"number"},
                    "order_date":{"type":"datetime-local"},
                    "amount":{"type":"number"}}}

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
    return redirect("/display/customer_table")
    
@app.route("/display/<table_name>")
def display(table_name):
    query = "select * from `sys`.`"+ table_name +"`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('display.html',values = resp, table_name = table_name, schema = schema[table_name])

@app.route("/insert/<table_name>")
def insert(table_name):
    query = "select * from `sys`.`"+ table_name +"`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('insert.html',values = resp, table_name = table_name, schema = schema[table_name])

@app.route("/delete/<table_name>")
def delete(table_name):
    query = "select * from `sys`.`"+ table_name +"`;"
    resp = execute_query(query)

    if isinstance(resp, str):
        return resp
    else:
        return render_template('delete.html',values = resp, table_name = table_name, schema = schema[table_name])

@app.route("/insert_form/<table_name>",methods=["POST"])
def insert_form(table_name):
    columns = {}
    strings = []
    for column,args in schema[table_name].items():
        columns[column] = request.form[column]
        if args["type"] == "number":
            strings.append(request.form[column])
        elif args["type"] == "text":
            strings.append("'" + request.form[column] + "'")
        elif args["type"] == "datetime-local":
            strings.append("'" + ' '.join(request.form[column].split('T')) + ":00'")
    string = ", ".join(strings)

    query = f"insert into `sys`.`%s` values (%s);" % (table_name,string)
    resp = execute_query(query,q_type="CRUD")

    if isinstance(resp, str):
        return resp
    else:
        return redirect(url_for('display', table_name = table_name))
    
@app.route("/delete_form",methods=["POST"])
def delete_form():
    filters = []

    for k,v in request.form.items():
        if v == '':
            continue
            
        if k == 'customer_id' or k == 'order_id':
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