from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456', 
    'database': 'r',
}

conn = mysql.connector.connect(**mysql_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/next', methods=['GET', 'POST'])
def next():
    return render_template('next.html')
@app.route('/fine', methods=['GET', 'POST'])
def fine():
    return render_template('fine.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (name,password) VALUES (%s,%s)", (name, password,))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data WHERE name=%s AND password=%s", (name, password))
        user = cursor.fetchone()
        cursor.fetchall()
        cursor.close()
        if user:
            return redirect(url_for('next'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/attend', methods=['GET', 'POST'])
def attend():
    return render_template('attend.html')

@app.route('/n', methods=['GET', 'POST'])
def n():
    return render_template('n.html')

@app.route('/a', methods=['GET', 'POST'])
def a():
    if request.method == 'POST':
        date = request.form['date']
        year = request.form['year']
        branch = request.form['branch']
        section = request.form['section']
        roll_numbers = request.form.getlist('roll_number')
        cursor = conn.cursor()
        for roll_number in roll_numbers:
            cursor.execute("INSERT INTO attendance (date, year, branch, section, roll_number) VALUES (%s, %s, %s, %s, %s)", (date, year, branch, section, roll_number))
        conn.commit()
        cursor.close()
    return render_template('n.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

@app.route('/f',methods=['GET','POST'])
def f():
	if request.method=='POST':
		fromdate=request.form['fromdate']
		todate=request.form['todate']
		year=request.form['year']
		branch=request.form['branch']
		section=request.form['section']
		cursor = conn.cursor()
		cursor.execute("SELECT roll_number,date FROM attendance WHERE date between %s and %s and year=%s and branch=%s and section=%s order by roll_number" , (fromdate,todate,year,branch,section))
		user = cursor.fetchall()
		cursor.close()

		cursor = conn.cursor()
		cursor.execute("select roll_number,count(*) from attendance t2 where roll_number in (SELECT roll_number FROM attendance WHERE date between %s and %s and year=%s and branch=%s and section=%s order by date) group by roll_number order by roll_number" , (fromdate,todate,year,branch,section))
		data1 = cursor.fetchall()
		cursor.close()

	return render_template('result.html',data=user,data1=data1)
@app.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')
@app.route('/ab', methods=['GET', 'POST'])
def ab():
    return render_template('ab.html')
@app.route('/d',methods=['GET','POST'])
def d():
	if request.method=="POST":
		date=request.form['date']
		year=request.form['year']
		branch=request.form['branch']
		section=request.form['section']
		cursor=conn.cursor()
		cursor.execute("select roll_number from attendance where date=%s and year=%s and branch=%s and section=%s order by roll_number",(date,year,branch,section))
		user=cursor.fetchall()
		cursor.close()
	return render_template('ab.html',data=user)
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')
@app.route('/e',methods=['GET','POST'])
def e():
	if request.method=="POST":
		date=request.form['date']
		roll_number=request.form['roll_number']
		cursor=conn.cursor()
		cursor.execute("delete from attendance where date=%s and roll_number=%s",(date,roll_number))
		conn.commit()
		cursor.close()
	#return render_template('ab.html')
	return redirect(url_for('data'))
if __name__ == '__main__':
    app.run(debug=True)
