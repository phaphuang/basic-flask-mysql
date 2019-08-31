from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
import json
import collections
import os

conn=pymysql.connect(host="localhost",user="root",password="",db="transaction_prototype")
c=conn.cursor()

DATA_DIR = 'static/uploads'

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route('/')
def main():
    return render_template('menus.html')

@app.route('/createForm')
def createform():
    return render_template('insert.html')

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method=='POST':
        name1=request.form['t_name']
        c.execute("""INSERT into master(first_name, last_name,balance) VALUES (%s,%s,%s)""",(name1,request.form['t_lname'],request.form['t_balance']))
        conn.commit()
        return redirect(url_for('disp', name=name1))

@app.route('/disp/<name>')
def disp(name):
    return render_template("insert_success.html",name=name)

@app.route('/listForm')
def select():
    c.execute("SELECT * from master")
    data=c.fetchall()
    return render_template('show.html', data=data)

@app.route('/update', methods=['POST', 'GET'])
def update_detail():
    if request.method=='POST':
        update_data = request.form['upid']
        query="SELECT * from master WHERE id=%s"
        param=update_data
        c.execute(query, param)
        fetch_data=c.fetchall()
        return render_template('show_update.html', data=fetch_data)

@app.route('/update_det', methods=['POST', 'GET'])
def details_update():
    if request.method=='POST':
        id=request.form['uid']
        fname=request.form['fname']
        lname=request.form['lname']
        balance=request.form['balance']
        query="UPDATE master SET first_name=%s, last_name=%s, balance=%s WHERE id=%s"
        par=(fname, lname, balance, id)
        c.execute(query,par)
        conn.commit()

        return render_template('update_success.html', name=fname)

@app.route('/delete', methods=['POST', 'GET'])
def delete_data():
    if request.method=='POST':
        delete_id = request.form['delid']
        query = "DELETE FROM master WHERE id=%s"
        c.execute(query, delete_id)
        conn.commit()
        return render_template("delete_success.html", id=delete_id)

@app.route('/makeTransaction')
def make_transaction():
    return render_template('make_transaction.html')

@app.route('/makeDeposit')
def make_deposit():
    return render_template('make_deposit.html')

#### src: https://www.datasciencelearner.com/python-ajax-json-request-form-flask/
@app.route('/deposit', methods=['POST', 'GET'])
def deposit():
    if request.method=='POST':
        depid = request.form['uid']
        amount = request.form['amount']
        query="SELECT id, balance from master WHERE id=%s"
        param=depid
        c.execute(query, param)
        result = c.fetchone()
        if (len(result) > 0) and (int(amount) >= 0):
            qid=result[0]
            oldbalance=result[1]
            update_query="UPDATE master SET balance=%s WHERE id=%s"
            newbalance = str(int(oldbalance) + int(amount))
            par=(newbalance, qid)
            c.execute(update_query,par)
            insert_query="INSERT INTO transaction(user_id, prev_amount, curr_amount, action_id, amount) VALUES (%s,%s,%s,%s,%s)"
            insert_param = (qid, oldbalance, newbalance, "02", amount)
            c.execute(insert_query, insert_param)
            conn.commit()
            return jsonify({'output': newbalance})
        else:
            return jsonify({'error': 'Invalid input'})

@app.route("/makeWithdraw")
def make_withdraw():
    return render_template('make_withdraw.html')

@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    if request.method=='POST':
        depid = request.form['uid']
        amount = request.form['amount']
        query="SELECT id, balance from master WHERE id=%s"
        param=depid
        c.execute(query, param)
        result = c.fetchone()
        if (len(result) > 0) and (int(amount) >= 0):
            qid=result[0]
            oldbalance=result[1]
            if (int(oldbalance) < int(amount)):
                return jsonify({'error': 'Not enough money to withdraw'})
            else:
                update_query="UPDATE master SET balance=%s WHERE id=%s"
                newbalance = str(int(oldbalance) - int(amount))
                par=(newbalance, qid)
                c.execute(update_query,par)
                insert_query="INSERT INTO transaction(user_id, prev_amount, curr_amount, action_id, amount) VALUES (%s,%s,%s,%s,%s)"
                insert_param = (qid, oldbalance, newbalance, "01", amount)
                c.execute(insert_query, insert_param)
                conn.commit()
                return jsonify({'output': newbalance})
        else:
            return jsonify({'error': 'Invalid input'})

@app.route("/viewTransactions")
def view_transactions():
    c.execute("SELECT m.id, m.first_name, m.last_name, t.prev_amount, t.amount, t.action_id, t.curr_amount, t.timestamp FROM transaction t INNER JOIN master m ON t.user_id = m.id")
    data=c.fetchall()
    return render_template('view_transaction.html', data=data)

@app.route("/listJson")
def show_json():
    c.execute("""
        SELECT id, first_name, last_name, balance, registration_date
        FROM master
    """)
    rows = c.fetchall()

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['first_name'] = row[1]
        d['last_name'] = row[2]
        d['balance'] = row[3]
        d['registration_date'] = str(row[4])
        objects_list.append(d)
    j = json.dumps(objects_list)
    return render_template("show_json.html", data=j)

### src: https://stackoverflow.com/questions/29726929/converting-sql-file-to-a-text-table-using-python
@app.route("/listText")
def read_textfile():
    c.execute("""
        SELECT id, first_name, last_name, balance, registration_date
        FROM master
    """)
    rows = c.fetchall()
    f = open(os.path.join(DATA_DIR, 'out.txt'), 'w')
    f.write('ID\t\t|\tFirstname\t|\tLastname\t|\tBalance\t|\tDate\n')
    for row in rows:
        for idx, item in enumerate(row):
            if idx == 0:
                f.write(str(item))
            else:
                f.write('\t\t|\t')
                f.write(str(item))
        f.write("\n")
    f.close()
    return render_template('show_textfile.html')

app.run(debug=True, host="0.0.0.0", port=5003)