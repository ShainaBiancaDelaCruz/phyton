from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
myconn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='shainaexam'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        reason = request.form['reason']

        mycursor = myconn.cursor()
        sql = "INSERT INTO info (name,gender,email,phone,date,time,reason) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (name, gender, email, phone, date, time, reason)
        mycursor.execute(sql, data)
        myconn.commit()

        mycursor1 = myconn.cursor()
        sql = "SELECT * FROM info"
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        if myresult:
            return render_template('bookedappointment.html', patient=myresult)


@app.route('/booked', methods=['POST', 'GET'])
def booked():
    mycursor = myconn.cursor()
    sql = "SELECT * FROM info"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()


    return render_template('bookedappointment.html', patient=myresult)



@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'GET':
        mycursor = myconn.cursor()
        sql = "SELECT * FROM info WHERE id=%s"
        data = (id,)
        mycursor.execute(sql, data)
        myresult = mycursor.fetchall()
        if myresult:
            return render_template('update.html', myresult=myresult)
    elif request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        reason = request.form['reason']
        mycursor = myconn.cursor()
        sql = "UPDATE info SET name=%s, gender=%s, email=%s, phone=%s, date=%s, time=%s, reason=%s WHERE id=%s"
        data = (name, gender, email, phone, date, time, reason, id)
        mycursor.execute(sql, data)
        myconn.commit()
        return redirect('/booked')

@app.route('/delete/<id>')
def delete(id):
    mycursor = myconn.cursor()
    sql = "DELETE FROM info WHERE id=%s"
    data = (id,)
    mycursor.execute(sql, data)
    myconn.commit()
    mycursor1 = myconn.cursor()
    sql = "SELECT * FROM info"
    mycursor1.execute(sql)
    myresult = mycursor1.fetchall()
    if myresult:
        return render_template('bookedappointment.html', patient=myresult)

if __name__ == '__main__':
    app.run(debug=True)