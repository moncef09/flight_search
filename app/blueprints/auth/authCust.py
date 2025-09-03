from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

auth = Blueprint('authCust', __name__)

#Authenticates the login of Customer
@auth.route('/loginAuthCust', methods=['GET', 'POST'])
def loginAuthCust():
	#grabs information from the forms
	username = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and password = md5(%s)' #md5 to hash password
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['usertype'] = "customer"
		return redirect(url_for('main.home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)
	
#Authenticates the register of Customer
@auth.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCust():
	#grabs information from the forms
	email = request.form.get('email')
	password = request.form.get('password')
	name = request.form.get('name')
	building_num = request.form.get('building_num')
	street = request.form.get('street')
	city = request.form.get('city')
	state = request.form.get('state')
	phone_num = request.form.get('phone_number')
	passport_number = request.form.get('passport_number')
	passport_expiration = request.form.get('passport_expiration')
	passport_country = request.form.get('passport_country')
	date_of_birth = request.form.get('date_of_birth')

	# Check if all required fields are provided
	if not all([email, password, name, building_num, street, city, state, 
	           phone_num, passport_number, passport_expiration, 
	           passport_country, date_of_birth]):
		error = "All fields are required"
		return render_template('register_customer.html', error=error)

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = "SELECT * FROM Customer WHERE email = %s"
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_customer.html', error=error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'  #added md5 to hash password
		cursor.execute(ins, (email, password, name, building_num, street, city, state, 
		                    phone_num, passport_number, passport_expiration, 
		                    passport_country, date_of_birth))
		current_app.config['db'].commit()
		cursor.close()
		return render_template('index.html')